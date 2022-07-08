# lambda function

        
#!/usr/bin/python3.6
import urllib3
import json
http = urllib3.PoolManager()
def lambda_handler(event, context):
    url = "https://hooks.slack.com/services/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"
    msg = {
        "channel": "#cloud_watch",
        "username": "U0373TEQLNN",
        "text": event['Records'][0]['Sns']['Message'],
        "icon_emoji": ""
    }
    
    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST',url, body=encoded_msg)
    print({
        "message": event['Records'][0]['Sns']['Message'], 
        "status_code": resp.status, 
        "response": resp.data
    })
    
    # https://aws.amazon.com/premiumsupport/knowledge-center/sns-lambda-webhooks-chime-slack-teams/
    # stress --cpu 2 --timeout 300s


