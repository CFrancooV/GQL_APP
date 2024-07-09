
import boto3
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError,ClientError
from dotenv import load_dotenv
import os

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
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except NoCredentialsError:
        print("Credentials not available")
        return None
    except PartialCredentialsError:
        print("Incomplete credentials")
        return None
    except ClientError as e:
        # Handle specific exceptions that could be raised
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"The requested secret {secret_name} was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print(f"The request was invalid due to: {e}")
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print(f"The request had invalid params: {e}")
        else:
            print(f"An error occurred: {e}")
        return None


    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    # Parse the JSON secret if it is a JSON object
    secret_dict = json.loads(secret)
    #print(secret_dict)
    return secret_dict['DB_URL']

DB_URL = get_secret()
#print(DB_URL)

