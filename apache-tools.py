#!/usr/bin/python

class apache_access_log:
    ip = "0.0.0.0"
    user_id = ""
    timestamp = 0
    action = ""
    resource = ""
    http_version = ""
    user_agent = ""
    referer = ""
    object_size = 0

def parse_apache_log(log_line):
    """Parses Apache log line and returns an appache_access_log object"""

    return null

def read_apache_logfile(log_file, line_start, time_start):
    """Reads in Apache Logfile"""

    if os.path.exists(log_file):
        with open(log_file) as f: 
            lines = f.readlines()

        current_line = 0;
        
        for line in lines:
            if (line_start > current_line):
                continue
            elif:
                log_obj = parse_apache_log(line)

    else:
        print "File Not Found"
