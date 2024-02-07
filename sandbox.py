import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from configuration import sender_passwords
from configuration import sender_passwords

sender_password =sender_passwords
def send_email(sender_email,recipient_email, subject, body):
    # Create a MIMEMultipart message
    print("send to: ", recipient_email, " ", subject, " ", body)
    print("body is; ", body)
    msg = MIMEMultipart()

    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Add the email body to the message.
    msg.attach(MIMEText(body, 'plain'))

    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Enable security
    server.login(sender_email, sender_password)  # Log in to the SMTP server

    # Send the email
    server.send_message(msg)
    server.quit()

    print("Email 1 sent successfully!")
    # return
    # nie dajemy pustego return na końcu funkcji, jest tam domyślnie
#
send_email('slawek.piela@koios-mail.pl','slawek.piela@mac.com','test', 'this is a test')
# Email details
# sender_email = "slawek.piela@koios-mail.pl"  # Replace with your Gmail address
# sender_password = sender_passwords  # Replace with your Gmail password or app-specific password
# recipient_email = "slawek.piela@koios-mail.pl"  # Replace with the recipient's email address
# subject = "KOIOS"
# body = "Czy KOIOS obsługuje tagi NFC?"

# send_email(sender_email, sender_password, recipient_email, subject, body)
