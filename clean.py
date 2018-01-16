#!/usr/bin/env python

import os.path
import shutil

remove_files = ["app.db", "logs/microblog.log", ]
remove_directories = ["logs/", ]
remove_tree = ["migrations/", ]

concat_list = remove_files + remove_directories + remove_tree

for item in concat_list:
    if not os.path.exists(item):
        print("'" + item + "' does not exist.")
    if item in remove_files and os.path.exists(item):
        os.remove(item)
        print("Removed File: " + item)
    if item in remove_directories and os.path.exists(item):
        os.rmdir(item)
        print("Removed Directory: " + item)
    if item in remove_tree and os.path.exists(item):
        shutil.rmtree(item)
        print("Removed Tree: " + item)