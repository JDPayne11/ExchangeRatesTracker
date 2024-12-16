from datetime import datetime
from config import get_config, get_secret
from utils import get_exchange_rates
from handlers import send_email

def lambda_handler(event, context):

    # Threshold to send email notifcations
    THRESHOLD = .75
        
    config = get_config()

    secret_dict = get_secret(config)

    exchange_rate_CAD_to_USD = get_exchange_rates("CAD", secret_dict)
    print(f" - {datetime.now()} - CAD to USD exchange rate is: {exchange_rate_CAD_to_USD} ")

    if exchange_rate_CAD_to_USD > THRESHOLD:
        print(f"Email notifications send because exchange rate is higher than threshold: {exchange_rate_CAD_to_USD}")
        send_email(THRESHOLD, exchange_rate_CAD_to_USD, secret_dict)
    else:
        print(f"CAD of {exchange_rate_CAD_to_USD} still sucks")

    return



mock_event = {
    'name': 'Alice'
}
mock_context = {}

# Manually call the lambda_handler function (for local testing)
response = lambda_handler(mock_event, mock_context)


        