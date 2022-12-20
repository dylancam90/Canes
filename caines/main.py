#!/usr/bin/env python3

from modules.send_email import Email
from modules.data import Caines
import sys, os 

# TODO, check to see if external html can be altered with variables,
# replace recipent email with Jakes

def main():
    caines = Caines("assets/SERVSAFE-WORK PERMIT LOG.xlsx", 10)
    df = caines.make_dataframe()
    list = caines.iterate(df)

    email = Email(os.environ["EMAIL"], os.environ["RECIPIENT"], os.environ["PASSWORD"])
    email.set_subject("Caines Expiration")
    html = email.create_template(list)

    email.set_parts(("Caines", "plain"), (html, "html"))
    run = email.run()

    if run:
        caines.append_csv(list)
        print_success(list)
    else:
        print_error()


def print_success(list):
    print("EMAIL SENT!")
    for i in list:
        print(f"Name:  {i['name']},\tForm:  {i['form']}")
    sys.exit(0)


def print_error():
    print("ERROR, check recipient email and try again.")
    sys.exit(1)


if __name__ == "__main__":
    main()