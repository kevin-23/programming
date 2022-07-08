import boto3
import time

# Enter parameters
nameCGW = input(
    str('~~~ Customer Gataway parameters ~~~\nEnter Customer Gateway Name: '))
ipCGW = input(str('Enter Customer Gateway IPv4: '))

nameVPN = input(str('\n~~~ VPN S2S parameters ~~~\nEnter VPN Name: '))
staticRoutes = input(str(
    'Enter a Static Route IPv4. The CIDR block associated with the local subnet of the customer network: '))

# Keys variables
customerGWId = ''
vpnId = ''

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
    print('\nCreating Customer Gateway... Please wait.')
    time.sleep(15)

    vpnConnection(nameVPN, staticRoutes)

# This function creates a VPN S2S
def vpnConnection(nameVPN, staticRoutes):

    global vpnId

    client = boto3.client('ec2')

    # VPN S2S Options
    response = client.create_vpn_connection(
        CustomerGatewayId=customerGWId,
        Type='ipsec.1',
        VpnGatewayId='vgw-00f29de9944746ae3',
        Options={
            'StaticRoutesOnly': True,
        },
        TagSpecifications=[
            {
                'ResourceType': 'vpn-connection',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': nameVPN
                    }
                ]
            }
        ]
    )
    vpnId = response['VpnConnection']['VpnConnectionId']
    print('Creating VPN S2S... Please wait.')
    time.sleep(15)

    # Add static route
    client.create_vpn_connection_route(
        DestinationCidrBlock=staticRoutes,
        VpnConnectionId=vpnId
    )


cgw(ipCGW, nameCGW)