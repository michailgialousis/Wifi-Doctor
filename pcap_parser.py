import pyshark

# Path to your pcap file
pcap_file = '/home/moike/Downloads/wifi_doctor_zip/wifi_doctor_zip/HowIWiFi_PCAP.pcap'  # Replace with your actual file path

try:
    # Open the pcap file
    cap = pyshark.FileCapture(pcap_file, only_summaries=False)

     
    # Loop through each packet in the capture and print basic info
    #for packet in cap:
    for i, packet in enumerate(cap) :

        
        
        if i >= 1:
            break  # Stop after the first 30 packets

        print("packet : ")
        print(dir(packet))
        print("----------------------")
        print("packet.wlan : ")
        print(dir(packet.wlan))
        print("----------------------")
        print("packet.wlan_radio : ")
        print(dir(packet.wlan_radio))
        print("----------------------")
        print("packet.radiotap : ")
        print(dir(packet.radiotap))
        print("----------------------")
        
        print("Packet number: ", packet.number)
        print(f"Packet length: {packet.length} bytes")
        
        try:
            print(f" - BSSID: {packet.wlan.bssid}")
        except AttributeError:
            print(" - BSSID not found")
        
        try:
            print(f" - Transmitter MAC address (TA): {packet.wlan.ta}")
        except AttributeError:
            print(" - Transmitter MAC address (TA) not found")
        
        try:
            print(f" - Receiver MAC address (RA): {packet.wlan.ra}")
        except AttributeError:
            print(" - Receiver MAC address (RA) not found")
        
        try:
            print(f" - Type/Subtype: {packet.wlan.fc_type_subtype}")
        except AttributeError:
            print(" - Type/Subtype not found")
        
        try:
            print(f" - Data Rate: {packet.wlan_radio.data_rate}")
        except AttributeError:
            print(" - Data Rate not found")

        try:
            print(f" - Channel: {packet.wlan_radio.channel}")  # Channel number (e.g., 3)
        except AttributeError:
            print(" - Channel not found")
        
        try:
            print(f" - Frequency: {packet.wlan_radio.frequency}")  # Frequency (e.g., 2422 MHz)
        except AttributeError:
            print(" - Frequency not found")
        
        try:
            print(f" - PHY Type: {packet.wlan_radio.phy}")  # PHY Type (e.g., 802.11n)
        except AttributeError:
            print(" - PHY Type not found")
        
        try:
            print(f" - Short GI: {packet.radiotap.flags_shortgi}")  # Short Guard Interval (True/False)
        except AttributeError:
            print(" - Short GI not found")
        
        
        try:
            print(f" - Signal Strength: {packet.wlan_radio.signal_dbm}")  # Signal Strength (e.g., -57 dBm)
            signal_strength = packet.wlan_radio.signal_dbm
        except AttributeError:
            print(" - Signal Strength not found")
        
        try:
            print(f" - MCS Index: {packet.radiotap.present_mcs}")  # MCS Index (if available)
        except AttributeError:
            print(" - MCS Index not found")
        
        try:
            print(f" - Bandwidth: {packet.radiotap.channel_flags}")  # Channel Bandwidth (e.g., 40 MHz)
        except AttributeError:
            print(" - Bandwidth not found")
        
        try:
            print(f" - Spatial Streams: {packet.wlan_radio.spatial_streams}")  # Number of Spatial Streams (if available)
        except AttributeError:
            print(" - Spatial Streams not found")
        
        try:
            print(f"- Signal/Noise Ratio: {packet.wlan_radio.dbm_antsignal - packet.wlan_radio.dbm_antnoise}")  # Signal/Noise Ratio
        except AttributeError:
            print(" - Signal/Noise Ratio not found")
        
        try:
            print(f" - TSF Timestamp: {packet.radiotap.present_tsft}")  # TSF Timestamp
        except AttributeError:
            print(" - TSF Timestamp not found")

        print('---')


except FileNotFoundError:
    print(f"Error: The file {pcap_file} was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
