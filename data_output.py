# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 2022

A module to handle the plots and data output of the simulation

@author: Keanan Scarbro
"""

import matplotlib.pyplot as plt
import pandas as pd
import json  # I could have just used eval, but knowing json is helpful
import datetime
import os

import planet
import constants


def extract():
    begin_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    # Reinitialize planets (initial position and history) in case the loaded planets have previous (x,v,t)history
    for planet_ in planet.Planet.planet_list:
        planet_.reinit()

    if constants.CONFIG['RESTART'] != 'none':
        file_index, time_offset = _restart()
        # Update the hst file with the current process of the sim
        _update_hst_file(
            f"Restarting from {constants.CONFIG['NAME']}_{constants.CONFIG['RESTART']} at {begin_time}\n")
    else:
        # Index keeping track of what output file number we're on and an offset to keep track of the time after restarts
        file_index, time_offset = 0, 0
        # Removing the hst file if it exists (since we're not restarting) and writing when the sim started
        if os.path.exists(f"output/{constants.CONFIG['NAME']}.hst"):
            os.remove(f"output/{constants.CONFIG['NAME']}.hst")
        _update_hst_file(
            f"{constants.CONFIG['NAME']} started on {begin_time}\n")

    # Letters keeping track of what restart file we're on
    restart_letters = constants.CONFIG['RESTART']
    for i in range(constants.CONFIG['DURATION'] + 1 - time_offset):
        if i % constants.CONFIG['OUTPUT'] == 0 or i == constants.CONFIG['DURATION']:
            file_index = _output(file_index)
        if i % constants.CONFIG['DUMP'] == 0 and i != 0:
            restart_letters = _dump(
                restart_letters, file_index, i + time_offset)
        for planet_ in planet.Planet.planet_list:
            planet_.move()

    _update_hst_file(
        f"=Finished writing on {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
    _update_hst_file("\n----------------------------------------\n")
    _plot()


def _restart():
    # Clear the preset-loaded planets (probably the solar system)
    planet.Planet.clear()

    # Create a pandas dataframe with the stored data present in the restart file, and recreate the previous system
    df = pd.read_csv(
        f"restart/{constants.CONFIG['NAME']}_{constants.CONFIG['RESTART']}.csv", delimiter=';')
    for i in range(len(df.index)):
        p = planet.Planet(df['mass'].tolist()[i], df['radius'].tolist()[i], json.loads(
            df['xhistory'][i])[-1], json.loads(df['vhistory'][i])[-1], name=df['name'][i], color=eval(df['color'][i]))
        p.xhistory = json.loads(df['xhistory'][i])
        p.vhistory = json.loads(df['vhistory'][i])
        p.thistory = json.loads(df['thistory'][i])

    # Read the file_index and time_offset for the current sim in the hst file
    file_index, time_offset = _read_hst_file()

    return file_index, time_offset


def _output(file_index):
    for planet_ in planet.Planet.planet_list:
        df = pd.DataFrame({'time': planet_.thistory,
                           'x': [x[0] for x in planet_.xhistory],
                           'y': [x[1] for x in planet_.xhistory],
                           'z': [x[2] for x in planet_.xhistory],
                           'r': [(x[0]**2 + x[1]**2 + x[2]**2)**.5 for x in planet_.xhistory],
                           'rho': [(x[0]**2 + x[1]**2)**.5 for x in planet_.xhistory],
                           'v': [(v[0]**2 + v[1]**2 + v[2]**2)**.5 for v in planet_.vhistory]
                           })
        df.columns.name = f'{planet_.name}'
        df.to_string(
            f"output/{constants.CONFIG['NAME']}_{file_index}_{planet_.__str__()}.dat")
    file_index += 1
    return file_index


def _dump(restart_letters, file_index, i):
    new_restart_letters = _increment_char(restart_letters)

    planet_info = {'name': [planet_.name for planet_ in planet.Planet.planet_list],
                   'color': [planet_.color for planet_ in planet.Planet.planet_list],
                   'mass': [planet_.mass for planet_ in planet.Planet.planet_list],
                   'radius': [planet_.radius for planet_ in planet.Planet.planet_list],
                   'xhistory': [planet_.xhistory for planet_ in planet.Planet.planet_list],
                   'vhistory': [planet_.vhistory for planet_ in planet.Planet.planet_list],
                   'thistory': [planet_.thistory for planet_ in planet.Planet.planet_list]
                   }
    df = pd.DataFrame(planet_info)
    df.to_csv(
        f"restart/{constants.CONFIG['NAME']}_{new_restart_letters}.csv", sep=';')

    # Write to history file the file_index and the current time
    _update_hst_file(
        f"={new_restart_letters}=\n\tDumped on file {file_index}\n\tDumped on day {i}\n")

    return new_restart_letters


def _update_hst_file(str_):
    with open(f"output/{constants.CONFIG['NAME']}.hst", 'a') as f:
        f.write(str_)


def _increment_char(letters):
    if letters == 'none':
        return 'aa'

    first_letter = letters[0]
    second_letter = letters[1]

    if second_letter == 'z':
        if first_letter == 'z':
            raise Exception("Maximum number of restart files reached")
        else:
            first_letter = chr(ord(first_letter) + 1)
            second_letter = 'a'
    else:
        second_letter = chr(ord(second_letter) + 1)

    return first_letter + second_letter


def _read_hst_file():
    with open(f"output/{constants.CONFIG['NAME']}.hst") as f:
        impo_lines = f.read().split('=')
        restart_index = [i for i, item in enumerate(
            impo_lines) if item == constants.CONFIG['RESTART']][-1]
        file_index = int(
            impo_lines[restart_index + 1].split('\n\t')[1].split(' ')[-1])
        time_offset = int(
            impo_lines[restart_index + 1].split('\n\t')[2].split(' ')[-1].replace('\n', ''))
    return file_index, time_offset


def _plot():
    # Initialize figures and axes
    i = 0
    while True:
        fig, axs = plt.subplots(ncols = 3, nrows = 2, figsize = (5.5, 3.5), constrained_layout = True)
        fig3d = plt.figure()
        ax3d = fig3d.add_subplot(projection = '3d')
        j = 1
        while True:
            with open(f"output/{constants.CONFIG['NAME']}_{i}_Planet{j}.dat", "r") as f:
                lines = f.readlines()
                name = lines[0].split()[0]
                t = [float(line.split()[1]) / (60**2 * 24)
                     for line in lines[1:]]
                x = [float(line.split()[2]) /
                     planet.Planet.AU for line in lines[1:]]
                y = [float(line.split()[3]) /
                     planet.Planet.AU for line in lines[1:]]
                z = [float(line.split()[4]) /
                     planet.Planet.AU for line in lines[1:]]
                r = [float(line.split()[5]) /
                     planet.Planet.AU for line in lines[1:]]
                rho = [float(line.split()[6]) /
                       planet.Planet.AU for line in lines[1:]]
                v = [float(line.split()[7]) * 60**2 * 24 /
                     planet.Planet.AU for line in lines[1:]]

            # Create subplots with data
            ax3d.plot(x, y, z, label = name)
            
            axs[0, 0].plot(x, y, '.', label = name)
            axs[0, 0].set_title(r'$y$ vs $x$')
            axs[0, 0].set_xlabel(r'$y$ distance (AU)')
            axs[0, 0].set_ylabel(r'$x$ distance (AU)')

            axs[0, 1].plot(t, x, '.', label = name)
            axs[0, 1].set_title(r'$x$ vs $t$')
            axs[0, 1].set_ylabel(r'$x$ distance (AU)')
            axs[0, 1].set_xlabel('Time (days)')

            axs[0, 2].plot(t, r, '.', label = name)
            axs[0, 2].set_title(r'$r$ vs $t$')
            axs[0, 2].set_ylabel(r'$r$ distance (AU)')
            axs[0, 2].set_xlabel('Time (days)')

            axs[1, 0].plot(t, rho, '.', label = name)
            axs[1, 0].set_title(r'$\rho$ vs $t$')
            axs[1, 0].set_ylabel(r'$\rho$ distance (AU)')
            axs[1, 0].set_xlabel('Time (days)')

            axs[1, 1].plot(t, v, '.', label = name)
            axs[1, 1].set_title(r'$v$ vs $t$')
            axs[1, 1].set_ylabel('Velocity (AU/day)')
            axs[1, 1].set_xlabel('Time (days)')

            j += 1
            if not os.path.exists(f"output/{constants.CONFIG['NAME']}_{i}_Planet{j}.dat"): break

        fig.suptitle(f"{constants.CONFIG['NAME']} data")
        fig.show()
        fig3d.show()
        
        i += 1
        if not os.path.exists(f"output/{constants.CONFIG['NAME']}_{i}_Planet1.dat"):
            break
