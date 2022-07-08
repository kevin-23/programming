import boto3

# Enter parameters
ipCGW = input(
    str('~~~ Customer Gataway parameters ~~~\nEnter Customer Gateway IPv4: '))
nameCGW = input(str('Enter Customer Gateway Name: '))

# Keys variables
customerGWId = ''

# This function creates a customer gateway
def cgw(ipCGW, nameCGW):

    global customerGWId

    client = boto3.client('ec2')

    # Customer Gateway Options
    response = client.create_customer_gateway(
        BgpAsn=65000,
        Type='ipsec.1',
        IpAddress=ipCGW,
        TagSpecifications=[
            {
                'ResourceType': 'customer-gateway',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': nameCGW
                    },
                ]
            },
        ],
    )

    customerGWId = response['CustomerGateway']['CustomerGatewayId']

'''
def vpnConnection(nameCGW)
    response = client.create_vpn_connection(
        CustomerGatewayId=nameCGW,
        Type='string',
        VpnGatewayId='vgw-00f29de9944746ae3',
        Options={
            'StaticRoutesOnly': True,
        }
    )
'''

cgw(ipCGW, nameCGW)
