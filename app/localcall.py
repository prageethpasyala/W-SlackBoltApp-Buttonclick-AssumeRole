from cgitb import text
from distutils.command.clean import clean
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import boto3

# ec2 status information 
AWS_REGION = "eu-west-2"
EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)
instances = EC2_RESOURCE.instances.all()
for instance in instances:
    print(f'EC2 instance {instance.id}" information:')
    print(f'Instance state: {instance.state["Name"]}')
    print(f'Instance AMI: {instance.image.id}')
    print(f'Instance platform: {instance.platform}')
    print(f'Instance type: "{instance.instance_type}')
    print(f'Piblic IPv4 address: {instance.public_ip_address}')
    print('-'*60)



# Initializes your app with your bot token and socket mode handler
# app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Listens to incoming messages that contain "hello"
@app.message("hey")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    # say(f"Hey there <@{message['user']}>!")
	say(
		blocks=[
				{
				"type": "section",
				"text": {
					"type": "plain_text",
					# "emoji": true,
					"text": "Welcome to BotOnRamp Service:"
				}
			},
			{
				"type": "divider"
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					# "text": "*<fakeLink.toUserProfiles.com|Iris / Zelda 1-1>*\nTuesday, January 21 4:00-4:30pm\nBuilding 2 - Havarti Cheese (3)\n2 guests"
					"text" : f"*<fakeLink.toUserProfiles.com| EC2 instance id: {instance.id} information>* \n Instance state: {instance.state} \n Instance AMI: {instance.image.id} \n Instance platform: {instance.platform} \n Instance type: {instance.instance_type} \n Public IPv4 address: {instance.public_ip_address}" 
					
				},
				"accessory": {
					"type": "image",
					"image_url": "https://api.slack.com/img/blocks/bkb_template_images/notifications.png",
					"alt_text": "calendar thumbnail"
				}
			},
			{
				"type": "context",
				"elements": [
					{
						"type": "image",
						"image_url": "https://api.slack.com/img/blocks/bkb_template_images/notificationsWarningIcon.png",
						"alt_text": "notifications warning icon"
					},
					{
						"type": "mrkdwn",
						"text": "*CPU-High |  EC2-Id: ec0002323*"
					}
				]
			}
			
			]
			
		)
	say(
		blocks = [
			{
				"type": "divider"
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "*<fakeLink.toUserProfiles.com| Select an option:>*"
				}
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "*S3*\nList S3 Buckets"
				},
				"accessory": {
					"type": "button",
					"action_id": "button_click_1",
					"text": {
						"type": "plain_text",
						# "emoji": true,
						"text": "Choose"					
					},
					"value": "click_me_123"
				}
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "*IAM-2*\nFull detail list of UserID/Iam ARN/CreatedDate"
				},
				"accessory": {
					"type": "button",
					"action_id": "button_click_2",
					"text": {
						"type": "plain_text",
						# "emoji": true,
						"text": "Choose"
					},
					"value": "click_me_123"
				}
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "*IAM-1*\nShort list of all iam users"
				},
				"accessory": {
					"type": "button",
					"action_id": "button_click_3",
					"text": {
						"type": "plain_text",
						# "emoji": true,
						"text": "Choose"
					},
					"value": "click_me_123"
				}
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "*EC2*\nDetail list of all ec2 instances"
				},
				"accessory": {
					"type": "button",
					"action_id": "button_click_4",
					"text": {
						"type": "plain_text",
						# "emoji": true,
						"text": "Choose"
					},
					"value": "click_me_123"
				}
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "*<fakelink.ToMoreTimes.com|Show more times>*"
				}
			}
		]
	)

# access_key="AKIASZAXXD4DOTEQWFRS"
# secret_key="bwLqKBK6wA3MiF0qu+eqgMB0IcLazVbTDEqxA4h+"
# aws_access_key_id =  os.environ.get('aws_access_key_id')
# aws_secret_access_key = os.environ.get('aws_secret_access_key')

# say(f"<@{body['user']['id']}> clicked the button")
@app.action("button_click_1")
def action_button_click(body, ack, say):
    # Acknowledge the action
	say(":file_folder: *---- Existing buckets ----*")
	# s3 = boto3.client('s3',aws_access_key_id=os.environ.get('aws_access_key_id'),aws_secret_access_key=os.environ.get('aws_secret_access_key'))
	s3 = boto3.client('s3')
	response = s3.list_buckets()

	# Output the bucket names
	# print("*Existing buckets*")
	i=1
	for bucket in response['Buckets']:
		# print(f'  {bucket["Name"]}')
		ack()
		say(f"Bucket {i} : {bucket['Name']}")
		i=i+1
	say("\n")


@app.action("button_click_2")
def action_button_click(body, ack, say):
    # Acknowledge the action
	# iam = boto3.client('iam',aws_access_key_id=os.environ.get('aws_access_key_id'),aws_secret_access_key=os.environ.get('aws_secret_access_key'))
	iam = boto3.client('iam')
	say(":busts_in_silhouette: *---- Existing Users ----*")
	i=1
	for user in iam.list_users()['Users']:		
		ack()
		say(f":bust_in_silhouette: User{i}")		
		say(("User: {0}\nUserID: {1}\nARN: {2}\nCreatedOn: {3}\n".format(
		user['UserName'],
		user['UserId'],
		user['Arn'],
		user['CreateDate']
		)
		))
		i=i+1
	say("\n")

@app.action("button_click_3")
def action_button_click(body, ack, say):
    # Acknowledge the action
	# client = boto3.client('iam',aws_access_key_id=os.environ.get('aws_access_key_id'),aws_secret_access_key=os.environ.get('aws_secret_access_key')) 
	client = boto3.client('iam') 
	response = client.list_users()
	say(":busts_in_silhouette: *---- Existing Users ----*")
	i=1
	for x in response['Users']:
		# print (x['UserName']) 
		ack()
		say(f"User{i} : {x['UserName']}")
		i=i+1
	say("\n")

@app.action("button_click_4")
def action_button_click(body, ack, say):
    
	# ec2 status information 
	AWS_REGION = "eu-west-2"
	EC2_RESOURCE = boto3.resource('ec2', region_name=AWS_REGION)
	instances = EC2_RESOURCE.instances.all()
	say(":tv: *---- Existing EC2 instances ----*")
	i=1
	for instance in instances:
		ack()
		say(f":computer: Ec2{i}")
		say(f"EC2 instance : {instance.id}\n" f"Instance state: {instance.state}\n" f"Instance AMI: {instance.image.id}\n" f"Instance platform: {instance.platform}\n" f"Instance type: {instance.instance_type}\n" f"Public IPv4 address: {instance.public_ip_address}\n" )
    
		
		i=i+1
	say("\n")

	
	





# Start your app
if __name__ == "__main__":
	
    # SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
	SocketModeHandler(app, app_token=os.environ.get("SLACK_APP_TOKEN")).start()







    # https://slack.dev/bolt-python/tutorial/getting-started
            # run followign command to activate the virtual env
                #   python3 -m venv .venv
                #   source .venv/bin/activate
				#  pip install slack_bolt
				#   python3 -m pip install boto3
				# export slack & aws profile

    # type  heybolt

	# how to create docker file https://www.youtube.com/watch?v=bi0cKgmRuiA
    #  checking the image working locally 
	#  docker build -t bolt-app . 
	#  env > env_file && docker run --env-file .env bolt-app  


	# https://www.youtube.com/watch?v=h0Dk8K_ncp4
	# push docker image to ECR
	# aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 191175794438.dkr.ecr.eu-west-2.amazonaws.com
	# docker build -t bolt-app .
	# docker tag bolt-app:latest 191175794438.dkr.ecr.eu-west-2.amazonaws.com/bolt-app:latest
	# docker push 191175794438.dkr.ecr.eu-west-2.amazonaws.com/bolt-app:latest
	# aws ecs update-service --cluster bolt-app-cluster --service bolt-app-container-service --force-new-deployment --region eu-west-2 
	# create ECS container fargate with the image & open port 3000