import pyshark

# Path to your pcap file
pcap_file = '/home/moike/Downloads/wifi_doctor_zip/wifi_doctor_zip/HowIWiFi_PCAP.pcap'

# Verify file exists
import os
if not os.path.exists(pcap_file):
    print(f"Error: The file {pcap_file} was not found.")
else:
    print(f"Successfully found the file: {pcap_file}")

    try:
        # Open the pcap file
        cap = pyshark.FileCapture(pcap_file)

        # Loop through each packet in the capture
        packet_count = 0
        for packet in cap:
            print(f"Packet number {packet.number}:")
            #print(packet.summary())
            print('---')
            packet_count += 1

        if packet_count == 0:
            print("No packets found in the file.")
        else:
            print(f"Processed {packet_count} packets.")

    except Exception as e:
        print(f"An error occurred while processing the file: {e}")
