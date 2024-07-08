import os
from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_sqs as sqs,
    aws_lambda_event_sources as event_sources,
)
from constructs import Construct

class AwsFanoutStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account_id = os.getenv["AWS_ACCOUNT_ID"]
        region = os.getenv["AWS_REGION"]

        sns_topic = sns.Topic(
            self, "SNSTopic",

        )

        queue1 = sqs.Queue(
            self, "Queue1",
            # 可視性タイムアウト　→　visibility_timeout=Duration.seconds(300),
        )

        queue2 = sqs.Queue(
            self, "Queue2",
        )
        
        # SQSキューをそれぞれSNSのSubscriberとして設定
        sns_topic.add_subscription(subscriptions.SqsSubscription(queue1))
        sns_topic.add_subscription(subscriptions.SqsSubscription(queue2))
        
        # PublisherとなるLambda関数
        publisher_lambda = lambda_.Function(
            self, "PublisherLambda",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="publisher.lambda_publisher",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                'TOPIC_ARN': f'arn:aws:sns:{region}:{account_id}:SNSTopic'
            }
        )
        
        # Lambda関数にSNSのPublish権限を付与
        sns_topic.grant_publish(publisher_lambda)


        # SQSキューのSubscriberとなるLambda関数
        subscriber_lambda1 = lambda_.Function(
            self, "SubscriberLambda1",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="subscriber.lambda_subscriber1",
            code=lambda_.Code.from_asset("lambda"),
            timeout=Duration.seconds(10)
        )

        subscriber_lambda2 = lambda_.Function(
            self, "SubscriberLambda2",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="subscriber.lambda_subscriber2",
            code=lambda_.Code.from_asset("lambda"),
            timeout=Duration.seconds(10)
        )
        
        # Lambda関数をそれぞれSQSキューのSubscriberとして設定
        subscriber_lambda1.add_event_source(event_sources.SqsEventSource(queue1))
        subscriber_lambda2.add_event_source(event_sources.SqsEventSource(queue2))




