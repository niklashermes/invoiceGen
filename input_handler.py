from enum import Enum

import addressbook
import re
import user_prompts
from invoice import Invoice
from parameters import install_fee, wage, shipping_cost, invoice_number


class Service(str, Enum):
    """Used to determine the types of offered Services"""
    INSTALLATION = "Installation"
    REMOTE = "Remote Session"
    UN_BRICK = "Installation with bricked device/OS"
    SUPPORT = "Support"


class OS(str, Enum):
    """Used to determine the types of offered Operating Systems"""
    LOS = "LineageOS"
    GOS = "GrapheneOS"
    EOS = "/e/OS"
    COS = "CalyxOS"
    ELIXIR = "Project Elixir OS"
    PIXEL = "PixelExperience OS"
    MICROG = "LineageOS for MicroG"
    AOS = "ArrowOS"
    UBUNTU = "Ubuntu Touch"


def get_user_input():
    """Take user input interactively and get all needed customer data and service data"""
    # initialize parameters
    search_name = service_type = os_type = style = duration = setup = shipping = None
    invoice = Invoice()
    service_tex = specials_tex = pretty_specials = service_string = ""
    specials = []
    item = {}
    while True:
        # ask for the customer name
        if not search_name:
            search_name = user_prompts.question_with_text("Type in the contact info to search for")
            customer = addressbook.search(search_name)
        else:
            customer = addressbook.search(search_name)
        while "\n" in customer.name:
            print("""The results for the search string '{}' aren't unique.
Please reenter a more precise search string.""".format(search_name))
            search_name = user_prompts.question_with_text("Type in the contact info to search for")
            customer = addressbook.search(search_name)
        print("---\nFound Contact: " + customer.name + "\n---")

        # ask for the service type
        if not service_type:
            service_type = user_prompts.question_with_choices("Choose a Service type",
                                                              [service for service in Service])

        # ask for the OS
        if not os_type:
            os_type = user_prompts.question_with_choices("Choose an Operating System",
                                                         [os for os in OS])

        # create fee for the given service type
        if service_type == Service.INSTALLATION:
            service_tex = "\\Fee{{Installation von {os_type}}}{{{install_fee}}}{{1}}".format(os_type=os_type,
                                                                                             install_fee=install_fee)
            service_string = re.search(r'\\Fee{(.*?)}', service_tex).group(1)

        elif service_type == Service.REMOTE:
            # ask for the style
            if not style:
                style = user_prompts.question_with_choices("Was it an installation or just support",
                                                           [Service.INSTALLATION, Service.SUPPORT])

            # ask for the amount of time
            if not duration:
                duration = user_prompts.question_with_numbers("How long did it take in hours?")
            if style == Service.INSTALLATION:
                service_tex = "\\Fee{{Online-Beratung bei der " \
                              "Installation von {os_type}}}{{{wage}}}{{{time}}}".format(os_type=os_type,
                                                                                        time=duration,
                                                                                        wage=wage)
                service_string = re.search(r'\\Fee{(.*?)}', service_tex).group(1)
            else:
                service_tex = "\\Fee{{{os_type} software support}}{{{wage}}}{{{time}}}".format(os_type=os_type,
                                                                                               time=duration,
                                                                                               wage=wage)
                service_string = re.search(r'\\Fee{(.*?)}', service_tex).group(1)
        elif service_type == Service.UN_BRICK:
            service_tex = """\\Fee{{Wiederherstellung der Stock Firmware und Reparatur des Bootloaders.}}{{{wage}}}{{1}}
    \\Fee{{Installation von {os_type}}}{{30}}{{1}}""".format(os_type=os_type, wage=wage)
            service_string = "Wiederherstellung der Stock Firmware und Reparatur des Bootloaders." + "\n" + \
                                     "Installation von {0}".format(os_type)

        elif service_type == Service.SUPPORT:
            if not duration:
                duration = user_prompts.question_with_numbers("How long did it take in hours?")
            service_tex = "\\Fee{{{os_type} Support}}{{{wage}}}{{{time}}}".format(os_type=os_type,
                                                                                time=duration,
                                                                                wage=wage)
            service_string = re.search(r'\\Fee{(.*?)}', service_tex).group(1)
            if duration == "1":
                service_string = service_string + " " + duration + " Stunde"
            else:
                service_string = service_string + " " + duration + " Stunden"

        invoice.pretty_service = service_string
        invoice.service = service_tex

        # ask if the customer wanted a setup too
        if setup is None:
            if os_type in [OS.LOS, OS.GOS, OS.AOS]:
                setup = user_prompts.confirmation("Is the installation with Setup?")
        if os_type in [OS.LOS, OS.AOS] and setup:
            invoice.setup = "\\Fee{{Einrichtung mit F-Droid und Aurora Store als Systemapps, sowie installation von " \
                    "alternativ Apps}}{{{wage}}}{{1}}\n".format(wage=2 * int(wage))
            invoice.pretty_setup = re.search(r'\\Fee{(.*?)}', invoice.setup).group(1)
        elif os_type == OS.GOS and setup:
            invoice.setup = "\\Fee{{Einrichtung inkl. F-Droid und Aurora Store, sowie der Installation von abgeschotteten " \
                    "Google-Play-Diensten in einem separaten Profil}}{wage}{{1}}\n".format(wage=2 * wage)
            invoice.pretty_setup = re.search(r'\\Fee{(.*?)}', invoice.setup).group(1)
        else:
            invoice.setup = invoice.pretty_setup = ""

        # add shipping cost if needed
        if shipping is None:
            if service_type == Service.UN_BRICK or service_type == Service.INSTALLATION:
                shipping = user_prompts.confirmation("Will the parcel be shipped?", True)
            else:
                shipping = user_prompts.confirmation("Will the parcel be shipped?")
        if shipping:
            invoice.shipping = "\\Fee{{Versand mit DHL Paket + Materialkosten}}{shipping_cost}{{1}}\n".format(
                shipping_cost=shipping_cost)

            invoice.pretty_shipping = re.search(r'\\Fee{(.*?)}', invoice.shipping).group(1)
        else:
            invoice.shipping = invoice.pretty_shipping = ""

        # here is space for special fees
        if not specials:
            while user_prompts.confirmation("Are there any specials left to add?"):
                item["detail"] = user_prompts.question_with_text("Type the details of the item")
                item["price"] = user_prompts.question_with_numbers("Type the price of the item")
                specials_tex += "\\Fee{{{0}}}{{{1}}}{{1}} \n".format(item["detail"], item["price"])
                pretty_specials += item["detail"] + ", für " + item["price"] + " € \n"
                specials.append(item)
        elif specials:
            for item in specials:
                specials_tex += "\\Fee{{{0}}}{{{1}}}{{1}} \n".format(item["detail"], item["price"])
                pretty_specials += item["detail"] + ", für " + item["price"] + " € \n"
        else:
            specials_tex = ""

        specials_tex.rstrip()
        pretty_specials.rstrip()

        # give a summary and ask for final creation

        invoice.email_header = service_string

        if specials:
            invoice.specials = specials_tex
            invoice.pretty_specials = pretty_specials

        print("---")
        print(customer)
        print("---")
        print(invoice)
        print("---")
        print("R.-Nr.: " + str(invoice_number))
        print("---")

        if user_prompts.critical_confirmation("Are the inputs correct?"):
            return customer, invoice
        else:
            search_name = service_type = os_type = style = duration = setup = shipping = None
            invoice = Invoice()
            service_tex = specials_tex = pretty_specials = ""
            specials = []
            item = {}
