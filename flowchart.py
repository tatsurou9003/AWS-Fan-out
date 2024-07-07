from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import SNS, SQS

with Diagram("Lambda SNS SQS Fanout", show=True):
    publisher = Lambda("Publisher Lambda")
    sns_topic = SNS("SNS Topic")
    queue1 = SQS("SQS Queue 1")
    queue2 = SQS("SQS Queue 2")
    lambda1 = Lambda("Lambda Function 1")
    lambda2 = Lambda("Lambda Function 2")

    publisher >> sns_topic
    sns_topic >> queue1 >> lambda1
    sns_topic >> queue2 >> lambda2
