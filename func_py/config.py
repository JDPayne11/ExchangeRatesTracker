import os
import boto3 
from botocore.exceptions import ClientError
import json
from dotenv import load_dotenv

def get_config():
    if os.getenv('ENV') == 'production':
        # Use production environment variables or AWS services like Secrets Manager
        return {
            'SENDER_EMAIL': os.getenv('SENDER_EMAIL'),
            'RECEIVER_EMAIL': os.getenv('RECEIVER_EMAIL'),
            'APP_ID': os.getenv('APP_ID'),
            'APIKEY': os.getenv('APIKEY'),
            'AWS_REGION_NAME': os.getenv('AWS_REGION'),
            'AWS_SECRET_NAME': os.getenv('AWS_SECRET_NAME')
        }
    else:
        # Use local .env for development
        from dotenv import load_dotenv
        load_dotenv()  # Load environment variables from .env file
        return {
            'SENDER_EMAIL': os.getenv('SENDER_EMAIL'),
            'RECEIVER_EMAIL': os.getenv('RECEIVER_EMAIL'),
            'APP_ID': os.getenv('APP_ID'),
            'APIKEY': os.getenv('APIKEY'),
            'AWS_REGION_NAME': os.getenv('AWS_REGION'),
            'AWS_SECRET_NAME': os.getenv('AWS_SECRET_NAME')
        }
    

def get_secret(config):

    secret_name = config["AWS_SECRET_NAME"]
    region_name = config["AWS_REGION_NAME"]
    sender_email = config["SENDER_EMAIL"]
    receiver_email = config["RECEIVER_EMAIL"]
    app_id = config["APP_ID"]
    apikey = config["APIKEY"]

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
    secret_json = json.loads(secret)

    sender_email = secret_json.get(sender_email) 
    receiver_email = secret_json.get(receiver_email) 
    email_password = secret_json.get(app_id) 
    api_key = secret_json.get(apikey) 


    return {
            "sender_email": sender_email,
            "receiver_email": receiver_email,
            "email_password": email_password,
            "api_key": api_key
        }