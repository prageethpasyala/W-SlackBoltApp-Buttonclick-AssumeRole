<h1><b>SLACKBOT ASSUMEROLE APP</h1>

The Main task for this app is checking the connectivity of the client account after running the landing zone pipeline. Assume role and trust relationships between accounts will be created during the process of the migration. 
    This app contains 3 button options list from the remote account.
    1.  Call assume role info
    2.  Call the EC2 list
    3.  Call the S3 bucket list


![Alt text](assumerole.png?raw=true "Title")



<h2>installation</h2>
**Creating the virtual environment**
    sudo yum install python3 python3-venv

    mkdir .venv
    python3 -m venv .venv
    source .venv/bin/activate   (type "deactivate" to deactivate the env)

**Install all dependencies** 
    > pip install --upgrade pip
    > pip install slackclient slackeventsapi Flask
    > pip3 install boto3
    > pip3 install slack_bolt
    > python -m pip install requests
**Before dockersing the code required to create the requirement file**
    pip3 freeze > requirements.txt
**Create the Docker file in the root directory**
    Dockerfile
    ```
        FROM python:3.8

        <!-- Creating the working dir in the container -->
        WORKDIR /bolt-app       

        <!-- copying the requirment.txt file into the container -->
        COPY requirements.txt.

        <!-- Installing the dependencies via requirements file -->
        RUN pip install -r requirements.txt

        <!-- copying the local app folder to the root folder  -->
        COPY ./app ./app

        <!-- setting startup file to run -->
        CMD ["python", "./app/remotecall4L3-onramp.py"]


***When you test in the local docker container use the folowing steps (optional)***
    
    <!-- build docker image  -->
    docker build -t slackbot-gui-ecs .

    <!-- run the docker container -->
    docker run -it -e SLACK_APP_TOKEN=<SLACK-APP-TOKEN> \
    -e SLACK_BOT_TOKEN=<SLACK-BOT-TOKEN> \
    -e SLACK_SIGNING_SECRET=<SLACK-SIGNING-SECRET> \
    -t slackbot-gui-ecs

    

***when you need to push an image to aws ecr use the following steps***
    go back to root directory(come out from app folder if you are in)
    create a AWS ecr public repo 
    then follow the push commands to push your code and docker file
    copy the uri for the created image

***then create an ECS-SlackBot iam role with 4 policies (2 inline and 2 aws managed) which can have access to parameter store, cw logs etc..***
```
        Customer inline policy - slackbot-gui-cw-ddb ->
                    {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": "logs:CreateLogGroup",
                        "Resource": "arn:aws:logs:eu-west-2:<your-account-id>:*"
                    },
                    {
                        "Effect": "Allow",
                        "Action": [
                            "logs:CreateLogStream",
                            "logs:PutLogEvents"
                        ],
                        "Resource": "arn:aws:logs:eu-west-2:<your-account-id>:log-group:/aws/lambda/slackbot-gui:*"
                    },
                    {
                        "Effect": "Allow",
                        "Action": "dynamodb:*",
                        "Resource": "arn:aws:dynamodb:eu-west-2:<your-account-id>:table/onrampclient"
                    }
                ]
            }

        AmazonECSTaskExecutionRolePolicy ->
                            {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Action": [
                                "ecr:GetAuthorizationToken",
                                "ecr:BatchCheckLayerAvailability",
                                "ecr:GetDownloadUrlForLayer",
                                "ecr:BatchGetImage",
                                "logs:CreateLogStream",
                                "logs:PutLogEvents"
                            ],
                            "Resource": "*"
                        }
                    ]
                }

        AmazonSSMReadOnlyAccess ->
                {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": [
                            "ssm:Describe*",
                            "ssm:Get*",
                            "ssm:List*"
                        ],
                        "Resource": "*"
                    }
                ]
            }

    Customer inline policy - slackParamaterStoreAccess ->
            {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Action": [
                                "secretsmanager:GetSecretValue",
                                "ssm:GetParameters",
                                "kms:Decrypt"
                            ],
                            "Resource": [
                                "arn:aws:ssm:eu-west-2:<your-account-id>:parameter/SLACK_APP_TOKEN",
                                "arn:aws:ssm:eu-west-2:<your-account-id>:parameter/SLACK_BOT_TOKEN",
                                "arn:aws:ssm:eu-west-2:<your-account-id>:parameter/SLACK_SIGNING_SECRET"
                            ]
                        }
                    ]
                }

```
***create the ECR and push files to the repo***
        aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.eu-west-2.amazonaws.com
        docker build -t <cluster-name> .                                                                                                      
        docker tag slackbot-gui:latest <your-account-id>.dkr.ecr.eu-west-2.amazonaws.com/<cluster-name>:latest  
        docker push <your-account-id>.dkr.ecr.eu-west-2.amazonaws.com/<cluster-name>:latest                                                        


***create ECS cluster -  fargate - add ECS-SlackBot role***
***create a fargate task definition***
    Attached the created role ECS-SlackBot and ECR repo image uri - ref:(https://www.youtube.com/watch?v=-Vsuzi4OByY&ab_channel=DenysonData)
    run the task - make sure your sg inbound configured to 80

    Run the task 
    CLI command for stopping a running task
        aws ecs stop-task --cluster "Slackbot-gui" --task "84c5a8610c7b4cf8b8ae6db1a13cf1fe" --region "eu-west-2"
            Note: command will not work for an inactive task

