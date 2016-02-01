# VPS-Log-Watch

## Description
A collection of scripts that watch or forward logs from VPS servers where forwarders cannot be installed.

These scripts are still being written, but more details on the workings of the scripts will be written here.

## Main Scripts
### send_logs.py 
Monitors logs and sends new entries via HTTP to a collector like Splunk.

## Support Scripts
### apache_tools.py
A collection of functions for dealing with apache logs. This is used by the main scripts.

## Requirements
Python version 3.0 or higher
