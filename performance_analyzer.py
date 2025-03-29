import pandas as pd
import numpy as np

def rate_gap(csv_file, max_mcs):
    """
    Rate_Gap = MCS_theoretical - MCS_observed

    For the AP that we are observing we find the best theoretical throughput.
    Specifically, we find how many spatial streams it can support; 
    hence the max MCS index.

    By having the max MCS aka the theoretical MCS we go through all the packets 
    (we filter only: data frame packets, destination address to be a specific device, 
    source address to be a specific AP and packets that do have a MCS index)
    and we measure the rate gap for each. 

    Then we average the rate gap for all the packets and we return the average.
    
    Args:
        packets (list): List of packet dictionaries.
        max_mcs (int): Maximum MCS index.
    
    Returns:
        float: Average rate gap.
    """
    

    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Convert fc_type to numeric if necessary
    df['fc_type'] = pd.to_numeric(df['fc_type'], errors='coerce')
    
    # Normalize MAC addresses (ta and ra) to uppercase and strip whitespace
    df['ta'] = df['ta'].str.upper().str.strip()
    df['ra'] = df['ra'].str.upper().str.strip()

    print(f"Initial DataFrame shape: {df.shape}")

    # Filter the DataFrame for packets with MCS index and the specified conditions
    filtered_df = df[
        (df['fc_type'] == 2) &
        (df['ta'] == "2C:F8:9B:DD:06:A0") &
        (df['ra'] == "00:20:A6:FC:B0:36")
    ]
   #(df['mcs_index'] != 0)]

    print(f"Filtered DataFrame shape: {filtered_df.shape}")

    # Calculate the rate gap for each packet
    filtered_df['rate_gap'] = max_mcs - filtered_df['mcs_index']

    # Calculate the average rate gap
    average_rate_gap = filtered_df['rate_gap'].mean()

    return average_rate_gap, filtered_df['rate_gap']

#if __name__ == "__main__":
    #csv_file = 'HowIWiFi.csv'
    #max_mcs = 15  # Example maximum MCS index
    #average_gap = rate_gap(csv_file, max_mcs)
    #print(f"Average Rate Gap: {average_gap}")