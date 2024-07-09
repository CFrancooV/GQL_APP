import boto3
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from dotenv import load_dotenv
import os

# Load environment variables from .env file if present
load_dotenv()

SECRET_NAME = os.getenv("SECRET_NAME")
REGION_NAME = os.getenv("REGION_NAME")

def get_secret():
    secret_name = SECRET_NAME
    region_name = REGION_NAME

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except NoCredentialsError:
        print("AWS credentials not available")
        return None
    except PartialCredentialsError:
        print("Incomplete AWS credentials")
        return None
    except ClientError as e:
        # Handle specific exceptions that could be raised
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            print(f"The requested secret {secret_name} was not found")
        elif error_code == 'InvalidRequestException':
            print(f"The request was invalid due to: {e}")
        elif error_code == 'InvalidParameterException':
            print(f"The request had invalid params: {e}")
        else:
            print(f"An error occurred: {e}")
        return None

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    # Parse the JSON secret if it is a JSON object
    try:
        secret_dict = json.loads(secret)
        return secret_dict['DB_URL']
    except json.JSONDecodeError:
        print("Failed to parse secret JSON")
        return None

DB_URL = get_secret()
