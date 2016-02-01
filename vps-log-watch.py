#!/usr/bin/python

import apache_tools
import json
import os

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

    def write_config(self):
        config_json = {"monitor" : self.log_monitors}
        
        with open(self.file_path, 'w') as outfile:
            json.dump(config_json, outfile)

def check_monitors(config_obj): 
    for monitor in config_obj.log_monitors:
        if monitor["type"] == "apache access combined":
            log_list = apache_tools.read_apache_logfile(monitor["location"], monitor["last_line_read"])
            monitor["last_line_read"] = monitor["last_line_read"] + len(log_list)

            for le in log_list:
                print str(le)

    config_obj.write_config()
    
def main():
    print "Script started"
    config_obj = config()
    check_monitors(config_obj)

def test_apache():
    script_dir = os.path.dirname(__file__)
    log_file = "test logs/Apache-WordPress.log"
    file_path = os.path.join(script_dir, log_file)
    log_list = apache_tools.read_apache_logfile(file_path)

    print log_list

main()
