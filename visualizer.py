import pandas as pd
import matplotlib.pyplot as plt
from performance_monitor import beacon_jitter_intervals, rssi_based_overlap_index, overlap_tot_avg, compute_rssid_from_csv,jitter_tot_avg

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

def plot_avg_overlap(scenario_avgs, output_filename="average_overlap_index_comparison.png"):
    """
    Plots a bar chart of the average overlap index for each scenario.
    
    Parameters:
        scenario_avgs (dict): A dictionary where the keys are scenario names (e.g., "5GHz Home")
                              and the values are the average overlap index (scalar numeric values).
        output_filename (str): Filename to save the plot.
    """
    scenarios = list(scenario_avgs.keys())
    values = [scenario_avgs[sc] for sc in scenarios]
    
    plt.figure(figsize=(10, 6))
    plt.bar(scenarios, values, color=["blue", "green", "orange", "red"], edgecolor="black")
    plt.xlabel("Scenario")
    plt.ylabel("Average Overlap Index")
    plt.title("Average Overlap Index per Scenario")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.close()
    print(f"Bar chart saved as {output_filename}")


def plot_rssids(scenarios_rssid, output_filename="rssid.png"):
    """
    Plots a bar chart of the bssid for each scenario.
    
    Parameters:
        scenario_avgs (dict): A dictionary where the keys are scenario names (e.g., "5GHz Home")
                              and the values are the average overlap index (scalar numeric values).
        output_filename (str): Filename to save the plot.
    """
    scenarios = list(scenarios_rssid.keys())
    values = [scenarios_rssid[sc] for sc in scenarios]
    
    plt.figure(figsize=(10, 6))
    plt.bar(scenarios, values, color=["magenta", "purple", "orange", "red"], edgecolor="black")
    plt.xlabel("Scenario")
    plt.ylabel("Total RSSID")
    plt.title("Total RSSID per Scenario")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.close()
    print(f"Bar chart saved as {output_filename}")


def plot_avg_jitter(scenario_avg_jitter, output_filename="avg_jitter.png"):
    """
    Plots a bar chart of the jitter average for each scenario.
    
    Parameters:
        scenario_avgs (dict): A dictionary where the keys are scenario names (e.g., "5GHz Home")
                              and the values are the average overlap index (scalar numeric values).
        output_filename (str): Filename to save the plot.
    """
    scenarios = list(scenario_avg_jitter.keys())
    values = [scenario_avg_jitter[sc] for sc in scenarios]
    
    plt.figure(figsize=(10, 6))
    plt.bar(scenarios, values, color=["red", "blue", "orange", "green"], edgecolor="black")
    plt.xlabel("Scenario")
    plt.ylabel("Avg jitter ms")
    plt.title("Average jitter per Scenario")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.close()
    print(f"Bar chart saved as {output_filename}")






if __name__ == "__main__":

    # CSV files 
    input_csv_single_channel_5home_1ch = '5_home_one.csv'
    input_csv_single_channel_5mall_1ch = '5_riverwest_one.csv'
    input_csv_single_channel_24home_1ch = '2.4_home_one.csv'
    input_csv_single_channel_24mall_1ch = '2.4_riverwest_one.csv'
    
    input_csv_channel_5home  = '5_home.csv'
    input_csv_channel_5mall  = '5_riverwest.csv'
    input_csv_channel_24home = '2.4_home.csv'
    input_csv_channel_24mall = '2.4_riverwest.csv'

    # Compute jitter
    beacon_jitter_df_5h  = beacon_jitter_intervals(input_csv_single_channel_5home_1ch)
    beacon_jitter_df_5m  = beacon_jitter_intervals(input_csv_single_channel_5mall_1ch)
    beacon_jitter_df_24h = beacon_jitter_intervals(input_csv_single_channel_24home_1ch)
    beacon_jitter_df_24m = beacon_jitter_intervals(input_csv_single_channel_24mall_1ch)

    # avg jitter
    summary_5h  = jitter_tot_avg(beacon_jitter_df_5h)
    mean_jitter_ms_5h = summary_5h['avg_jitter_ms'].iloc[0] #extracting the mean in ms
    summary_5m  = jitter_tot_avg( beacon_jitter_df_5m)
    mean_jitter_ms_5m = summary_5m['avg_jitter_ms'].iloc[0] 
    summary_24h = jitter_tot_avg(beacon_jitter_df_24h)
    mean_jitter_ms_24h = summary_24h['avg_jitter_ms'].iloc[0] 
    summary_24m = jitter_tot_avg(beacon_jitter_df_24m)
    mean_jitter_ms_24m = summary_24m['avg_jitter_ms'].iloc[0] 

    # Average overlapping channels
    overlap_df_5h,chsummary5h  = rssi_based_overlap_index(input_csv_channel_5home,-75)
    overlap_df_5m,chsummary5m  = rssi_based_overlap_index(input_csv_channel_5mall,-75)
    overlap_df_24h,chsummary24h = rssi_based_overlap_index(input_csv_channel_24home,-75)
    overlap_df_24m,chsummary24m  = rssi_based_overlap_index(input_csv_channel_24mall,-75)

    avg_ch_5h  = overlap_tot_avg( chsummary5h)
    avg_ch_5m  = overlap_tot_avg( chsummary5m) 
    avg_ch_24h = overlap_tot_avg( chsummary24h)
    avg_ch_24m = overlap_tot_avg( chsummary24m)

    # RSSID
    rssid_5home_val,rssid_5home_total = compute_rssid_from_csv(input_csv_channel_5home)
    rssid_5mall_val,rssid_5mall_total = compute_rssid_from_csv(input_csv_channel_5mall)
    rssid_24h_val,  rssid_24home_total   = compute_rssid_from_csv(input_csv_channel_24home)
    rssid24m_val,  rssid24mall_total  = compute_rssid_from_csv( input_csv_channel_24mall)

    # Input for ploting avg channel overal
    scenario_avgs = {
    "5GHz Home": avg_ch_5h,
    "5GHz Mall": avg_ch_5m,
    "2.4GHz Home": avg_ch_24h,
    "2.4GHz Mall": avg_ch_24m
    }
    
    # Input for ploting rssid
    scenarios_rssid = {
    "5GHz Home": rssid_5home_total,
    "5GHz Mall": rssid_5mall_total,
    "2.4GHz Home": rssid_24home_total,
    "2.4GHz Mall": rssid24mall_total
    }

    # Input for ploting avg jitter
    scenario_avg_jitter={
    "5GHz Home": mean_jitter_ms_5h,
    "5GHz Mall": mean_jitter_ms_5m,
    "2.4GHz Home": mean_jitter_ms_24h,
    "2.4GHz Mall": mean_jitter_ms_24m
    }
   

    # plots for each scenario-----------------------------------------------------------------------------------------------------

    # jitter
    plot_beacon_jitter(beacon_jitter_df_5h, top_n=2, output_filename="beacon_jitter_5_home.png")
    plot_beacon_jitter(beacon_jitter_df_5m, top_n=2, output_filename="beacon_jitter_5_mall.png")
    plot_beacon_jitter(beacon_jitter_df_24h, top_n=3, output_filename="beacon_jitter_2.4_home.png")
    plot_beacon_jitter(beacon_jitter_df_24m, top_n=2, output_filename="beacon_jitter_2.4_mall.png")
    
    # channel overlap
    plot_avg_overlap(scenario_avgs)
   
    # rssid
    plot_rssids(scenarios_rssid)

    # avg jitter
    plot_avg_jitter(scenario_avg_jitter)
