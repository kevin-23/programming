import boto3

client = boto3.client('cloudwatch')

def getCLXActions():

    paginator = client.get_paginator('describe_alarms')
    response_iterator = paginator.paginate(AlarmNamePrefix='CLX',
                                           PaginationConfig={'MaxItems': 462})

    for alarm in response_iterator:
        for x in range(len(alarm['MetricAlarms'])):
            cond1 = 'arn:aws:sns:us-east-1:808378037958:Slack_infra_Vozy_Ok'
            cond2 = alarm['MetricAlarms'][x]['OKActions']

            if cond1 not in cond2:
                print(alarm['MetricAlarms'][x]['AlarmName'])

getCLXActions()
