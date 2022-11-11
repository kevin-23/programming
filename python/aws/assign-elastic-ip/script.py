import os
import time
import boto3

# Get the ip state
def state_and_associate_ip(eni):
    
    # Variables
    IPS = os.environ['IPS']
    
    # Connect to EC2 service
    client = boto3.client('ec2')
    
    # Search for an available elastic ip
    for ip in IPS.rsplit(","):
        response = client.describe_addresses(
        PublicIps=[
            ip.replace("\t", "")
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
            
            return {"body": f"An IP was successfully attached to this ENI: {eni}"}
            

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
            result = state_and_associate_ip(eniId)
            return result

# Get the instance id
def lambda_handler(event, context):

    # Connect to EC2 service
    client = boto3.client('autoscaling')

    # Describes the ASG activities
    response = client.describe_scaling_activities(
    AutoScalingGroupName=os.environ['ASG_NAME'],
    MaxRecords=1
    )

    # Getting the instance id and the activity name
    text = response['Activities'][0]['Description']
    text = text.split(" ")
    if text[0] == "Launching":
        result = get_ip_nic(text[-1])
        return result