# DONT FORGET TO CHANGE DAY_LIMIT

import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import csv, os, sys


class Caines:
    load_dotenv()
    def __init__(self, file, day_limit=7) -> None:
        self.file = file
        # days before notification is sent, 7 is the default
        self.DAY_LIMIT = day_limit
        # todays date (UPDATED TO SUBTRACT 1 DAY)
        self.TODAY = datetime.now().date() - timedelta(days=1)
        # pd column keys
        self.columns = []
        self.CSV_NAME = "assets/already_emailed.csv"

    def make_dataframe(self):
        data = pd.read_excel(
            self.file,
            skiprows=1,
            engine="openpyxl"
        ).dropna(how="all", axis=1)

        df = pd.DataFrame(data).dropna(axis=0, how="all")
        self.columns = [i for i in df.columns]
        return df


    def iterate(self, df):
        # list of people to email
        email_list = []
        # 2 empty columns to add to DF
        serv_results = []
        work_results = []

        for i in df.index:
            # all df columns
            name = df[self.columns[0]][i]
            servsafe = df[self.columns[1]][i]
            workpermit = df[self.columns[2]][i]

            # turn dates into days remaining
            serv_days = self._get_days(servsafe)
            work_days = self._get_days(workpermit)

            self._get_email_list(serv_days, name, self.columns[1], email_list)
            self._get_email_list(work_days, name, self.columns[2], email_list)

            # append to columns
            serv_results.append(serv_days)
            work_results.append(work_days)

        # add columns to DF    
        df["Servsafe Days Left"] = serv_results
        df["Work Permit Days Left"] = work_results


        # if no forms are expired, exit
        if self._check_len(email_list):
            email_list = self._check_duplicate_emails(email_list)
            return email_list


    # if length of list is greater than 0
    def _check_len(self, email_list):
        if len(email_list) < 1:
            print("No new notification needed")
            sys.exit(0)
        return True

    def _get_days(self, value):
        null_field = str(value).split(" ")[0]
        if null_field in ("MISSING", "None", "nan"):
            return None
        else:
            return str(value.date() - self.TODAY).split(" ")[0]


    def _get_email_list(self, days, name, column_name, email_list):
        buffer = dict()
        try:
            if int(days) < self.DAY_LIMIT:
                buffer["name"], buffer["form"], buffer["days"] = name, column_name.title(), days
                email_list.append(buffer)
        except TypeError:
            pass


    def _check_duplicate_emails(self, email_list):

        already = []
        # load csv into memory
        with open(self.CSV_NAME, "r") as file:
            reader = csv.DictReader(file)
            for i in reader:
                 already.append({"name": i["name"], "form": i["form"]})

        # print("ALREADY ", already, "\n")
        # print("EMAIL LIST ", email_list, "\n")

        # go through email list and check against csv values
        index = []
        for i in range(len(email_list)):
            for j in range(len(already)):
                if email_list[i]["name"] == already[j]["name"] and email_list[i]["form"] == already[j]["form"]:
                    index.append(i)

        # remove from email_list. Doing this in loop above gave me an index error (?)
        if len(index) > 0:
            for i in index:
                del email_list[i]

        # print("NEW EMAIL LIST ", email_list, "\n", "INDEX ", index)

        # if forms are expired but have already been emailed, exit
        if self._check_len(email_list):
            return email_list


    def append_csv(self, email_list):
        with open(self.CSV_NAME, "a") as file:
            writer = csv.writer(file)
            for i in email_list:
                row = [i["name"], i["form"]]
                writer.writerow(row)
