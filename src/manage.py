#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

    # From <app>/bin to <app>/src
    PROJECT_DIR = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
    sys.path.append(PROJECT_DIR)

    #Change the app_name to your app_name 
    #Example lithium.settings

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gladminds.settings")
  
    from django.core.management import execute_from_command_line
    print os.environ["DJANGO_SETTINGS_MODULE"]
    execute_from_command_line(sys.argv)
