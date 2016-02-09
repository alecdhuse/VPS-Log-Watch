# VPS-Log-Watch

## Requirements
Python version 3.0 or higher

## Description
A collection of scripts that watch or forward logs from VPS servers where forwarders cannot be installed.
These scripts are still being written, but more details on the workings of the scripts will be written here.


## Main Scripts
### send_logs.py 
Monitors logs and sends new entries via HTTP to a collector like Splunk.


## Support Scripts
### apache_tools.py
A collection of functions for dealing with apache logs. This is used by the main scripts.

### log_tools.py
A collection of shared function for log proccessing.

## Troubleshooting

Your VPS host may block various outbound connections, causing issues with the script. However port 80 is usually open. If your receiving host is running linux an easy fix is to use port forwarding to direct port 80 to the correct listening port. Below is a one line rule that will accomplish this.

> iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to 8088
