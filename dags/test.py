from airflow.utils.email import send_email
import os

def test_email():
    try:
        send_email(
            to='omarmohhameed828@gmail.com',  # Replace with the email where you want to receive the test
            subject='Airflow Email Test',
            html_content='This is a test email sent from Airflow.',
            files=None,
            cc=None,
            bcc=None,
            mime_subtype='mixed',
            mime_charset='utf-8',
            conn_id=None,
        )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
        print("SMTP Configuration:")
        print(f"SMTP Host: {os.environ.get('AIRFLOW__SMTP__SMTP_HOST')}")
        print(f"SMTP Port: {os.environ.get('AIRFLOW__SMTP__SMTP_PORT')}")
        print(f"SMTP User: {os.environ.get('AIRFLOW__SMTP__SMTP_USER')}")
        print(f"SMTP Mail From: {os.environ.get('AIRFLOW__SMTP__SMTP_MAIL_FROM')}")
        print(f"SMTP SSL: {os.environ.get('AIRFLOW__SMTP__SMTP_SSL')}")
        print(f"SMTP STARTTLS: {os.environ.get('AIRFLOW__SMTP__SMTP_STARTTLS')}")

if __name__ == "__main__":
    test_email()