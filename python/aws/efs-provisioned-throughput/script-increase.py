import boto3

client = boto3.client('efs')
fs = 'fs-08c8702eaa463570a'
addMB = 20

def increaseMBProvisioned():

    response = client.describe_file_systems(
        FileSystemId = fs)

    MBProvisioned = response['FileSystems'][0]['ProvisionedThroughputInMibps']

    newMB = int(MBProvisioned) + int(addMB)

    response2 = client.update_file_system(
        FileSystemId = fs,
        ProvisionedThroughputInMibps = float(newMB))

increaseMBProvisioned()
