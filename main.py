# -*- coding: utf-8 -*-
import argparse
import os
import shlex
import subprocess
import sys
import time
from datetime import date

import requests

import contact
import input_handler
import user_prompts
from parameters import year, invoice_number, running_on

MIN_PYTHON = (3, 0)
if (sys.version_info.major, sys.version_info.minor) < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


def run_pipes(cmds):
    """Run commands in PIPE, return the last process in chain

    Keyword arguments:
    cmds -- list of commands to be piped
    """
    cmds = map(shlex.split, cmds)
    first_cmd, *rest_cmds = cmds
    procs = [subprocess.Popen(first_cmd, stdout=subprocess.PIPE)]
    for cmd in rest_cmds:
        last_stdout = procs[-1].stdout
        proc = subprocess.Popen(cmd, stdin=last_stdout, stdout=subprocess.PIPE)
        procs.append(proc)
    return procs[-1]


def run(cmd):
    proc = subprocess.Popen(
        cmd.split(' '),
        stdout=subprocess.PIPE,
        universal_newlines=True)
    return proc.communicate()


def main():
    """ask for user all needed user input.
    generate tex files and the resulting pdf.
    Email to the customer and generate a shipping label if needed."""

    parser = argparse.ArgumentParser(description="Tool for fast generation of invoices. Also usefully to create "
                                                 "contacts.")
    parser.add_argument("-c", "--create", action='store_true',
                        help="Create a new contact in the khard addressbook", required=False)
    parser.add_argument("-d", "--dryrun", action='store_true',
                        help="Only create PDF Invoice, don't send e-mail.", required=False)
    args = parser.parse_args()

    # show the running modes
    print("Running on : " + running_on)
    print("Dryrun mode: " + str(args.dryrun))
    print("Create mode: " + str(args.create))

    if args.create:
        while True:
            contact.create()

    # lookup customer data
    customer, invoice = input_handler.get_user_input()

    # manipulate tex files
    os.chdir("latex-rechnung")

    # set correct invoice_number
    tex = open("invoice_number.tex", "w")
    tex.write(str(invoice_number))
    tex.close()

    # check for different shipping address
    if not hasattr(customer, 'work'):
        shipping_label = "wie Rechnungsadresse"
        customer.work = {"extended": "",
                         "street": "",
                         "box": "",
                         "code": "",
                         "city": ""}
    else:
        shipping_label = user_prompts.question_with_text("Wie lautet der Empfänger der Lieferadresse?")

    # create customer data file
    tex = open("customer_data.tex", "w")
    tex.write("""\\newcommand{{\\customerCompany}}{{Rechnungsadresse:}}
\\newcommand{{\\customerName}}{{{0}}}
\\newcommand{{\\customerExtended}}{{{1}}}
\\newcommand{{\\customerStreet}}{{{2} {3}}}
\\newcommand{{\\customerZIP}}{{{4}}}
\\newcommand{{\\customerCity}}{{{5}}}
\\newcommand{{\\customerEmail}}{{{6}}}

\\newcommand{{\\shippingCompany}}{{Lieferadresse:}}
\\newcommand{{\\shippingName}}{{{7}}}
\\newcommand{{\\shippingExtended}}{{{8}}}
\\newcommand{{\\shippingStreet}}{{{9} {10}}}
\\newcommand{{\\shippingZIP}}{{{11}}}
\\newcommand{{\\shippingCity}}{{{12}}}""".format(customer.name,
                                                 customer.home["extended"],
                                                 customer.home["street"],
                                                 customer.home["box"],
                                                 customer.home["code"],
                                                 customer.home["city"],
                                                 customer.email,
                                                 shipping_label,
                                                 customer.work["extended"],
                                                 customer.work["street"],
                                                 customer.work["box"],
                                                 customer.work["code"],
                                                 customer.work["city"],
                                                 ))
    tex.close()

    # create the invoice.tex file
    tex = open("_invoice.tex", "w")
    tex.write("""\\ProjectTitle{{IT Dienstleisung}}\n{0}\n{1}{2}{3}""".format(invoice.service,
                                                                              invoice.setup,
                                                                              invoice.shipping,
                                                                              invoice.specials))
    tex.close()

    # run tex to generate a pdf file and name it properly
    print("Generating the pdf file...", end='', flush=True)
    run("pdflatex -synctex=1 -interaction=batchmode _main.tex")
    run("mv _main.pdf ../../rechnungen_{year}/rechnung_{inv}_{surn}_{n}.pdf".format(year=year,
                                                                                    inv=invoice_number,
                                                                                    surn=customer.surname.replace(" ", "_").lower(),
                                                                                    n=customer.name[0].lower()))
    print("done.")

    # make sure the file exists on the server
    if running_on == "desktop":
        print("Waiting 5 seconds for the file to be uploaded.", end='', flush=True)
        for i in range(5):
            time.sleep(1)
            print(".", end='', flush=True)
        print("done.")
    else:
        run("sudo -u www-data php /var/www/nextcloud/occ files:scan --path "
            "/niklas/files/Dokumente/Gewerbe/rechnungen_{year}".format(year=year))

    # try to send the pdf as an email
    if customer.email != "" and not args.dryrun:
        print("Sending email...", end='', flush=True)
        os.chdir("../../rechnungen_{year}".format(year=year))
        try:
            run_pipes(["""echo 'Sehr geehrteR {0},\nanbei, wie vereinbart, die Rechnung.\n\n
Beste Grüße\nNiklas Hermes'""".format(customer.name),
                       """s-nail -A it-hermes -a rechnung_{inv}_{surn}_{n}.pdf -s 'R.-Nr.: {inv} {service}' -r rechnung@it-hermes.de
{email}""".format(inv=invoice_number,
                  surn=customer.surname.replace(" ", "_").lower(),
                  n=customer.name[0].lower(),
                  service=invoice.email_header,
                  email=customer.email)])
            print("done.")
        except FileNotFoundError:
            print("error. ")
            print("command not found: s-nail \nis the program installed?")
    else:

        # generate a download link to the file
        print("Generating download-link...", end='', flush=True)
        date_next_month = str(date.today().year) + '-' + str(date.today().month + 1) + '-' + str(
            date.today().day).zfill(2)
        resp = requests.post('https://cloud.it-hermes.de/ocs/v1.php/apps/files_sharing/api/v1/shares',
                             data={'shareType': '3',
                                   'permissions': '1',
                                   'expireDate': '{}'.format(date_next_month),
                                   'path': '/Dokumente/Gewerbe/rechnungen_{year}/rechnung_{inv}_{surn}_{n}.pdf'.format(
                                       year=year,
                                       inv=invoice_number,
                                       surn=customer.surname.replace(" ", "_").lower(),
                                       n=customer.name[0].lower())},
                             headers={'OCS-APIRequest': 'true'})
        if resp.status_code == 200:
            print('done.')
        else:
            print('Something went wrong during link generation. Status code: ' + str(resp.status_code))
        print("---")
        print(resp.text[resp.text.find('<url>') + 5:resp.text.find('</url>')])
        print("---")


if __name__ == "__main__":
    main()
