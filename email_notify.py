susmitha@infra-test:~/susmitha$ cat emailnotify.py
import smtplib
from email.message import EmailMessage

def send_email(subject, body, to_email):
    smtp_server = 'smtp.office365.com'  # Outlook/Office 365 server
    smtp_port = 587
    sender_email = 'infrastructure@redbackops.com'
    sender_password = 'Gigi@1090'  # Replace with real password or app password

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"Email sent to {to_email}: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")
