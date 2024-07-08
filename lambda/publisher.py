import os
import json
import boto3

sns = boto3.client('sns')
TOPI_ARN = os.getenv('TOPIC_ARN')

def lambda_publisher(event, context):
    message = {
        'default': 'Hello from Lambda Publisher!'
    }
    response = sns.publish(
        TopicArn=TOPI_ARN,
        Message=json.dumps(message)
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Message published to SNS topic')
    }