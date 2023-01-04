#!/usr/bin/env python3
from modules.send_email import Email
from modules.data import Canes
import sys, os 

# TODO, check to see if external html can be altered with variables,
# replace recipent email with Jakes

def main():
    canes = Canes("assets/SERVSAFE-WORK PERMIT LOG.xlsx", 10)
    df = canes.make_dataframe()
    list = canes.iterate(df, everyday=True)

    email = Email(os.environ["EMAIL"], os.environ["RECIPIENT"], os.environ["PASSWORD"])
    email.set_subject("Canes Expiration")
    html = email.create_template(list)

    email.set_parts(("Canes", "plain"), (html, "html"))

    run = email.run()


    # if email sent and everyday is set to false append to do not email, else if 
    if run and not canes.everyday:
        canes.append_csv(list)
        print_success(list)
    elif run and canes.everyday:
        print_success(list)
    else:
        print_error()

    # if run:
    #     # if run everyday is set to false append names to csv to not duplicate emails.
    #     if not caines.everyday:
    #         caines.append_csv(list)
    #     print_success(list)
    # else:
    #     print_error()


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