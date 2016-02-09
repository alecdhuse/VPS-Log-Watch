#!/usr/local/bin/python3.0

import os

def read_single_line_log_file(log_file):
    """Reads all logs from a file where logs are denoted by a line break."""
    log_lines = []

    if os.path.exists(log_file):
        with open(log_file) as f: 
            log_lines = f.readlines()    
    else:
        print ("Log file not found: %s" % str(log_file))

    return log_lines
