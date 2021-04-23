import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender, password, receiver, subject, message):
    '''
    Sends an email from a given gmail account.
    Requires:
        - sender (string), a gmail account with 'less secure apps' permissions
        - password (string), the password to the sender's email account
        - receiver (string), an email address
        - subject (string), the email subject
        - message (string), the email body message in plain text
    Ensures: an email is sent from the sender to the receiver, with the given
    subject and message.
    '''

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    
    server.quit()
