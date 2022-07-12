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
        VpnGatewayId="vgw-01de3c706bedb0f42",
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

    print(
        "\n~~~ VPN S2S Tunnel Options: https://docs.aws.amazon.com/vpn/latest/s2svpn/VPNTunnels.html ~~~\n\
\nModifying Tunnel 1..."
    )
    modifyTunnels(tunnel1)
    vpnStateValidation()
    print("\nModifying Tunnel 2...")
    modifyTunnels(tunnel2)

    print("Creating CloudWatch alarms...")
    cwAlarm(tunnel1, "1")
    cwAlarm(tunnel2, "2")


# This functions modify the VPN tunnels
def modifyTunnels(tunnel):

    Phase1Encryption = []
    Phase2Encryption = []
    Phase1Integrity = []
    Phase2Integrity = []
    Phase1DH = []
    Phase2DH = []
    IKEv = []

    Phase1Lifetime = int(
        input("The lifetime for phase 1 of the IKE negotiation, in seconds: ")
    )
    Phase2Lifetime = int(
        input("The lifetime for phase 2 of the IKE negotiation, in seconds: ")
    )
    Phase1EncryptionAlgorithms = str(
        input("Phase 1 encryption algorithms (Delimit by comma): ")
    )
    Phase2EncryptionAlgorithms = str(
        input("Phase 2 encryption algorithms (Delimit by comma): ")
    )
    Phase1IntegrityAlgorithms = str(
        input("Phase 1 integrity algorithms (Delimit by comma): ")
    )
    Phase2IntegrityAlgorithms = str(
        input("Phase 2 integrity algorithms (Delimit by comma): ")
    )
    Phase1DHGroupNumbers = str(input("Phase 1 DH group numbers (Delimit by comma): "))
    Phase2DHGroupNumbers = str(input("Phase 2 DH group numbers (Delimit by comma): "))
    IKEVersions = str(input("IKE versions (Delimit by comma): "))

    for a in Phase1DHGroupNumbers.rsplit(","):
        Phase1DH.append({"Value": int(a)})

    for b in Phase2DHGroupNumbers.rsplit(","):
        Phase2DH.append({"Value": int(b)})

    for c in Phase1EncryptionAlgorithms.rsplit(","):
        Phase1Encryption.append({"Value": c.replace(" ", "")})

    for d in Phase2EncryptionAlgorithms.rsplit(","):
        Phase2Encryption.append({"Value": d.replace(" ", "")})

    for e in Phase1IntegrityAlgorithms.rsplit(","):
        Phase1Integrity.append({"Value": e.replace(" ", "")})

    for f in Phase2IntegrityAlgorithms.rsplit(","):
        Phase2Integrity.append({"Value": f.replace(" ", "")})

    for g in IKEVersions.rsplit(","):
        IKEv.append({"Value": g.replace(" ", "")})

    # Tunnel Options
    tunnelsOptions = {
        "Phase1LifetimeSeconds": Phase1Lifetime,
        "Phase2LifetimeSeconds": Phase2Lifetime,
        "DPDTimeoutAction": "clear",
        "StartupAction": "add",
        "Phase1EncryptionAlgorithms": Phase1Encryption,
        "Phase2EncryptionAlgorithms": Phase2Encryption,
        "Phase1IntegrityAlgorithms": Phase1Integrity,
        "Phase2IntegrityAlgorithms": Phase2Integrity,
        "Phase1DHGroupNumbers": Phase1DH,
        "Phase2DHGroupNumbers": Phase2DH,
        "IKEVersions": IKEv,
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
        OKActions=["arn:aws:sns:us-east-1:808378037958:VPN_OK"],
        AlarmActions=[
            "arn:aws:sns:us-east-1:808378037958:VPN_Alarm",
            "arn:aws:sns:us-east-1:808378037958:Slack_infra_Vozy_Alarm",
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
