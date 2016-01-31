#!/usr/bin/python

import apache_tools
import json
import os

class config:
    log_monitors = []
    
    def __init__(self):
        script_dir = os.path.dirname(__file__)
        config_file = "logw.config"
        file_path = os.path.join(script_dir, config_file)

        if os.path.exists(file_path):
            json_file = open(file_path)
            json_data = json.load(json_file)
            self.log_monitors = json_data["monitor"]; 

def test_apache():
    script_dir = os.path.dirname(__file__)
    log_file = "test logs/Apache-WordPress.log"
    file_path = os.path.join(script_dir, log_file)
    log_list = apache_tools.read_apache_logfile(file_path)

    print log_list
    
def main():
    print "Script started"
    config_obj = config()
    print config_obj.log_monitors

main()
