# -*- coding: utf-8 -*-
import subprocess

import user_prompts
import main
import time

from parameters import running_on, khard_prefix


def create():
    first_name = user_prompts.question_with_text("First name")
    last_name = user_prompts.question_with_text("Last name")

    checkCmd = subprocess.Popen([
        "khard", "list", "{0}".format(first_name + " " + last_name)],
        stdout=subprocess.PIPE,
        universal_newlines=True)
    checkOutput = checkCmd.communicate()[0][:-1]

    while checkOutput != "Found no contacts":
        print("The given Contact already exists.")
        first_name = user_prompts.question_with_text("First name")
        last_name = user_prompts.question_with_text("Last name")

        checkCmd = subprocess.Popen([
            "khard", "list", "{0}".format(first_name + " " + last_name)],
            stdout=subprocess.PIPE,
            universal_newlines=True)
        checkOutput = checkCmd.communicate()[0][:-1]

    email = user_prompts.question_with_email("Email")
    phone = user_prompts.question_with_phone("Phone")
    try:
        temp = ""
        *street, box = user_prompts.question_with_text("Street name No.").split(" ")
        for part in street:
            temp += part
            temp += " "
        street = temp.rstrip()

        temp = ""
        code, *city = user_prompts.question_with_text("ZIP City").split(" ")
        for part in city:
            temp += part
            temp += " "
        city = temp.rstrip()
    except ValueError:
        street, box, code, city = " ", " ", " ", " "
    extended = user_prompts.question_with_text("Extended(optional, like DHL Number)")

    contact = """First name : {0}
Last name : {1}
Phone :
    cell : {2}
Email :
    work : {3}
Address :
    home :
        Box : {4}
        Extended : {5}
        Street : {6}
        Code : {7}
        City : {8}""".format(first_name, last_name, phone, email, box, extended, street, code, city)
    print(contact)
    if user_prompts.critical_confirmation("Are these information correct?"):
        # create contact yaml
        yaml = open("contact.yaml", "w")
        yaml.write(contact)
        yaml.close()
        print("Creating new contact.", end='', flush=True)
        time.sleep(1)
        print(".", end='', flush=True)

        main.run_pipes([f"{khard_prefix}khard new -a business -i contact.yaml"])
        # synchronize contacts with CardDAV server
        main.run("vdirsyncer sync")
        # make sure the file exists on the server
        if running_on == "desktop":
            print("Waiting 5 seconds for the file to be uploaded.", end='', flush=True)
            for i in range(5):
                time.sleep(1)
                print(".", end='', flush=True)
            print("done.")
        else:
            main.run("sudo -u www-data php /var/www/nextcloud/occ files:scan --path "
                     "/niklas/files/Dokumente/Gewerbe/invoiceGen/contacts")
            time.sleep(0.5)
            print("done.")
    else:
        create()
