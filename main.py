# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 2022

A 2D planet simulation using the law of gravitation (n-body problem)

@author: Keanan Scarbro
"""

import constants
import planet
import data_output
import simulation

def main():
    planet.load_solar_system()
    
    if constants.CONFIG['MODE'] != 1:
        simulation.run_simulation()
        
    if constants.CONFIG['MODE'] != 2: 
        data_output.extract()
        
if __name__ == '__main__':
    main()