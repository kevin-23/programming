import boto3
import time
import sys

# Enter parameters
nameCGW = input(
    str("~~~ Customer Gataway parameters ~~~\nEnter Customer Gateway Name: "))
ipCGW = input(str("Enter Customer Gateway IPv4: "))

nameVPN = input(str("\n~~~ VPN S2S parameters ~~~\nEnter VPN Name: "))
staticRoutes = input(
    str("Enter Static Routes IPv4 (Delimit by comma). The CIDR block associated with the local subnet of the customer network: "
        ))


# This function creates a customer gateway
def cgw(ipCGW, nameCGW):

    global customerGWId

    client = boto3.client("ec2")

    # Customer Gateway Options
    try:
        response = client.create_customer_gateway(
            BgpAsn=65000,
            Type="ipsec.1",
            IpAddress=ipCGW,
            TagSpecifications=[
                {
                    "ResourceType": "customer-gateway",
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": nameCGW
                        },
                    ],
                },
            ],
        )
    except:
        sys.exit(
            "\n!!! Error when creating the Customer Gateway. Unable to continue with the creation of the S2S VPN !!!"
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
    try:
        response = client.create_vpn_connection(
            CustomerGatewayId=customerGWId,
            Type="ipsec.1",
            VpnGatewayId="vgw-01de3c706bedb0f42",
            Options={"StaticRoutesOnly": True},
            TagSpecifications=[{
                "ResourceType": "vpn-connection",
                "Tags": [{
                    "Key": "Name",
                    "Value": nameVPN
                }],
            }],
        )
    except:
        sys.exit(
            "\n!!! Error when creating the VPN S2S. Unable to continue with the creation of the S2S VPN !!!"
        )
    # Get VPN id, outside ip address and psk
    vpnId = response["VpnConnection"]["VpnConnectionId"]
    tunnel1 = response["VpnConnection"]["Options"]["TunnelOptions"][0][
        "OutsideIpAddress"]
    tunnel2 = response["VpnConnection"]["Options"]["TunnelOptions"][1][
        "OutsideIpAddress"]
    psk1 = response["VpnConnection"]["Options"]["TunnelOptions"][0][
        "PreSharedKey"]
    psk2 = response["VpnConnection"]["Options"]["TunnelOptions"][1][
        "PreSharedKey"]

    # Modify the static rotues
    staticRT = ''.replace(" ", "")
    try:
        for routes in staticRoutes.rsplit(","):
            staticRT = routes
            client.create_vpn_connection_route(DestinationCidrBlock=routes.replace(
                " ", ""),
                VpnConnectionId=vpnId)
            time.sleep(2)
    except:
        print(
            f"\n!!! {staticRT} is a wrong static route. The configuration of static routes is stopped !!!"
        )

    print("\nCreating VPN S2S... Please wait a few minutes.")
    vpnStateValidation()

    print("\n~~~ S2S VPN tunnel options available: ~~~\
\nPhase 1 Lifetime: Specify a number between 900 and 28800\n\
Phase 2 lifetime: Specify a number between 900 and 3600\n\
Phase 1 encryption, multiple options available: AES128, AES256, AES128-GCM-16, AES256-GCM-16\n\
Phase 2 encryption, multiple options available: AES128, AES256, AES128-GCM-16, AES256-GCM-16\n\
Phase 1 integrity, multiple options available: SHA1, SHA2-256, SHA2-384, SHA2-512\n\
Phase 2 integrity, multiple options available: SHA1, SHA2-256, SHA2-384, SHA2-512\n\
Phase 1 DH group numbers, multiple options available: 2, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24\n\
Phase 2 DH group numbers, multiple options available: 2, 5, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24\n\
IKE versions, multiple options available: IKEV1, IKEV2\n")

    try:
        tunnelsParameters()
        print("\nModifying Tunnel 1...")
        modifyTunnel(tunnel1)
        vpnStateValidation()

        sameParameters = input(
            str("\nDo you want to use the same configuration of tunnel 1 for tunnel 2? y/N: "
                )).lower()
        if sameParameters == "y" or sameParameters == "yes":
            print("\nModifying Tunnel 2...")
            modifyTunnel(tunnel2)
        else:
            tunnelsParameters()
            modifyTunnel(tunnel2)
    except:
        print(
            "\n!!! You entered a wrong parameter for the VPN tunnel configuration. The configuration of both VPN tunnels is stopped !!!\n"
        )

    print("Creating CloudWatch alarms...")
    cwAlarm(tunnel1, "1")
    cwAlarm(tunnel2, "2")


Phase1Encryption = []
Phase2Encryption = []
Phase1Integrity = []
Phase2Integrity = []
Phase1DH = []
Phase2DH = []
IKEv = []


# This functions modify the VPN tunnels
def tunnelsParameters():

    Phase1Encryption.clear()
    Phase2Encryption.clear()
    Phase1Integrity.clear()
    Phase2Integrity.clear()
    Phase1DH.clear()
    Phase2DH.clear()
    IKEv.clear()

    global Phase1Lifetime, Phase2Lifetime

    Phase1Lifetime = int(
        input("\n~~~ S2S VPN tunnel options: ~~~\n\
Type the lifetime for phase 1 of the IKE negotiation, in seconds: "))
    Phase2Lifetime = int(
        input("Type the lifetime for phase 2 of the IKE negotiation, in seconds: "))
    Phase1EncryptionAlgorithms = str(
        input("Type the phase 1 encryption algorithms (Delimit by comma): ").upper())
    Phase2EncryptionAlgorithms = str(
        input("Type the phase 2 encryption algorithms (Delimit by comma): ").upper())
    Phase1IntegrityAlgorithms = str(
        input("Type the phase 1 integrity algorithms (Delimit by comma): ").upper())
    Phase2IntegrityAlgorithms = str(
        input("Type the phase 2 integrity algorithms (Delimit by comma): ").upper())
    Phase1DHGroupNumbers = str(
        input("Type the phase 1 DH group numbers (Delimit by comma): "))
    Phase2DHGroupNumbers = str(
        input("Type the phase 2 DH group numbers (Delimit by comma): "))
    IKEVersions = str(input("IKE versions (Delimit by comma): ")).lower()

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


def modifyTunnel(tunnel):
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
        OKActions=[
            "arn:aws:sns:us-east-1:808378037958:AWSHealth-chatbot2",
            "arn:aws:sns:us-east-1:808378037958:Slack_infra_Vozy_Ok",
        ],
        AlarmActions=[
            "arn:aws:sns:us-east-1:808378037958:AWSHealth-chatbot2",
            "arn:aws:sns:us-east-1:808378037958:Slack_infra_Vozy_Alarm",
        ],
        MetricName="TunnelState",
        Namespace="AWS/VPN",
        Statistic="Average",
        Dimensions=[
            {
                "Name": "TunnelIpAddress",
                "Value": ipTunnel
            },
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
        response = client.describe_vpn_connections(VpnConnectionIds=[vpnId], )

        if response["VpnConnections"][0]["State"] == "available":
            vpnState = True
        else:
            time.sleep(40)


# Call cgw function to create CGW and VPN S2S
cgw(ipCGW, nameCGW)

# Print the results
print(f"\n~~~ VPN S2S successfully created, relevant values: ~~~\n\
    \nTunnel 1: {tunnel1}\
    \nTunnel 2: {tunnel2}\
    \nPSK 1: {psk1}\
    \nPSK 2: {psk2}\
    \nPerfect Forward Secrecy: Yes\
    \nDiffie-Hellman Group (DH): 2")
