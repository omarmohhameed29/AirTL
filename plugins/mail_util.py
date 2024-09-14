import smtplib

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Secure the connection
    server.login("omarmohhameed828@gmail.com", "diceieedwxddhrqc")
    server.sendmail("omarmohhameed828@gmail.com", "omarmohhameed828@gmail.com", "Test email from Airflow environment")
    server.quit()
