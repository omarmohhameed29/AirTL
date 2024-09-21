import smtplib

def send_success_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Secure the connection
    
    # Creating the email headers and message body
    subject = "Airflow DAG Status"
    body = "All Tasks Succeeded"
    message = f"Subject: {subject}\n\n{body}"  # Note the double newline
    
    server.login("Your Email", "Your SMTP Secret Key")
    server.sendmail("Your Email", "Destination Eamil", message)
    server.quit()


def send_failure_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Secure the connection
    
    # Creating the email headers and message body
    subject = "Airflow DAG Status"
    body = "one or more task failed"
    message = f"Subject: {subject}\n\n{body}"  # Note the double newline
    
    server.login("Your Email", "Your SMTP Secret Key")
    server.sendmail("Your Email", "Destination Eamil", message)
    server.quit()
