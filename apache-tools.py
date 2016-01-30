#!/usr/bin/python

def parse_apache_log(log_file, line_start, time_start):
    """Parses Apache Logs"""

    if os.path.exists(log_file):
        with open(log_file) as f: 
            lines = f.readlines()
