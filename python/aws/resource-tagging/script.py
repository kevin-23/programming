import boto3

client = boto3.client("ec2")

def tagResourceWithName(resourceId, instanceId):
    client.create_tags(
        Resources=[
            resourceId,
        ],
        Tags=[
            {
                'Key': 'Name',
                'Value': instanceId
            },
            {
                'Key': 'environment',
                'Value': 'dev'
            },
        ]
    )

def tagResourceWithoutName(resourceId):
    client.create_tags(
        Resources=[
            resourceId,
        ],
        Tags=[
            {
                'Key': 'environment',
                'Value': 'dev'
            },
        ]
    )

def getElasticIP(eip, name):
    try:
        response = client.describe_addresses(
        PublicIps=[
            eip
            ]
        )

        allocationId = response['Addresses'][0]['AllocationId']
        tagResourceWithName(allocationId, name)
    except:
        print(f'The {eip} does not exists.')

def getResource():
    response = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:environment',
                'Values': [
                    'dev',
                ]
            },
        ],
        MaxResults=120,
    )
    numberTag = response['Reservations']
    for n in range(len(numberTag)):
        nameTag = response['Reservations'][n]['Instances'][0]['Tags']
        numberEBS = response['Reservations'][n]['Instances'][0]['BlockDeviceMappings']
        numberNIC = response['Reservations'][n]['Instances'][0]['NetworkInterfaces']
        for tag in nameTag:
            if tag['Key'] == 'Name':
                for x in range(len(numberEBS)):
                    volumeId = response['Reservations'][n]['Instances'][0]['BlockDeviceMappings'][x]['Ebs']['VolumeId']
                    tagResourceWithName(volumeId, f'{tag["Value"]}')
                for m in range(len(numberNIC)):
                    ipAllocationId = response['Reservations'][n]['Instances'][0]['NetworkInterfaces'][m]['Association']['PublicIp']
                    getElasticIP(ipAllocationId, f'{tag["Value"]}')
                       
getResource()