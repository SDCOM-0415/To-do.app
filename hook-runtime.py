#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Todo App v0.3.1 - PyInstaller Runtime Hook
Ensures tkinter loads correctly in packaged environment
"""

import os
import sys

# If running in packaged environment, set correct TCL/TK paths
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
    
    # Try multiple possible paths
    possible_tcl_paths = [
        os.path.join(base_dir, '_tcl_data', 'tcl8.6'),  # Primary path
        os.path.join(base_dir, 'tcl', 'tcl8.6'),        # Backup path 1
        os.path.join(base_dir, 'tcl')                   # Backup path 2
    ]
    
    possible_tk_paths = [
        os.path.join(base_dir, '_tcl_data', 'tk8.6'),   # Primary path
        os.path.join(base_dir, 'tk', 'tk8.6'),          # Backup path 1
        os.path.join(base_dir, 'tk')                    # Backup path 2
    ]
    
    # Find valid TCL path
    for tcl_path in possible_tcl_paths:
        if os.path.exists(tcl_path):
            os.environ['TCL_LIBRARY'] = tcl_path
            print(f"Set TCL_LIBRARY={tcl_path}")
            break
    
    # Find valid TK path
    for tk_path in possible_tk_paths:
        if os.path.exists(tk_path):
            os.environ['TK_LIBRARY'] = tk_path
            print(f"Set TK_LIBRARY={tk_path}")
            break
    
    # Print debug information
    print(f"MEIPASS path: {base_dir}")
    print(f"Current TCL_LIBRARY: {os.environ.get('TCL_LIBRARY', 'Not set')}")
    print(f"Current TK_LIBRARY: {os.environ.get('TK_LIBRARY', 'Not set')}")
