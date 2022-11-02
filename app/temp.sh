#!/bin/bash



TASK_ID=`aws ecs list-tasks --desired-status "RUNNING" --cluster "SlackBot-Assume-App" | grep arn | sed 's/[ "]//g'`
AWS_PAGER="" aws ecs stop-task --cluster "SlackBot-Assume-App" --task $TASK_ID --reason "Restarting task due to new ECR image deployment"




