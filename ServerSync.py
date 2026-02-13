#!/usr/bin/env python3


import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import argparse

parser = argparse.ArgumentParser(usage="A Quick Tool to Sync Files to Local Servers over FTP", description="Idk , i had ADHD and i was too ored to look up a tool for this job , so yea")

parser.add_argument("Action", help="The action you wanna perform , do Setup to setup ")
parser.add_argument("-l","--log", type=int,help="Set the logging mode")
arguments = parser.parse_args()

match arguments.Action:

        case "Setup":
        
            print("Setup Mode")
            import setup
            setup.initialSetup()

        case "init":
            import initSync
            print("initialising new SyncNode")
            initSync.begin()
        case "sync":
            import sync
            print("Syncing...")
            sync.handle_upload()

    


