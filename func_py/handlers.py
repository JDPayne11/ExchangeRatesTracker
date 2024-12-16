import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(THRESHOLD, exchange_rate_CAD_to_USD, secret_dict):

    sender_email = secret_dict["sender_email"]
    receiver_email = secret_dict["receiver_email"]
    email_password = secret_dict["email_password"]
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    subject = f"Exchange Rate Alert: {exchange_rate_CAD_to_USD} > {THRESHOLD}"
    body = f"The current CAD to USD exchange rate is {exchange_rate_CAD_to_USD}, which exceeds your threshold of {THRESHOLD}."

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, email_password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")