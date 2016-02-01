#!/usr/bin/python

import os
import shlex

from datetime import datetime


class apache_access_log:
    ip = "0.0.0.0"
    user_id = ""
    timestamp = 0
    action = ""
    resource = ""
    status = 0
    http_version = ""
    user_agent = ""
    referer = ""
    object_size = 0

    def __init__(self, log_line):
        """Parses Apache log line and creates a new appache_access_log object"""
        fields = shlex.split(log_line)

        self.ip = fields[0]
        self.user_id = fields[2] if (fields[2] != "-") else ""
        
        #Parse timestamp and offset to UDT
        line_timestamp = datetime.strptime(fields[3][1:], '%d/%b/%Y:%H:%M:%S')
        offset_string = fields[4][:-1]
        ts_offset = (int(offset_string[-4:-2])*60 + int(offset_string[-2:])) * 60
        if offset_string[:1] == "-": ts_offset = -ts_offset
        self.timestamp = int(line_timestamp.strftime('%s'))

        #Split up request field
        req_fields = shlex.split(fields[5])
        self.action = req_fields[0]
        self.resource = req_fields[1]
        self.http_version = req_fields[2]

        self.status = int(fields[6])
        self.referer = fields[8]
        self.user_agent = fields[9]

        try:
            self.object_size = int(fields[7])
        except:
            self.object_size = 0
            
    def get_dictionary(self):
        new_dictionary = {}
        new_dictionary["ip"] = self.ip
        new_dictionary["user_id"] = self.user_id
        new_dictionary["time"] = self.timestamp
        new_dictionary["action"] = self.action
        new_dictionary["resource"] = self.resource
        new_dictionary["http_version"] = self.http_version
        new_dictionary["status"] = self.status
        new_dictionary["user_agent"] = self.user_agent
        new_dictionary["referer"] = self.referer
        new_dictionary["object_size"] = self.object_size
        
        return new_dictionary
        
def read_apache_logfile(log_file, line_start=0, time_start=0):
    """Reads in Apache Logfile"""
    log_list = []

    if os.path.exists(log_file):
        with open(log_file) as f: 
            lines = f.readlines()
            
        current_line = 0;

        for line in lines:
            
            if (line_start > current_line):
                current_line = current_line + 1
                continue
            else:
                log_obj = apache_access_log(line)
                log_list.append(log_obj.get_dictionary())
                current_line = current_line + 1

    else:
        print ("File Not Found")

    return log_list
