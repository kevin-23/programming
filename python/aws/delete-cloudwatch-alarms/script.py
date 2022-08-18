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

    # Get all alarms with Insufficient Data
    response = client.describe_alarms(
        AlarmNamePrefix=prefix,
        StateValue='INSUFFICIENT_DATA',
        MaxRecords=3
    )

    # Get the instance id, check if the instance exist and delete the CW alarm
    for x in range(len(response['MetricAlarms'])):
        for l in range(len(response['MetricAlarms'][x]['Dimensions'])):
            alarmName = response['MetricAlarms'][x]['AlarmName']
            dimensionName = response['MetricAlarms'][x]['Dimensions'][l]['Name']
            if dimensionName == 'InstanceId':
                dimensionValue = response['MetricAlarms'][x]['Dimensions'][l]['Value']
                instanceExistsOrNot = check_if_instance_ec2_exists(dimensionValue)
                if instanceExistsOrNot == True:
                   delete_cw_alarm(alarmName)

search_insufficient_data_alamrs('Vozy')