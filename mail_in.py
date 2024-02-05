import email
import imaplib
import re
import requests
import json
import email.header
from datetime import datetime
from bs4 import BeautifulSoup
from configuration import sender_passwords, user_mail, airtable_token, base_id, table_id2


def convert_time(
        time2convert):  # time conversion to airtable date format. if problemtic 2000-01-01 00:00:00+00:00 is assigned
    timeconverted = ''
    try:
        timeconverted = datetime.strptime(time2convert, '%a, %d %b %Y %H:%M:%S %z')
    except:

        timeconverted = ' '.join(time2convert.split()[:-1])
    else:
        timeconverted = datetime.strptime(time2convert, '%a, %d %b %Y %H:%M:%S %z')
    return timeconverted


def decode_mime_words(encoded_str):
    decoded_words = email.header.decode_header(encoded_str)
    return ' '.join(
        word.decode(encoding or 'utf-8') if isinstance(word, bytes) else word
        for word, encoding in decoded_words
    )


from configuration import sender_passwords, user_mail, airtable_token, base_id, table_id2

print("2")


def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator='\n', strip=True)


def extract_email_address(raw_from):
    # Convert Header object to string, if necessary
    if isinstance(raw_from, email.header.Header):
        raw_from = str(raw_from)

    if raw_from is None:
        return None
    # Use regular expression to find text between < and >
    match = re.search(r'<(.+?)>', raw_from)
    if match:
        return match.group(1)

    return raw_from  # Return the original string if no match or raw_from is not None


def get_email_content(message):
    # Extract content from email message, focusing on plain text."""
    parts = []

    if message.is_multipart():
        for part in message.walk():
            # Check content type, skip if not text/plain
            if part.get_content_type() != 'text/plain':
                continue

            # Get the payload, skip if it's None
            payload = part.get_payload(decode=True)
            if payload is None:
                continue

            charset = part.get_content_charset()
            if charset is not None:
                try:
                    # Decode using the charset specified in the email
                    parts.append(payload.decode(charset))
                except UnicodeDecodeError:
                    # In case of decoding error, skip this part
                    continue
            else:
                # If no charset specified, try UTF-8 as a default
                try:
                    parts.append(payload.decode('utf-8'))
                except UnicodeDecodeError:
                    continue
    else:
        # If the message is not multipart, decode directly
        payload = message.get_payload(decode=True)
        if payload:
            try:
                # Attempt to decode with UTF-8
                parts.append(payload.decode('utf-8'))
            except UnicodeDecodeError:
                # Fallback to a different encoding, like ISO-8859-1
                parts.append(payload.decode('iso-8859-1'))

    html_content = "\n".join(parts)
    email_content = extract_text_from_html(html_content)

    return email_content


def fetch_all_emails():
    print("fetch all")
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(user_mail, sender_passwords)

    # initialise airtable
    url2 = f"https://api.airtable.com/v0/{base_id}/{table_id2}"
    headers = {
        "Authorization": "Bearer " + str(airtable_token),
        "Content-Type": "application/json",
    }
    # response = requests.get(url2, headers=headers)

    # Fetch all available mailboxes
    status, mailboxes = mail.list()
    if status == 'OK':
        for mailbox in mailboxes:
            print('\n', 'mbox: ', mailbox.decode().split(' "/" ')[1].strip('"'))
            if mailbox is None:
                print("No mailbox name")
                continue

            try:
                mailbox_name = mailbox.decode().split(' "/" ')[1].strip('"')
                mail.select(f'"{mailbox_name}"')  # Select the mailbox
            except Exception as e:
                print(f"Error selecting mailbox {mailbox}: {e}")
                continue  # Skip to the next mailbox

            # Search for all emails in this mailbox
            try:
                result, data = mail.search(None, 'ALL')
                email_ids = data[0].split()
            except imaplib.IMAP4.error as e:
                print(f"Error searching in mailbox {mailbox_name}: {e}")
                mailbox_name = mailbox.decode().split(' "/" ')[1].strip('"') + "err"
                mail.select(f'"{mailbox_name}"')  # Select the mailbox
                continue  # Skip to the next mailbox

            for email_id in email_ids:
                # Fetch each email
                result, email_data = mail.fetch(email_id, '(RFC822)')
                raw_email = email_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # Extract relevant information
                email_id_str = email_id.decode()
                email_date = convert_time(msg['Date'])
                email_raw_date = msg['Date']
                print(email_date)
                sender_header = str(msg['from'])
                recipient_header = str(msg['to'])
                sender = extract_email_address(sender_header)
                recipient = extract_email_address(recipient_header)
                subject = decode_mime_words(str(msg['subject']))
                content = get_email_content(msg)
                message_id = str(msg['message-ID'])
                print('\r', email_id, end='')

                if content:
                    # Write to file
                    with open('email_details.txt', 'a') as file:

                        file.write(f"Date/time: {email_date}\n")
                        file.write(f"Raw Date/time: {email_raw_date}\n")
                        file.write(f"Sender: {sender}\n")
                        file.write(f"Recipient: {recipient}\n")
                        file.write(f"Subject: {subject}\n")
                        file.write(f"Content:\n{content}\n")
                        file.write(f"Content:\n{message_id}\n")
                        file.write("-" * 50 + "\n")

                        data = {
                            "fields": {
                                "uid": f'{message_id}',
                                "mailbox":f'{mailbox_name}',
                                "Date": f"{email_date}",
                                "raw_date": f"{email_raw_date}",
                                "sender": f"{sender}",
                                "recipient": f"{recipient}",
                                "subject": f"{subject}",
                                "content": f"{content}",

                                # Add other fields here

                            }
                        }
                        response = requests.post(url2, headers=headers, data=json.dumps(data))
                        if response.status_code == 200:
                            pass
                        else:
                            print("Airtable post error", {e})
                else:
                    pass
        return


# Call the function to fetch all emails

if __name__ == "__main__":
    fetch_all_emails()
