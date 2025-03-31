# WiFi Doctor 

**WiFi Doctor** is a Python tool that helps you monitor, analyze, and visualize your Wi-Fi network. Its main purposes include:

1. **Parsing** capture files  
2. **Analyzing** signal strength, channel overlap, and network traffic  
3. **Detecting** performance issues such as jitter, interference, or congestion  
4. **Visualizing** network performance over time


## Description

The goal of this project is to design and implement a Wi-Fi network performance monitoring
system. By capturing and analyzing Wi-Fi packets across various setups, we are able to assess
network performance and identify the underlying factors influencing its quality. We observed
that either transitioning from the 2.4 GHz band to the 5 GHz band or operating in a home
environment instead of an enterprise setup significantly improves Wi-Fi density. Furthermore,
we identified the key factors that hinder throughput and data rate performance.

## Dependencies

Before running WiFi Doctor, install all required Python packages using:

```sh
   pip install -r requirements.txt
   ```
##

## How to Use  

You can use `pcap_parser.py` to process any `.pcap` file, converting it into a corresponding `.csv` file. This `.csv` file can then be used as input for `performance_monitor.py` and `performance_analyzer.py`.  

We have provided several `.csv` files for reference. The initial packet captures were taken in different environments (**2.4 GHz / 5 GHz, Home / Mall**), allowing for an easy comparison of **network density** and **interference levels**. Additionally, the file `mikehome1.csv` was captured while monitoring a device moving **away from and toward** an access point (**AP**).  

### Scripts Overview  

- **`performance_monitor.py`**  
  Analyzes the network based on **four density metrics** and outputs a **final density score** for each setup in the terminal.  

- **`visualizer.py`**  
  Utilizes functions from `performance_monitor.py` and `performance_analyzer.py` to generate **visual plots** for further analysis.  



