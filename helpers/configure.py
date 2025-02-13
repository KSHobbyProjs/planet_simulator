# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 2022

A helper module dedicated to initiating the configure file

@author: Keanan Scarbro
"""

def configure():
    with open('./config.txt', 'r') as configure_file:
        CONFIG = eval(configure_file.read())
    return CONFIG