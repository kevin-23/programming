import boto3
import time

# Connect to SQS service
client = boto3.client("sqs")

# Counters
counter = 0
counter2 = 0

# Assigns the tags to the queues. The queue is identified by the URL
def tagQueue(url):
    client.tag_queue(
        QueueUrl=url,
        Tags={
            "VantaOwner": "rmarin@vozy.co",
            "VantaDescription": "File of events ingested by the call campaigns handled by the log queue",
            "VantaContainsUserData": "true",
            "VantaUserDataStored": "User emails and phone numbers",
        },
    )


# Gets the URL of the queue
def getSQSUrl():

    global counter, counter2

    response = client.list_queues(QueueNamePrefix="cqm", MaxResults=60)

    for sqsurl in response["QueueUrls"]:
        response2 = client.get_queue_attributes(
            QueueUrl=sqsurl, AttributeNames=["CreatedTimestamp"]
        )

        response2 = int(response2["Attributes"]["CreatedTimestamp"])
        yearCreationTime = time.strftime("%Y", time.gmtime(response2))
        monthCreationTime = time.strftime("%m", time.gmtime(response2))
        dayCreationTime = time.strftime("%d", time.gmtime(response2))
        counter2 += 1

        if int(yearCreationTime) >= 2022:
            if int(monthCreationTime) >= 7:
                if int(dayCreationTime) >= 2:
                    tagQueue(sqsurl)
                    counter += 1


getSQSUrl()
print(
    f"Se obtuvieron {counter2} colas que inician con la palabra cqm.\n\
Y se agregaron los tags a {counter} colas."
)
