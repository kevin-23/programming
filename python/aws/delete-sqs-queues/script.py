import boto3
import time

# Connect to SQS service
client = boto3.client("sqs")

# Counters
counter = 0

# Assigns the tags to the queues. The queue is identified by the URL
def deleteQueue(url):
    
    global counter 

    try:
        client.delete_queue(
            QueueUrl=url
            )
        counter += 1
    except:
        print('ERROR DELETING')
        print(f"Se eliminaron {counter} colas.")

# Gets the URL of the queue
def getSQSUrl():

    prefix = "callhandler_dc4057af-8f97-4e6d-9429-84a77f4aa330"

    try:
        response = client.list_queues(QueueNamePrefix=prefix, MaxResults=1000)

        for sqsurl in response["QueueUrls"]:
            deleteQueue(sqsurl)
    except:
        print('It is not possible retrive a queue with this prefix: {prefix}')

getSQSUrl()
print(f"Se eliminaron {counter} colas.")
