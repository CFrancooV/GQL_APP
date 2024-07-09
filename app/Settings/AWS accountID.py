# import boto3

# def print_account_id():
#     # Create an STS client
#     session = boto3.session.Session()
#     client = session.client('sts')

#     try:
#         # Call the STS get_caller_identity operation
#         response = client.get_caller_identity()
#         account_id = response['Account']
#         print(f"Your AWS account ID is: {account_id}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Call the function to print the account ID
# print_account_id()
