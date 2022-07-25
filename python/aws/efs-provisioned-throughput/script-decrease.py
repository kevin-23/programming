import boto3

client = boto3.client('efs')
fs = 'fs-0be0dacecc7e251d5'
newMB = float(15)

def decreaseMBProvisioned():

    response = client.describe_file_systems(
        FileSystemId = fs)

    MBProvisioned = response['FileSystems'][0]['ProvisionedThroughputInMibps']

    if int(MBProvisioned) >= 19:
        response2 = client.update_file_system(
            FileSystemId = fs,
            ProvisionedThroughputInMibps = newMB)

decreaseMBProvisioned()
