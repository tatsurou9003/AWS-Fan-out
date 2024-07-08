def handler1(event, context):
    for record in event['Records']:
        print(f"Queue 1: {record['body']}")

def handler2(event, context):
    for record in event['Records']:
        print(f"Queue 2: {record['body']}")
