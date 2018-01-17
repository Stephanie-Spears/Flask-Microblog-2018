#!/usr/bin/env python

import os.path
import shutil

remove_files = ["app.db", ]
remove_tree = ["migrations/", "logs/", ]

concat_list = remove_files  + remove_tree

for item in concat_list:
    if not os.path.exists(item):
        print("'" + item + "' does not exist.")
    if item in remove_files and os.path.exists(item):
        os.remove(item)
        print("Removed File: " + item)
    if item in remove_tree and os.path.exists(item):
        shutil.rmtree(item)
        print("Removed Tree: " + item)

