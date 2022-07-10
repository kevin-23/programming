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
tunnel1 = ''
tunnel2 = ''
psk1 = ''
psk2 = ''
tunnelsOptions = {
    'Phase1LifetimeSeconds': 28800,
    'Phase2LifetimeSeconds': 3600,
    'DPDTimeoutAction': 'clear',
    'StartupAction': 'add',
    'Phase1EncryptionAlgorithms': [{'Value': 'AES256'}],
    'Phase2EncryptionAlgorithms': [{'Value': 'AES256'}],
    'Phase1IntegrityAlgorithms': [{'Value': 'SHA1'}],
    'Phase2IntegrityAlgorithms': [{'Value': 'SHA1'}],
    'Phase1DHGroupNumbers': [{'Value': 2}],
    'Phase2DHGroupNumbers': [{'Value': 2}],
    'IKEVersions': [{'Value': 'ikev1'}]
}

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
    print('\nCreating Customer Gateway...')
    time.sleep(15)

    vpnConnection(nameVPN, staticRoutes)

# This function creates a VPN S2S
def vpnConnection(nameVPN, staticRoutes):

    global vpnId, tunnel1, tunnel2, psk1, psk2

    client = boto3.client('ec2')

    # VPN S2S Options
    response = client.create_vpn_connection(
        CustomerGatewayId=customerGWId,
        Type='ipsec.1',
        VpnGatewayId='vgw-0cf5449a328cd3e40',
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

    # Get VPN id, outside ip address and psk
    vpnId = response['VpnConnection']['VpnConnectionId']
    tunnel1 = response['VpnConnection']['Options']['TunnelOptions'][0]['OutsideIpAddress']
    tunnel2 = response['VpnConnection']['Options']['TunnelOptions'][1]['OutsideIpAddress']
    psk1 = response['VpnConnection']['Options']['TunnelOptions'][0]['PreSharedKey']
    psk2 = response['VpnConnection']['Options']['TunnelOptions'][1]['PreSharedKey']

    # Modify the static rotues
    client.create_vpn_connection_route(
        DestinationCidrBlock=staticRoutes,
        VpnConnectionId=vpnId
    )

    print('Creating VPN S2S... Please wait a few minutes.')
    time.sleep(300)

    # Modify the tunnel optoons
    print('Modifying the tunnels.')
    client.modify_vpn_tunnel_options(
        VpnConnectionId=vpnId,
        VpnTunnelOutsideIpAddress=tunnel1,
        TunnelOptions=tunnelsOptions
    )
    
    time.sleep(210)

    client.modify_vpn_tunnel_options(
        VpnConnectionId=vpnId,
        VpnTunnelOutsideIpAddress=tunnel2,
        TunnelOptions=tunnelsOptions
    )


# Call cgw function to create CGW and VPN S2S
cgw(ipCGW, nameCGW)

# Print the results
print(f'\nVPN S2S successfully created, relevant values:\nTunnel 1: {tunnel1}\
    \nTunnel 2: {tunnel2}\
    \nPSK 1: {psk1}\
    \nPSK 2: {psk2}\
    \nPerfect Forward Secrecy: Yes\
    \nDiffie-Hellman Group (DH): 2')
