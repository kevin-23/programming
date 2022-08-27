#
# Environment variables
# INCREASE_THRESHOLD = intenger GB
# VOLUMEX = {"name": "VOLUMEX", "id": "volume id", "threshold": integer GB, "path": "Script path"}
#

import boto3
import json
import os

# Connect to EC2 service
client = boto3.client('ec2')

def edit_env_value(name, threshold):

    # Modify json
    with open("env.json", "r") as jsonFile:
        data = json.load(jsonFile)

    increaseThreshold = data['INCREASE_THRESHOLD']
    data[name]['threshold'] = threshold+increaseThreshold

    with open("env.json", "w") as jsonFile:
        json.dump(data, jsonFile)

# Execute resize script
def execute_rezise_script(volumeId, instanceId, path, name, threshold):
    try:
        ssmClient = boto3.client('ssm')
        ssmClient.send_command(
            Targets = [
                {
                    'Key': 'InstanceIds',
                    'Values': [
                        instanceId,
                    ]
                },
            ],
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': 
                [f'sh {path}']
                }
            )

        edit_env_value(name, threshold)
        return f'The volume {volumeId} has been successfully updated'
    except:
        return 'Error executing the increase_ebs_size function'
        
# Get the volume parameters
def get_volume_parameters(volumeId, threshold, path, name):
    try:
        response = client.describe_volumes(
            VolumeIds=[
                volumeId
            ]
        )
        currentSize = response['Volumes'][0]['Size']
        currentState = response['Volumes'][0]['State']
        instanceId = response['Volumes'][0]['Attachments'][0]['InstanceId']

        if currentSize >= threshold:
            if currentState == 'in-use' or currentState == 'available':
                return execute_rezise_script(volumeId, instanceId, path, name, threshold)
        else:
            return f'Volume size {volumeId} is {currentSize} GB'

    except:
        return f'The volume {volumeId} was not upgrade, check that the volume id exists and that they are separated by comma'

# Main function
def main():

    results = []
    envs = []
    counter = 1
    
    try: 
        while True:
            with open("env.json", "r") as jsonFile:
                data = json.load(jsonFile)
            envs.append(data[f'VOLUME{counter}'])
            counter += 1
    except:
        pass
        
    for resource in envs:
        results.append(get_volume_parameters
            (
                resource['id'],
                resource['threshold'],
                resource['path'],
                resource['name']
            )
        )
        
    log = f'\n`touch ./log.txt` echo "Last execution: `date` \n{results}" >> ./log.txt'
    os.system(log)

main()
