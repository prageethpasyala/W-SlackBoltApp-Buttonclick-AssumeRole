import logging
import json
from cgitb import text
from distutils.command.clean import clean
import os
from time import time
from xmlrpc.client import DateTime
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import boto3
from botocore.exceptions import NoCredentialsError
import requests

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Step 5: Payload is sent to this endpoint, we extract the `trigger_id` and call views.open
@app.command("/add")
def handle_command(body, ack, client, logger):
    logger.info(body)
    ack()

    res = client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
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
					{
						"text": {
							"type": "plain_text",
							"text": "DNC"
						},
						"value": "621073710421"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "DEMO1"
						},
						"value": "DEMO1xxxxxx"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "DEMO2"
						},
						"value": "DEMO2xxxxxxx"
					}
				]
			},
			"label": {
				"type": "plain_text",
				"text": "Onramp Clients"
			}
		}
                ],
        },
    )
    logger.info(res)

    
    
# Step 4: The path that allows for your server to receive information from the modal sent in Slack
@app.view("gratitude-modal")
def view_submission(ack, body, client, logger, say):
    ack()
    cloudreach_client_records = "C03AGA96W87"    
    logger.info(body["view"]["state"]["values"])
    
    global user_text_7
    user_text_7 = body["view"]["state"]["values"]["my_block_8"]["static_select-action"]["selected_option"]["value"]
    user_text_7_text = body["view"]["state"]["values"]["my_block_8"]["static_select-action"]["selected_option"]["text"]["text"]
    
    say(blocks= [{"type": "divider"}],channel=cloudreach_client_records)
    client.chat_postMessage(channel=cloudreach_client_records, text="*Please select your option for retrive your client's data*")
    client.chat_postMessage(channel=cloudreach_client_records, text=":hotel: Client Name: "+user_text_7_text)
    client.chat_postMessage(channel=cloudreach_client_records, text=":pouch: AWS Acc number: "+user_text_7+ "\n")
    say(
        blocks=[
                
        {
          "type": "divider"
                            }],channel=cloudreach_client_records)
    say(":bell: *Select an Option :* ",channel=cloudreach_client_records)
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
			},{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "Client "+user_text_7_text+"- IAM user list"
				},
				"accessory": {
					"type": "button",
					"action_id": "button_click_6",
					"text": {
						"type": "plain_text",
						# "emoji": true,
						"text": "IAM"
					},
					"value": "click_me_123"
				}
			},
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
        ],channel="C03AGA96W87"
    )
    return user_text_7


# ---------------------------button click continue-------------------------

@app.action("button_click_4")
def action_button_click(ack, say ):
    ack()
    
    print(user_text_7)
    # support link https://www.youtube.com/watch?v=sbsVhX-9gSQ&t=516s
    URL = f"https://ponoldokvg.execute-api.eu-west-2.amazonaws.com/default/sts-assume-execution?id={user_text_7}"
    headers = {"Contenet-Type": "application/json"}
    r = requests.request("POST", URL, headers=headers)
    say(":open_file_folder:----S3 BUCKET LIST----")
    say(r.text)
    

@app.action("button_click_5")
def action_button_click(ack, say ):
    ack()
    print(user_text_7)
    URL = f"https://kqp6dc995l.execute-api.eu-west-2.amazonaws.com/default/sts_exce_ec2_list?id={user_text_7}"
    headers = {"Contenet-Type": "yourstage/yourpath"}
    r = requests.request("POST", URL, headers=headers)
    say(":computer:----EC2 LIST----")
    say(r.text)
    

@app.action("button_click_6")
def action_button_click(ack, say ):
    ack()
    print(user_text_7)
    URL = f"https://p50flvjdtj.execute-api.eu-west-2.amazonaws.com/default/sts_ecxe_iam_users?id={user_text_7}"
    headers = {"Contenet-Type": "yourstage/yourpath"}
    r = requests.request("POST", URL, headers=headers)
    say(":busts_in_silhouette:----IAM USER LIST----")
    say(r.text)
    

@app.action("button_click_7")
def action_button_click(ack, say ):
    ack()
    print(user_text_7)
    URL = f"https://fypexur15c.execute-api.eu-west-2.amazonaws.com/default/sts_exec_assume_role_info?id={user_text_7}"
    headers = {"Contenet-Type": "yourstage/yourpath"}
    r = requests.request("POST", URL, headers=headers)
    say(":bust_in_silhouette:----ASSUME ROLE INFO----")
    say(r.text)
    

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()


