#!/usr/bin/env python3
# Program to email me if my IP address randomly changes.
import requests
import smtplib
import sys
import os
from dotenv import load_dotenv

load_dotenv()


def create_ip_file(IP):
    """
    Create txt file with my current ip for program to reference next time.
    """
    with open("current_ip.txt", "w") as file:
        file.write("{}\n".format(IP))
    file.close()


def change_ip(sender, new_ip):
    """
    Set details for email to be sent.
    """
    sendTo = os.environ.get("MyCurrentEmail")
    emailSubject = "IP Address changed - Rasp Server"
    emailContent = "The IP Adddress has changed and now is {}".format(new_ip)
    sender.sendmail(sendTo, emailSubject, emailContent)


# Email Variables
SMTP_SERVER = 'smtp.gmail.com'  # Email Server
SMTP_PORT = 587  # Server Port
GMAIL_USERNAME = os.environ.get("EmailFrom")
GMAIL_PASSWORD = os.environ.get("EmailPassword")


# Emailer class to define attributes of email
class Emailer:
    def sendmail(self, recipient, subject, content):
        # Create Headers
        headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: "
                   + recipient, "MIME-Version: 1.0", "Content-Type: text/html"]
        headers = "\r\n".join(headers)
        # Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()
        # Login to Gmail
        session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
        # Send Email & Exit
        session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n"
                         + content)
        session.quit


# class init
sender = Emailer()


def main() -> int:
    """
    main method: Checks for current ip from file
    Makes an api request to determine the current IP.
    """
    web_info = requests.get("https://api.ipify.org")
    current = ""
    try:
        with open("current_ip.txt", "r") as file:
            lines = file.readlines()
            current = lines[0].strip()
        file.close()
    except IOError:
        print("No current ip file")
        # create file
        create_ip_file(str(web_info.text))
        change_ip(sender, str(web_info.text))
        exit(0)
    if (web_info.text != current):
        change_ip(sender, str(web_info.text))
        exit(0)
    return (0)


if __name__ == "__main__":
    sys.exit(main())
