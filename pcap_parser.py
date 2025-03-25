import pyshark
import pandas as pd
import datetime

pcap_file = '/home/axynobiti/Downloads/2.4_tuc_pavlos.pcapng'

# helper functions
def get_field(layer, attr):
    try:
        return getattr(layer, attr)
    except Exception:
        return None

def get_raw_field(packet, layername, key):
    try:
        return packet[layername]._all_fields.get(key)
    except Exception:
        return None

# Store parsed data here
packet_data = []

try:
    cap = pyshark.FileCapture(pcap_file, only_summaries=False, use_json=False)

    for i, packet in enumerate(cap):

        # Special treatment for timestamp otherwise it doesnt recognize fixed_timestamp from layer wlan.mgt
        tsf_timestamp = None
        try:
            if 'wlan.mgt' in packet:
                tsf = packet['wlan.mgt'].get_field('wlan_fixed_timestamp')
                if tsf:
                    tsf_timestamp = tsf
        except Exception:
            pass



        # Building the packet dictionary
        pkt = {
            "packet_number": get_field(packet, 'number'),
            "length": get_field(packet, 'length'),
            "bssid": get_field(getattr(packet, 'wlan', None), 'bssid'),
            "ta": get_field(getattr(packet, 'wlan', None), 'ta'),
            "ra": get_field(getattr(packet, 'wlan', None), 'ra'),
            "fc_type_subtype": get_field(getattr(packet, 'wlan', None), 'fc_type_subtype'),
            "data_rate": get_field(getattr(packet, 'wlan_radio', None), 'data_rate'),
            "channel": get_field(getattr(packet, 'wlan_radio', None), 'channel'),
            "frequency": get_field(getattr(packet, 'wlan_radio', None), 'frequency'),
            "phy": get_field(getattr(packet, 'wlan_radio', None), 'phy'),
            "short_gi": get_field(getattr(packet, 'radiotap', None), 'flags_shortgi'),
            "signal_strength": get_field(getattr(packet, 'wlan_radio', None), 'signal_dbm'),
            "bandwidth": get_field(getattr(packet, 'radiotap', None), 'channel_flags'),
            "mcs_index": get_raw_field(packet, 'radiotap', 'radiotap.mcs.index'),
            "spatial_streams_tx_max": get_field(getattr(packet, 'wlan_mgt', None), 'wlan_ht_mcsset_txmaxss'), #NOT FOUND YET
            "tsf_timestamp": tsf_timestamp, # in wireshark its inside wifi manager its the APs timestamp 
            "timestamp_wireshark" : float(packet.frame_info.time_epoch), # for beacon jitter!!!
        }

        # Append the packet data
        packet_data.append(pkt)

    # Create DataFrame and save CSV
    df = pd.DataFrame(packet_data)

    # making readable time from wireshark
    df['timestamp_readable'] = df['timestamp_wireshark'].apply(
    lambda x: datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S.%f')
)
    # maybe use the file in libreoffice calc or excel
    df.to_csv("wifi_packet_analysis.csv", index=False)
    print("CSV saved as wifi_packet_analysis.csv")

except FileNotFoundError:
    print(f"Error: The file {pcap_file} was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
