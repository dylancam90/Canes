import smtplib, ssl
from jinja2 import Template
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Email:
    load_dotenv()

    def __init__(self, sender, reciever, password) -> None:
        self.sender = sender
        self.reciever = reciever
        self.password = password

        self.msg = MIMEMultipart("alternative")
        self.context = ssl.create_default_context()


    def set_subject(self, subject) -> None:
        self.msg["Subject"] = subject
        self.msg["FROM"] = self.sender
        self.msg["To"] = self.reciever


    def set_parts(self, *args) -> None:
        for key in args:
            part = MIMEText(key[0], key[1])

            self.msg.attach(part)


    def create_template(self, values):
        with open("assets/template.html") as f:
            template = Template(f.read())

        return template.render(values=values)


    def run(self):
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=self.context) as smtp:
                smtp.login(self.sender, self.password)
                smtp.sendmail(self.sender, self.reciever, self.msg.as_string())
        except:
            return False

        return True


""" OG """

# load_dotenv()

# email_sender = os.environ["EMAIL"]
# email_password = os.environ["PASSWORD"]
# email_reciever = "kalivm90@gmail.com"

# msg = MIMEMultipart('alternative')
# msg['Subject'] = "Canes Notification"
# msg['From'] = email_sender
# msg['To'] = email_reciever

# context = ssl.create_default_context()

# text = "Caines"
# html = open("index.html")

# part1 = MIMEText(text, "plain")
# part2 = MIMEText(html.read(), "html")

# msg.attach(part1)
# msg.attach(part2)


# with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
#     smtp.login(email_sender, email_password)
#     smtp.sendmail(email_sender, email_reciever, msg.as_string())

