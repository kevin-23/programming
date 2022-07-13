import boto3
import json


def lambda_handler(event, context):

    ASGName = ""

    client = boto3.client("autoscaling")

    client.update_auto_scaling_group(
        AutoScalingGroupName=ASGName, MinSize=0, DesiredCapacity=0
    )

    # TODO implement
    return {
        "statusCode": 200,
        "body": f"EC2 instances associated with the {ASGName} ASG shut down.",
    }
