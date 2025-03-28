import pandas as pd
import matplotlib.pyplot as plt
from performance_monitor import beacon_jitter_intervals

def plot_beacon_jitter(jitter_df, top_n=3, output_filename="beacon_jitter_top_n.png"):
    """
    Plots beacon jitter over time for the top_n APs using the jitter_df
    provided as input. This function assumes jitter_df is the DataFrame returned by
    beacon_jitter_intervals.

    Parameters:
        jitter_df (DataFrame): A DataFrame with columns:
            - timestamp_wireshark 
            - jitter_ms (jitter in milliseconds)
            - MAC adr 
        top_n (int): Number of top APs to plot.
        output_filename (str): saved plot.
    """
    # Convert the numeric timestamp to datetime for plotting
    jitter_df['datetime'] = pd.to_datetime(jitter_df['timestamp_wireshark'], unit='s')
    
    plt.figure(figsize=(12, 6))
    
    # Pick the most frequent beacons for ploting 
    top_bssids = jitter_df['bssid'].value_counts().nlargest(top_n).index.tolist()
    filtered_df = jitter_df[jitter_df['bssid'].isin(top_bssids)]
    
    # Plot jitter over time for each of APs choosen above
    for bssid, group in filtered_df.groupby('bssid'):
        plt.plot(group['datetime'], group['jitter_ms'], linestyle='-', label=bssid)
    
    plt.xlabel("Time")
    plt.ylabel("Beacon Jitter (ms)")
    plt.title(f"Beacon Jitter Over Time for Top {top_n} APs")
    plt.legend(title="MAC address", bbox_to_anchor=(0.90, 1), loc="upper left")
    plt.grid(True)
    plt.subplots_adjust(bottom=0.15, top=0.9)
    
    plt.savefig(output_filename)
    plt.close()
    print(f"Plot saved as {output_filename}")

if __name__ == "__main__":

    # CSV files 
    input_csv_single_channel_5home_1ch = '5_home_one.csv'
    input_csv_single_channel_5mall_1ch = '5_riverwest_one.csv'
    input_csv_single_channel_24home_1ch = '2.4_home_one.csv'
    input_csv_single_channel_24mall_1ch = '2.4_riverwest_one.csv'

    # Compute jitter
    beacon_jitter_df_5h  = beacon_jitter_intervals(input_csv_single_channel_5home_1ch)
    beacon_jitter_df_5m  = beacon_jitter_intervals(input_csv_single_channel_5mall_1ch)
    beacon_jitter_df_24h = beacon_jitter_intervals(input_csv_single_channel_24home_1ch)
    beacon_jitter_df_24m = beacon_jitter_intervals(input_csv_single_channel_24mall_1ch)

    # plots for each scenario
    plot_beacon_jitter(beacon_jitter_df_5h, top_n=2, output_filename="beacon_jitter_5_home.png")
    plot_beacon_jitter(beacon_jitter_df_5m, top_n=2, output_filename="beacon_jitter_5_mall.png")
    plot_beacon_jitter(beacon_jitter_df_24h, top_n=3, output_filename="beacon_jitter_2.4_home.png")
    plot_beacon_jitter(beacon_jitter_df_24m, top_n=2, output_filename="beacon_jitter_2.4_mall.png")
