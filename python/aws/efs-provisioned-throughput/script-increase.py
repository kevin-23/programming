import boto3

client = boto3.client("efs")
fs = "fs-0b13c3d1e2f948138"
addMB = float(3)

def increaseMBProvisioned():

    response = client.describe_file_systems(FileSystemId=fs)
    MBProvisioned = response["FileSystems"][0]["ProvisionedThroughputInMibps"]
    newMB = int(MBProvisioned) + int(addMB)

    client.update_file_system(
        FileSystemId=fs, ProvisionedThroughputInMibps=float(newMB)
    )

increaseMBProvisioned()
