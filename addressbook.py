# -*- coding: utf-8 -*-
import ast
import contact
import main
import user_prompts
from customer import Customer
from parameters import khard_prefix


def search(search_name):
    """Search with help of khard inside a folder of vcf files.
    The folder has to be configured in the khard config file.
    If no contact was found the creation of a new contact can be started right away.

    Keyword arguments:
    search_name -- any string about a given contact
    :return name, extended, street, box, code, city, email
    """

    # check if the contact is saved in the addressbook, otherwise create it

    checkOutput = main.run(f"{khard_prefix}khard list {search_name}")[0][:-1]

    while checkOutput == "Found no contacts":
        if user_prompts.confirmation("The given Contact doesn't exists. Retype?", True):
            search_name = user_prompts.question_with_text("Retype the contact info")
        elif user_prompts.confirmation("Do you want to create the contact?", True):
            contact.create()
        else:
            exit(0)

        checkOutput = main.run(f"{khard_prefix}khard list {search_name}")[0][:-1]

    postalCmd = main.run(f"{khard_prefix}khard list {search_name} --fields post_addresses --parsable")

    if "\n" == postalCmd[0]:
        customer = Customer({'home': {'box': '', 'extended': '', 'street': '', 'code': '', 'city': '', 'region': '', 'country': ''}})
    else:
        customer = Customer(ast.literal_eval(postalCmd[0].replace("[", "").replace("]", "")))

    customer.email = main.run(f"{khard_prefix}khard list {search_name} --fields email --parsable")[0][6:].strip()
    customer.name = main.run(f"{khard_prefix}khard list {search_name} --fields name --parsable")[0].strip()
    customer.firstname = main.run(f"{khard_prefix}khard list {search_name} --fields first_name --parsable")[0].strip()
    customer.surname = main.run(f"{khard_prefix}khard list {search_name} --fields last_name --parsable")[0].strip()

    return customer
