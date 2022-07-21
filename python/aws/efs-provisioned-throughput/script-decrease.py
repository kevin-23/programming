import boto3

client = boto3.client('efs')
fs = 'fs-0b13c3d1e2f948138'
newMB = float(20)

def decreaseMBProvisioned():

    response = client.describe_file_systems(
        FileSystemId = fs)

    MBProvisioned = response['FileSystems'][0]['ProvisionedThroughputInMibps']

    if int(MBProvisioned) >= 21:
        response2 = client.update_file_system(
            FileSystemId = fs,
            ProvisionedThroughputInMibps = newMB)

decreaseMBProvisioned()
