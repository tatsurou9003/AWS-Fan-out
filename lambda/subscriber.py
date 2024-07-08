def lambda_subscriber1(event, context):
    for record in event['Records']:
        print(f"Queue 1: {record['body']}")

def lambda_subscriber2(event, context):
    for record in event['Records']:
        print(f"Queue 2: {record['body']}")
