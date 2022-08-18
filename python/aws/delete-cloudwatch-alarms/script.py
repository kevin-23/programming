import boto3
import botocore

# Function to delete CloudWatch alarm
def delete_cw_alarm(alarmName):

    # Connect to specific service
    client = boto3.client('cloudwatch')

    # Delete the CloudWatch alarm
    client.delete_alarms(
        AlarmNames=[
            alarmName,
        ]
    )

# Function to check if an instance ec2 exists
def check_if_instance_ec2_exists(instanceId):

    # Connect to specific service
    client = boto3.client('ec2')

    # Search for the instance
    try:
        client.describe_instance_status(
            InstanceIds=[
                instanceId
                ],
        )
        return False
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidInstanceID.NotFound':
            return True

# Main function
def search_insufficient_data_alamrs(prefix):

    # Connect to specific service
    client = boto3.client('cloudwatch')
    paginator = client.get_paginator('describe_alarms')

    # Get all alarms with Insufficient Data
    response = paginator.paginate(
        AlarmNamePrefix=prefix,
        StateValue='INSUFFICIENT_DATA',
        PaginationConfig={
            'MaxItems': 500
        }
    )

    for alarm in response:
        for l in range(len(alarm['MetricAlarms'])):
            alarmName = alarm['MetricAlarms'][l]['AlarmName']
            for m in range(len(alarm['MetricAlarms'][l]['Dimensions'])):
                dimensionName = alarm['MetricAlarms'][l]['Dimensions'][m]['Name']
                if dimensionName == 'InstanceId':
                    dimensionValue = alarm['MetricAlarms'][l]['Dimensions'][m]['Value']
                    instanceExistsOrNot = check_if_instance_ec2_exists(dimensionValue)
                    if instanceExistsOrNot == True:
                        delete_cw_alarm(alarmName)

search_insufficient_data_alamrs('Vozy')