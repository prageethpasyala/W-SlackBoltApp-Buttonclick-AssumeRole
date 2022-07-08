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
    client = boto3.resource(
        'ec2',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )


    instances = client.instances.all()
    result = []
    for instance in instances:
        # print(f'  {bucket2["UserName"]}')
        result.append(instance.id)
        result.append(instance.state)
        result.append(instance.state)
        result.append(instance.image.id)
        result.append(instance.platform)
        result.append(instance.instance_type)
        result.append(instance.public_ip_address)
        print (instance.id)


    d = {"EC2 Instances : ":result, "ACCOUNT-ID":qs }
    
    return ({'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps(d)
    })
    
    # https://d2qcz467o9.execute-api.us-east-1.amazonaws.com/v1/id?id=621073710421

