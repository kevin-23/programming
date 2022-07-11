import boto3
import time

# Enter parameters
nameCGW = input(
    str("~~~ Customer Gataway parameters ~~~\nEnter Customer Gateway Name: ")
)
ipCGW = input(str("Enter Customer Gateway IPv4: "))

nameVPN = input(str("\n~~~ VPN S2S parameters ~~~\nEnter VPN Name: "))
staticRoutes = input(
    str(
        "Enter a Static Route IPv4. The CIDR block associated with the local subnet of the customer network: "
    )
)

# This function creates a customer gateway
def cgw(ipCGW, nameCGW):

    global customerGWId

    client = boto3.client("ec2")

    # Customer Gateway Options
    response = client.create_customer_gateway(
        BgpAsn=65000,
        Type="ipsec.1",
        IpAddress=ipCGW,
        TagSpecifications=[
            {
                "ResourceType": "customer-gateway",
                "Tags": [
                    {"Key": "Name", "Value": nameCGW},
                ],
            },
        ],
    )

    customerGWId = response["CustomerGateway"]["CustomerGatewayId"]
    print("\nCreating Customer Gateway...")
    time.sleep(15)

    vpnConnection(nameVPN, staticRoutes)


# This function creates a VPN S2S
def vpnConnection(nameVPN, staticRoutes):

    global vpnId, tunnel1, tunnel2, psk1, psk2

    client = boto3.client("ec2")

    # VPN S2S Options
    response = client.create_vpn_connection(
        CustomerGatewayId=customerGWId,
        Type="ipsec.1",
        VpnGatewayId="vgw-0cf5449a328cd3e40",
        Options={"StaticRoutesOnly": True},
        TagSpecifications=[
            {
                "ResourceType": "vpn-connection",
                "Tags": [{"Key": "Name", "Value": nameVPN}],
            }
        ],
    )

    # Get VPN id, outside ip address and psk
    vpnId = response["VpnConnection"]["VpnConnectionId"]
    tunnel1 = response["VpnConnection"]["Options"]["TunnelOptions"][0][
        "OutsideIpAddress"
    ]
    tunnel2 = response["VpnConnection"]["Options"]["TunnelOptions"][1][
        "OutsideIpAddress"
    ]
    psk1 = response["VpnConnection"]["Options"]["TunnelOptions"][0]["PreSharedKey"]
    psk2 = response["VpnConnection"]["Options"]["TunnelOptions"][1]["PreSharedKey"]

    # Modify the static rotues
    client.create_vpn_connection_route(
        DestinationCidrBlock=staticRoutes, VpnConnectionId=vpnId
    )

    print("Creating VPN S2S... Please wait a few minutes.")
    vpnStateValidation()

    print("Modifying the tunnels...")
    modifyTunnels(tunnel1)
    vpnStateValidation()
    modifyTunnels(tunnel2)

    print("Creating CloudWatch alarms...")
    cwAlarm(tunnel1, "1")
    cwAlarm(tunnel2, "2")


# This functions modify the VPN tunnels
def modifyTunnels(tunnel):

    # Tunnel Options
    tunnelsOptions = {
        "Phase1LifetimeSeconds": 28800,
        "Phase2LifetimeSeconds": 3600,
        "DPDTimeoutAction": "clear",
        "StartupAction": "add",
        "Phase1EncryptionAlgorithms": [{"Value": "AES256"}],
        "Phase2EncryptionAlgorithms": [{"Value": "AES256"}],
        "Phase1IntegrityAlgorithms": [{"Value": "SHA1"}],
        "Phase2IntegrityAlgorithms": [{"Value": "SHA1"}],
        "Phase1DHGroupNumbers": [{"Value": 2}],
        "Phase2DHGroupNumbers": [{"Value": 2}],
        "IKEVersions": [{"Value": "ikev1"}],
    }

    client = boto3.client("ec2")

    # Modify the tunnel options
    client.modify_vpn_tunnel_options(
        VpnConnectionId=vpnId,
        VpnTunnelOutsideIpAddress=tunnel,
        TunnelOptions=tunnelsOptions,
    )


# Creating Cloudwatch alarms for tunnels
def cwAlarm(ipTunnel, noTunnel):

    client = boto3.client("cloudwatch")

    # Alarm Options
    client.put_metric_alarm(
        AlarmName=f"VOZY-VPN-{nameVPN}-Tunnel {noTunnel}",
        AlarmDescription=f"VOZY-VPN-{nameVPN}-Tunnel {noTunnel}",
        ActionsEnabled=True,
        OKActions=["arn:aws:sns:us-east-1:420213966676:kevin_CW_Labs_Topic"],
        AlarmActions=[
            "arn:aws:sns:us-east-1:420213966676:kevin_CW_Labs_Topic",
            "arn:aws:sns:us-east-1:420213966676:sns-test-kevin",
        ],
        MetricName="TunnelState",
        Namespace="AWS/VPN",
        Statistic="Average",
        Dimensions=[
            {"Name": "TunnelIpAddress", "Value": ipTunnel},
        ],
        Period=300,
        EvaluationPeriods=1,
        DatapointsToAlarm=1,
        Threshold=0,
        ComparisonOperator="LessThanOrEqualToThreshold",
        TreatMissingData="missing",
    )


# Check vpn status
def vpnStateValidation():

    vpnState = False

    # Describe the VPN connection and get the state
    while vpnState != True:
        client = boto3.client("ec2")
        response = client.describe_vpn_connections(
            VpnConnectionIds=[vpnId],
        )

        if response["VpnConnections"][0]["State"] == "available":
            vpnState = True
        else:
            time.sleep(40)


# Call cgw function to create CGW and VPN S2S
cgw(ipCGW, nameCGW)

# Print the results
print(
    f"\n~~~ VPN S2S successfully created, relevant values: ~~~\n\
    \nTunnel 1: {tunnel1}\
    \nTunnel 2: {tunnel2}\
    \nPSK 1: {psk1}\
    \nPSK 2: {psk2}\
    \nPerfect Forward Secrecy: Yes\
    \nDiffie-Hellman Group (DH): 2"
)
