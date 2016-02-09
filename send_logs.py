#!/usr/local/bin/python3.0

import apache_tools
import json
import log_tools
import os
import sys
import urllib.request

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

            if "host" in json_data:
                self.host_id = json_data["host"];
            else:
                self.host_id = "localhost"

    def write_config(self):
        config_json = {
            "monitor" : self.log_monitors
        }
        
        with open(self.file_path, 'w') as outfile:
            json.dump(config_json, outfile, sort_keys = True, indent = 4)

def check_monitors(config_obj):
    for monitor in config_obj.log_monitors:
        if monitor["type"] == "apache access combined":
            log_lines = log_tools.read_single_line_log_file(monitor["location"])

            # Check to see if log was rotated
            if len(log_lines) < monitor["last_line_read"]:
                monitor["last_line_read"] = 0
                print ("Log Rotated: %s" % str(monitor["location"]))
                                  
            # Parse Apache access combined
            log_list = apache_tools.read_apache_logfile(log_lines, monitor["last_line_read"])
            line_count = 0
            
            for log_entry in log_list:
                post_success = proccess_event(monitor["host_id"], monitor, log_entry)
                line_count = line_count + 1

    config_obj.write_config()
    
def main():
    config_obj = config()
    check_monitors(config_obj)

def proccess_event(host_id, monitor_config, log_data):
    if "requests" in monitor_config:
        for request in monitor_config["requests"]:
            try:
                post_data = {
                    "time": log_data["time"],
                    "host": host_id,
                    "sourcetype": "access_combined",
                    "event": log_data
                }
                
                data = json.dumps(post_data).encode('utf8') 
                auth_header = "Splunk %s" % request["token"]
                headers = {'Authorization' : auth_header}

                req = urllib.request.Request(request["address"], data, headers)
                response = urllib.request.urlopen(req)
                read_response = response.read()

                try:
                    response_json = json.loads(str(read_response)[2:-1])

                    if "text" in response_json:
                        if response_json["text"] == "Success":
                            post_success = True
                        else:
                            post_success = False
                except:
                    post_success = False
                    
                if post_success == True:
                    # Update last line and time read
                    monitor_config["last_line_read"] = monitor_config["last_line_read"] + 1
                    monitor_config["last_time_read"] = int(datetime.now().strftime('%s'))
                else:
                    print ("Error sending request, server responded with error.")
                    break
                
            except Exception as err:
                post_success = False
                print ("Error sending request")
                print (str(err))

    return post_success

def test_apache():
    script_dir = os.path.dirname(__file__)
    log_file = "test logs/Apache-WordPress.log"
    file_path = os.path.join(script_dir, log_file)
    log_list = apache_tools.read_apache_logfile(file_path)

    for l in log_list:
        r = l["resource"]
        vs = apache_tools.read_variables(r)
        print (str(vs))
        
    # print (log_list)

main()
