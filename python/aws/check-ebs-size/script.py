#
# Environment Variables
# ADDGB = Add GB to current size
# SIZEOVER = Base size less than or equal to the current size to decide whether to resize.
# VOLUMEIDS = Ids of EBS volumes
#

import botocore
import boto3
import json
import os

# Connect to EC2 service
client = boto3.client('ec2')

# Increase EBS size
def increase_ebs_size(volumeId, currrentSize):
    try:
        client.modify_volume(
            VolumeId=volumeId,
            Size=currrentSize+os.environ['ADDGB']
        )  
        return f'The volume {volumeId} has been successfully updated, its new size is {currrentSize+os.environ["ADDGB"]}'
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'VolumeModificationRateExceeded':
            return f'The volume {volumeId} was modified less than 6 hours ago'
        elif error.response['Error']['Code'] == 'IncorrectModificationState':
            return f'The volume {volumeId} is not in a state available for modification'        
        else:
            return 'Unknown error executing the increase_ebs_size function'
        
# Get the volume parameters
def get_volume_parameters(volumeId):
    try:
        response = client.describe_volumes(
            VolumeIds=[
                volumeId
            ]
        )
        currentSize = response['Volumes'][0]['Size']
        currentState = response['Volumes'][0]['State']
        
        if currentSize <= os.environ['SIZEOVER']:
            if currentState == 'in-use' or currentState == 'available':
                return increase_ebs_size(volumeId, currentSize)
        else:
            return f'Volume size {volumeId} is {currentSize} GB'

    except:
        return f'The volume {volumeId} was not upgrade, check that the volume id exists and that they are separated by comma'

# Main function
def main(event, context):

    results = []

    volumeIds = os.environ['VOLUMEIDS']
    for id in volumeIds.rsplit(","):
        results.append(get_volume_parameters(id.replace(" ", "")))

    print({
        'statusCode': 200,
        'body': json.dumps(results)
    })
        
main()