#!/usr/bin/python

import apache_tools
import os

def test_apache():
    script_dir = os.path.dirname(__file__)
    log_file = "test logs/Apache-WordPress.log"
    file_path = os.path.join(script_dir, log_file)
    log_list = apache_tools.read_apache_logfile(file_path)

    print log_list

def main():
    print "Script started"
    test_apache()

main()
