import os
import smtplib
import threading
import time
from tqdm import tqdm # type: ignore
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from typing import List

class SendEmail:
    def __init__(self) -> None:
        self.username = os.getenv('EMAIL_USERNAME')
        self.app_password = os.getenv('EMAIL_APP_PASSWORD')
        self.attachment = os.getenv('EMAIL_ATTACHMENT')
        self.server = None

    def login(self):
        """Logs into the email server."""
        try:
            # Establish connection with Gmail's SMTP server
            self.server = smtplib.SMTP("smtp.gmail.com", 587)
            self.server.starttls()  # Secure the connection
            self.server.login(self.username, self.app_password)  # Login to your email
            # print("Login successful!")
        except Exception as e:
            print(f"Login failed: {e}")
            self.server = None

    def send_email(self, receiver_email: str, subject: str, body: str):
        """Sends an email to the specified recipient."""
        if self.server is None:
            print("Please log in first.")
            return
        with open(self.attachment, "rb") as attachment:
            # Add the attachment to the message
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {self.attachment}",
        )

        message = MIMEMultipart()
        message["From"] = self.username
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))
        message.attach(part)

        try:
            # Send the email
            self.server.sendmail(self.username, receiver_email, message.as_string())
            # print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def close_connection(self):
        """Closes the SMTP server connection."""
        if self.server:
            self.server.quit()
            print("Server connection closed.")


def load_emails(file_name: str) -> list:
    """ load email ids"""
    email_lists = []
    email_list = []
    MAX = 10
    count = 0
    with open(file_name, 'r') as email_file:
        for line in email_file:
            email_list.append(line.strip())
            count = count + 1
            if count == MAX:
                email_lists.append(email_list)
                count = 0
                email_list = []
    if email_list:
        email_lists.append(email_list)     
    return email_lists

def email_send_thread(email_lists: List[str], thread_count: int):
    """ process email list """
    email_sender = SendEmail()
    email_sender.login()

    with open ('email_template.html', 'r') as input_fp:
        email_body = input_fp.read()

    for email_list in tqdm(email_lists, desc=f"Sending email - {thread_count}"):
        receiver_info = email_list.split(',')
        receiver_email = receiver_info[0]
        subject = "Thank You! Let's Stay Informed about Cisco Case and Counter Disinformation Together"        
        formatted_email_body = email_body.format(receiver_info[1])
        email_sender.send_email(receiver_email, subject, formatted_email_body)
    
    email_sender.close_connection()

if __name__ == "__main__":
    """Main method"""

    email_array = []
    email_array = load_emails('email-list.csv')
    
    email_thread_list = []
    thread_count = 1
    for email_lists in email_array:
        email_mt = threading.Thread(target=email_send_thread,
                                    args=(email_lists,thread_count,))
        email_thread_list.append(email_mt)
        thread_count = thread_count + 1
    
    for exec_email_th in email_thread_list:
        exec_email_th.start()
        time.sleep(1)