import boto3
import time
import json

# Variables
IPS = []
ASG_NAME = ''

# Get the ip state
def state_and_associate_ip(eni):

    # Connect to EC2 service
    client = boto3.client('ec2')
    
    # Search for an available elastic ip
    for ip in IPS:
        response = client.describe_addresses(
        PublicIps=[
            ip,
        ]
    )   
        # Validates if the elastic ip is available
        try: 
            associationId = response['Addresses'][0]['AssociationId']
            
        except:
            print ('Waiting for the correct state of the instance to attach the EIP')
            time.sleep(40)
            allocationId = response['Addresses'][0]['AllocationId']
            client.associate_address(
                AllocationId=allocationId,
                NetworkInterfaceId=eni,
            )
            
            return {"body": f"The IP {ip} was successfully attached to this ENI: {eni}"}
            

# Get the instance state
def get_ip_nic(instanceId):

    # Connect to EC2 service
    client = boto3.client('ec2')

    # Search the nic with a public ip
    response = client.describe_network_interfaces(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [
                instanceId,
                ]
            }
        ]
    )

    # Gets the network interface to attach the eip
    for x in range(len(response['NetworkInterfaces'])):
        if response['NetworkInterfaces'][x]['Attachment']['DeviceIndex'] == 0:
            eniId = response['NetworkInterfaces'][x]['NetworkInterfaceId']
            state_and_associate_ip(eniId)
            break
            

# Get the instance id
def lambda_handler(event, context):

    # Connect to ASG service
    client = boto3.client('autoscaling')

    # Describes the ASG
    response = client.describe_auto_scaling_groups(
        AutoScalingGroupNames=[
            ASG_NAME
        ]
    )

    # Gets all instance ids
    instances = response['AutoScalingGroups'][0]['Instances']
    for x in range (len(instances)):
        instanceState = instances[x]["LifecycleState"]
        # Validates if it is necessary to call the function get_ip_nic
        if instanceState == 'Pending' or instanceState == 'Wait':
            instanceId = instances[x]["InstanceId"]
            get_ip_nic(instanceId)
            return {"body": f"The script was executed successfully"}