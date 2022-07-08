# lambda function
import boto3
import json


def lambda_handler(event, context):
    qs = event['queryStringParameters']['id']
    # qs = "621073710421"
    arn = "arn:aws:iam::"+qs+":role/my-assume-role"
    # arn = "arn:aws:iam::621073710421:role/my-assume-role"
    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn=arn,
        RoleSessionName="cross_acct_lambda"
    )
    
    ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
    SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
    SESSION_TOKEN = acct_b['Credentials']['SessionToken']

    # create service client using the assumed role credentials, e.g. S3
    client = boto3.client(
        'iam',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )
    users = client.list_users()
    users_list = []
    for user in users['Users']:
        user_dict = {"UserName": user['UserName'], "UserId": user['UserId'], 
                     "Arn": user['Arn'], "CreateDate": user['CreateDate']}
        users_list.append(user_dict)

    # return json.dumps(users_list, default=str,)

    return ({'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps(users_list, default=str,)
    })