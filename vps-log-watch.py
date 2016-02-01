#!/usr/bin/python

import apache_tools
import json
import os
from datetime import datetime

class config:
    log_monitors = []
    file_path = ""
    
    def __init__(self):
        script_dir = os.path.dirname(__file__)
        config_file = "logw.config"
        self.file_path = os.path.join(script_dir, config_file)

        if os.path.exists(self.file_path):
            json_file = open(self.file_path)
            json_data = json.load(json_file)
            self.log_monitors = json_data["monitor"];

            for monitor in self.log_monitors:
                # Check if log was rotated
                if "last_time_read" in monitor:
                    last_read = datetime.fromtimestamp(monitor["last_time_read"])
                else:
                    last_read = datetime.fromtimestamp(0)
                    
                now = datetime.now()
                time_arr = monitor["rotation_start"].split(":")
                rotate_time = now.replace(hour=int(time_arr[0]), minute=int(time_arr[1]))

                if (last_read < rotate_time) and (rotate_time < now):
                    monitor["last_line_read"] = 0

    def write_config(self):
        config_json = {"monitor" : self.log_monitors}
        
        with open(self.file_path, 'w') as outfile:
            json.dump(config_json, outfile, sort_keys = False, indent = 4)

def check_monitors(config_obj): 
    for monitor in config_obj.log_monitors:
        if monitor["type"] == "apache access combined":
            log_list = apache_tools.read_apache_logfile(monitor["location"], monitor["last_line_read"])
            monitor["last_line_read"] = monitor["last_line_read"] + len(log_list)
            monitor["last_time_read"] = int(datetime.now().strftime('%s'))
            
            for log_entry in log_list:
                proccess_event(config_obj, log_entry)

    config_obj.write_config()
    
def main():
    print "Script started"
    config_obj = config()
    check_monitors(config_obj)

def proccess_event(config_obj, event):
    print str(event)

def send_event(config_obj):
    print "Send event"

def test_apache():
    script_dir = os.path.dirname(__file__)
    log_file = "test logs/Apache-WordPress.log"
    file_path = os.path.join(script_dir, log_file)
    log_list = apache_tools.read_apache_logfile(file_path)

    print log_list

main()
