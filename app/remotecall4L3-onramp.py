import email
import logging
import json
from cgitb import text
from distutils.command.clean import clean
from multiprocessing.sharedctypes import Value
import os
from time import time
from typing import Dict
from xmlrpc.client import DateTime
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import boto3
from botocore.exceptions import NoCredentialsError
import requests

# Initializes your app with your bot token and socket mode handler
# app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
responseAppToken = "<App-token>"
responseBotToken = "<Bot-token>"
app = App(token=responseBotToken)



dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table("serverlessrepo-onramp-form-FormDataTable-13NPSDX8KPSY3")
# items = table.scan()['Items']
response = table.scan()
repo_lists = []
for itemsx in response['Items']:
    ditc1=json.loads(itemsx.get('formData'))
    print(ditc1['AccountNumber'])
    repo_lists.append(ditc1['AccountNumber'])

for i in repo_lists:	
	print(i)	


def call_dynamo():
	dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
	table = dynamodb.Table("serverlessrepo-onramp-form-FormDataTable-13NPSDX8KPSY3")
	# items = table.scan()['Items']
	response = table.scan()
	repo_lists = []
	for itemsx in response['Items']:
		ditc1=json.loads(itemsx.get('formData'))
		print(ditc1['AccountNumber'])
		repo_lists.append(ditc1['AccountNumber'])


dic = {"type": "modal",
				"callback_id": "gratitude-modal",
				"title": {"type": "plain_text", "text": "Client Details"},
				"submit": {"type": "plain_text", "text": "Submit"},
				"close": {"type": "plain_text", "text": "Cancel"},
				"blocks": [
					
					{
				"type": "input",
				"block_id": "my_block_8",
				"element": {
					"type": "static_select",
					"action_id": "static_select-action",
					"placeholder": {
						"type": "plain_text",
						"text": "Select a Client"
					},
					"options": [
						
						
					]
				},
				
				"label": {
					"type": "plain_text",
					"text": "Onramp Clients"
				}
			},
			            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "If account number not listed please click update list button."},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Update List"},
                    "action_id": "listupdate",
                },
            }
					],}

for n in repo_lists:
	item_dict = {
							"text": {
								"type": "plain_text",
								"text": n
							},
							"value": n
	}
	# print(dic['blocks'][0]['element']['options'])
	value = dic['blocks'][0]['element']['options']
	value.append(item_dict)
	# print(dic)
	

# printing result 
    # print("Dictionary after nested key update : " + str(dic))

# Step 5: Payload is sent to this endpoint, we extract the `trigger_id` and call views.open
@app.command("/cross")
def handle_command(body, ack, client, logger):
	
    logger.info(body)
    ack()
	
    res = client.views_open(
        trigger_id=body["trigger_id"],
		
        view=dic
    )
	
    logger.info(res)
	

	

# calling dynamodb item for display customer name
# response = table.get_item(
#     Key={
#         'awsid': '6057526'
        
#     }
# )
# x = response['Item']['items']
# x_dict = json.loads(x)
# cus_name= x_dict['customername']
# # cus_email = x_dict['email']
# # print(cus_email)



    
# Step 4: The path that allows for your server to receive information from the modal sent in Slack
@app.view("gratitude-modal")
def view_submission(ack, body, client, logger, say):
    ack()
    slackbot_onramp = "C041ZAP38CQ"    
    logger.info(body["view"]["state"]["values"])
    
    global user_text_7
    user_text_7 = body["view"]["state"]["values"]["my_block_8"]["static_select-action"]["selected_option"]["value"]
    user_text_7_text = body["view"]["state"]["values"]["my_block_8"]["static_select-action"]["selected_option"]["text"]["text"]
    say(blocks= [{"type": "divider"}],channel=slackbot_onramp)
    client.chat_postMessage(channel=slackbot_onramp, text=":hotel: *Client Info*")
    # client.chat_postMessage(channel=slackbot_onramp, text="Client Name: "+user_text_7_text)
	# client.chat_postMessage(channel=slackbot_onramp, text="Email: ")
    client.chat_postMessage(channel=slackbot_onramp, text="AWS Acc number: "+user_text_7+ "\n")
	

    say(
        blocks=[
                
        {
          "type": "divider"
                            }],channel=slackbot_onramp)
    say(":bell: *Select an Option :* ",channel=slackbot_onramp)
    say(
        blocks=[
                
        {
          "type": "divider"
                            },  
                {
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "Client "+user_text_7_text+"- S3 Bucket list"
				},
				"accessory": {
					"type": "button",
					"action_id": "button_click_4",
					"text": {
						"type": "plain_text",
						# "emoji": true,
						"text": "S3"
					},
					"value": "click_me_123"
				}
			},
            {
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "Client "+user_text_7_text+"- EC2 instance list"
				},
				"accessory": {
					"type": "button",
					"action_id": "button_click_5",
					"text": {
						"type": "plain_text",
						# "emoji": true,
						"text": "EC2"
					},
					"value": "click_me_123"
				}
			},
			# {
			# 	"type": "section",
			# 	"text": {
			# 		"type": "mrkdwn",
			# 		"text": "Client "+user_text_7_text+"- IAM user list"
			# 	},
			# 	"accessory": {
			# 		"type": "button",
			# 		"action_id": "button_click_6",
			# 		"text": {
			# 			"type": "plain_text",
			# 			# "emoji": true,
			# 			"text": "IAM"
			# 		},
			# 		"value": "click_me_123"
			# 	}
			# },
            {
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "Client "+user_text_7_text+"- STS Assume Role"
				},
				"accessory": {
					"type": "button",
					"action_id": "button_click_7",
					"text": {
						"type": "plain_text",
						# "emoji": true,
						"text": "STS ROLE"
					},
					"value": "click_me_123"
				}
			}
        ],channel="C041ZAP38CQ"
    )
    return user_text_7


# ---------------------------button click continue-------------------------

@app.action("button_click_4")
def action_button_click(ack, say ):
    ack()
    
    print(user_text_7)
    # support link https://www.youtube.com/watch?v=sbsVhX-9gSQ&t=516s
    URL = f"https://kefqqcgyj3.execute-api.us-east-1.amazonaws.com/v1/s3?id={user_text_7}"
    headers = {"Contenet-Type": "application/json"}
    r = requests.request("GET", URL, headers=headers)
    say(":open_file_folder:----S3 BUCKET LIST----")
    say(r.text)
    

@app.action("button_click_5")
def action_button_click(ack, say ):
    ack()
    print(user_text_7)
    URL = f"https://kefqqcgyj3.execute-api.us-east-1.amazonaws.com/v1/ec2?id={user_text_7}"
    headers = {"Contenet-Type": "yourstage/yourpath"}
    r = requests.request("GET", URL, headers=headers)
    say(":computer:----EC2 LIST----")
    say(r.text)
    

@app.action("listupdate")
def action_button_click(ack, say ):
    ack()
    # print(user_text_7)
    URL = f"https://5nbdz8lkog.execute-api.us-east-1.amazonaws.com/v1/id?id="
    headers = {"Contenet-Type": "yourstage/yourpath"}
    r = requests.request("GET", URL, headers=headers)
    say(":busts_in_silhouette: List updated.",channel="C041ZAP38CQ")
    # say(r.text)
    

@app.action("button_click_7")
def action_button_click(ack, say ):
    ack()
    print(user_text_7)
    URL = f"https://kefqqcgyj3.execute-api.us-east-1.amazonaws.com/v1/sts?id={user_text_7}"
    headers = {"Contenet-Type": "yourstage/yourpath"}
    r = requests.request("GET", URL, headers=headers)
	
    say(":bust_in_silhouette:----ASSUME ROLE INFO----")
    say(r.text)
    

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, responseAppToken).start()



# # https://www.youtube.com/watch?v=sbsVhX-9gSQ&t=516s&ab_channel=SrceCde

