# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 16:54:03 2018

@author: Mathu_Gopalan
"""

import argparse, os
import helper as h
import logging as lg

def main():
    parser = argparse.ArgumentParser(description='Export the GA metrics and \
                                     dimensions as csv')
    parser.add_argument('config_path', nargs='*', action="store", default="./config,ini", 
                        help = "mention the config file path")
    parser.add_argument('--sftp', dest="sft", action="store", default="sftp", 
                        help ="The data is stored in sftp")
    parser.add_argument('--save_dir', dest="save_dir", action="store", default="./output/", 
                        help = "The data is stored in local machine")
    
    pa = parser.parse_args()
    config_path = pa.config_path
    method = 
    View = ["15425",""]
    h.getrepor(view, metric, dime, data)