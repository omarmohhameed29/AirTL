import smtplib

def send_success_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Secure the connection
    
    # Creating the email headers and message body
    subject = "Airflow DAG Status"
    body = "All Tasks Succeeded"
    message = f"Subject: {subject}\n\n{body}"  # Note the double newline
    
    server.login("omarmohhameed828@gmail.com", "diceieedwxddhrqc")
    server.sendmail("omarmohhameed828@gmail.com", "om0558064@gmail.com", message)
    server.quit()


def send_failure_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Secure the connection
    
    # Creating the email headers and message body
    subject = "Airflow DAG Status"
    body = "one or more task failed"
    message = f"Subject: {subject}\n\n{body}"  # Note the double newline
    
    server.login("omarmohhameed828@gmail.com", "diceieedwxddhrqc")
    server.sendmail("omarmohhameed828@gmail.com", "om0558064@gmail.com", message)
    server.quit()

# Call the send_mail function
