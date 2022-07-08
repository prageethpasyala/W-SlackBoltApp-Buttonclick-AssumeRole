import json
import urllib3

def geolocation(public_ip, username, endpoint):
	http = urllib3.PoolManager()
	url = "http://ipinfo.io/"+ public_ip
	response = http.request('GET', url, retries = False)
	data = json.loads(response.data)
	data["endpoint"] = endpoint
	data["username"] = username
	print(data)
	return True 
    
def lambda_handler(event, context):
	allow = False
	error_msg = "User Authentication Failed"
	public_ip = event['public-ip']
	username = event['username']
	endpoint_id = event['endpoint-id']
	allow = geolocation(public_ip, username, endpoint_id)
	return {
		"allow": allow,
		"error-msg-on-failed-posture-compliance": error_msg,
		"posture-compliance-statuses": [],
		"schema-version": "v1"
	}	


    # https://aws.amazon.com/blogs/media/cs-automate-detecting-geolocation-of-client-vpn-users-lambda-function/