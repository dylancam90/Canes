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
    table = email.append_html(list)

    html = """<html>
                <head></head>
                <body style="font-family: Arial, Helvetica, sans-serif;">
                    <h1 style="font-weight: 400; text-decoration: underline;">Employment Form Expirations</h1>
                    <table style="width: 100%; border-collapse: collapse;">
                        <thead>
                            <tr style="font-size: 20px">
                                <th style="border: 1px solid #ddd; padding: 8px; background-color: #04AA6D; color:white;">Name</th>
                                <th style="border: 1px solid #ddd; padding: 8px; background-color: #04AA6D; color:white;">Form Type</th>
                                <th style="border: 1px solid #ddd; padding: 8px; background-color: #04AA6D; color:white;">Days</th>
                            </tr>
                        </thead>
                        <tbody style="text-align: center">
                            """+table+"""
                        </tbody>
                    </table>
                </body>
            </html>"""

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