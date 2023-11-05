# -*- coding: utf-8 -*-
import inquirer
import re


def question_with_choices(message, choices):
    """Prompt the user to select something from the choices.

    Keyword arguments:
    message -- string shown to the user
    choices -- the list of strings to choose from
    :returns string with the choice
    """
    choices.append("Exit")
    questions = [inquirer.List("question",
                               message,
                               choices,
                               ),
                 ]
    answers = inquirer.prompt(questions)
    if answers["question"] == "Exit":
        exit(0)
    else:
        try:
            return answers["question"]
        except TypeError:
            exit(0)


def question_with_phone(message):
    """Prompt the user to input a number and only a number.

    Keyword arguments:
    message -- string shown to the user
    :returns number typed in by the user
    """
    questions = [inquirer.Text("number",
                               message,
                               validate=lambda _, x: re.match('^$|((?:\+\d{2})?\d{3,4}\D?\d{3}\D?\d{3})', x), )]
    answers = inquirer.prompt(questions)
    try:
        return answers["number"]
    except TypeError:
        exit(0)


def question_with_numbers(message):
    """Prompt the user to input a number and only a number.

    Keyword arguments:
    message -- string shown to the user
    :returns number typed in by the user
    """
    questions = [inquirer.Text("number",
                               message,
                               validate=lambda _, x: re.match('^\d*\.?\d+$', x), )]
    answers = inquirer.prompt(questions)
    try:
        return answers["number"]
    except TypeError:
        exit(0)


def question_with_text_only(message):
    """Prompt the user to input any kind of text but only text.

    Keyword arguments:
    message -- string shown to the user
    :returns the typed in text by the user
    """
    questions = [inquirer.Text("text",
                               message,
                               validate=lambda _, x: re.match('^[a-zA-ZäöüÄÖÜ]+$', x), )]
    answers = inquirer.prompt(questions)
    try:
        return answers["text"]
    except TypeError:
        exit(0)


def question_with_text(message):
    """Prompt the user to input any kind of text but only text.

    Keyword arguments:
    message -- string shown to the user
    :returns the typed in text by the user
    """
    questions = [inquirer.Text("text",
                               message, )]
    answers = inquirer.prompt(questions)
    try:
        return answers["text"]
    except TypeError:
        exit(0)


def question_with_email(message):
    """Prompt the user to input any kind of text but only text.

    Keyword arguments:
    message -- string shown to the user
    :returns the typed in text by the user
    """
    questions = [inquirer.Text("email",
                               message,
                               validate=lambda _, x: re.match('^$|(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                                                              #
                                                              x), )]
    answers = inquirer.prompt(questions)
    try:
        return answers["email"]
    except TypeError:
        exit(0)


def confirmation(message, *default):
    """Prompt the user to press y or n.

    Keyword arguments:
    message -- string shown to the user
    *default -- return value if user only presses return
    :returns the answer as a boolean value
    """
    questions = [inquirer.Confirm("confirmed",
                                  message=message,
                                  default=default)]
    answers = inquirer.prompt(questions)
    try:
        return answers["confirmed"]
    except TypeError:
        exit(0)


def critical_confirmation(message):
    """Prompt the user to confirm an important step by literally typing the answer.

    Keyword arguments:
    message -- string shown to the user
    :returns the typed in text by the user
    """
    questions = [inquirer.Text("text",
                               message=message + " [type in 'yes' or 'no']",
                               validate=lambda _, x: re.match('(?:yes|no)', x), )]
    answers = inquirer.prompt(questions)
    try:
        return True if answers["text"] == "yes" else False
    except TypeError:
        exit(0)
