import requests as re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import boto3 
from botocore.exceptions import ClientError
import json
from datetime import datetime


def lambda_handler(event, context):

    # Threshold to send email notifcations
    THRESHOLD = .75
    

    def get_secret():

        secret_name = "fnc_CADToUSDExchangeRateAlert"
        region_name = "us-east-2"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e

        secret = get_secret_value_response['SecretString']
        return json.loads(secret)


    secret_dict = get_secret()

    # Email information
    sender_email = secret_dict.get('fnc_CADToUSDExchangeRateAlert_Email_Sender') 
    receiver_email = secret_dict.get('fnc_CADToUSDExchangeRateAlert_Email_Receiver') 
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_password = secret_dict.get('fnc_CADToUSDExchangeRateAlert_Gmail_APP_ID') 
    API_KEY = secret_dict.get('fnc_CADToUSDExchangeRateAlert_APIKEY') 

    def get_exchange_rates(to_currency: str) -> float:
        """
            Finds the exchange rate to USD for a given currency.
            Params: 
                to_currency: The currency you want to convert into USD
            Returns:
                a float of the exchange rate
        """

        # Get request
        url = "https://openexchangerates.org/api/latest.json"
        params = {
            "app_id":API_KEY,
            "base":"USD",
            "symbols": to_currency
        }

        response = re.get(url, params=params)
        json_response = response.json()
        exchange_rate_to_currency = json_response["rates"]["CAD"]
        exchange_rate_to_USD = round(1 / exchange_rate_to_currency, 4)
        return exchange_rate_to_USD


    exchange_rate_CAD_to_USD = get_exchange_rates("CAD")
    print(f" - {datetime.now()} - CAD to USD exchange rate is: {exchange_rate_CAD_to_USD} ")

    if exchange_rate_CAD_to_USD > THRESHOLD:
        print(f"CAD to USD conversion rate of {exchange_rate_CAD_to_USD} is now greater than .75")

        # Compose the email
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

    else:
        print(f"CAD of {exchange_rate_CAD_to_USD} still sucks")

    return



# mock_event = {
#     'name': 'Alice'
# }
# mock_context = {}

# # Manually call the lambda_handler function (for local testing)
# response = lambda_handler(mock_event, mock_context)


        