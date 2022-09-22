# Libraries
import boto3

# Changing variables, only accept one tag
# You can adds more tags for the resources. Modifying the tagResourceWithName function
searchInstancesKey = 'tag:environment'
searchInstancesValue = 'staging'

taggingResourceKey = 'environment'
taggingResourceValue = 'staging'

# Connecting EC2 service
client = boto3.client("ec2")

# Tagging function
def tagResourceWithName(resourceId, instanceId):

    # Execute the API request
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
                'Key': taggingResourceKey,
                'Value': taggingResourceValue
            },
        ]
    )

# Getting elastic IP
def getElasticIP(eip, name):

    # Execute the API request only if it is successful
    try:
        response = client.describe_addresses(
        PublicIps=[
            eip
            ]
        )

        # Saves the elastic IP in a variable
        allocationId = response['Addresses'][0]['AllocationId']

        # This loop calls the tagResourceWithName function to tag the elastic IP
        tagResourceWithName(allocationId, name)
        print(f'The elastic IP of the instance was tagged: {name}')

    # Print a text if the tagging is unsuccessful
    except:
        print(f'The {eip} does not exists.\n')

# Getting resource id, this is the main function
def getResource():

    # Execute the API request
    paginator = client.get_paginator('describe_instances')
    response = paginator.paginate(
        Filters=[
            {
                'Name': searchInstancesKey,
                'Values': [
                    searchInstancesValue
                ]
            }
        ],
        PaginationConfig={
            'MaxItems': 122,
            }
        )

    # This loop reads all retrieved instances
    for page in response:
        numberTag = page['Reservations']
        print(f'~~~ SE OBTUVIERON {len(numberTag)} INSTANCIAS ~~~')
        
        # This loop retrieves all instances tags, block devices and NICs
        for n in range(len(numberTag)):
            nameTag = page['Reservations'][n]['Instances'][0]['Tags']
            numberEBS = page['Reservations'][n]['Instances'][0]['BlockDeviceMappings']
            numberNIC = page['Reservations'][n]['Instances'][0]['NetworkInterfaces']
            
            # This loop retrieves the instance names
            for tag in nameTag:
                if tag['Key'] == 'Name':
                    
                    # This loop calls the tagResourceWithName function to tag the NICs
                    for m in range(len(numberNIC)):
                        try:
                            ipAllocationId = page['Reservations'][n]['Instances'][0]['NetworkInterfaces'][m]['NetworkInterfaceId']
                            print(f'\nSe tagueo la NIC {ipAllocationId} de la instancia: {tag["Value"]}')
                            tagResourceWithName(ipAllocationId, f'{tag["Value"]}')
                        except:
                            print(f"Validar la NIC \
{page['Reservations'][n]['Instances'][0]['NetworkInterfaces'][0]['NetworkInterfaceId']} \
de la instancia {tag['Value']} ya que no se pudo taguear\n")

                    # This loop calls the getElasticIP function to search a elastic IP
                    for m in range(len(numberNIC)):
                        try:
                            ipAllocationId = page['Reservations'][n]['Instances'][0]['NetworkInterfaces'][m]['Association']['PublicIp']
                            getElasticIP(ipAllocationId, f'{tag["Value"]}')
                        except:
                            print(f"La NIC \
{page['Reservations'][n]['Instances'][0]['NetworkInterfaces'][0]['NetworkInterfaceId']} no tiene IP elastica")

                    # This loop calls the tagResourceWithName function to tag the EBS volumes
                    for x in range(len(numberEBS)):
                        volumeId = page['Reservations'][n]['Instances'][0]['BlockDeviceMappings'][x]['Ebs']['VolumeId']
                        tagResourceWithName(volumeId, f'{tag["Value"]}')
                        print(f'Se tagueo el EBS de la instancia: {tag["Value"]}')

# Call the main function
getResource()
