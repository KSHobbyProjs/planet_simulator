# PLANET SIMULATOR

Developers: Keanan Scarbro

Version: Alpha 1.0 <br>
Date: 8/16/2022 <br>
Updated Date: 2/19/2025

___
## DESCRIPTION
This game is a mock universe sandbox.

It uses Newtonian gravity to simulate the trajectory of planets given initial conditions. There are three modes. In Mode 1, the program runs a simulation of the planets over time, and data on the positions and velocities of the planets over time is output in the form of plots and data files. Mode 2 is an interactive game. Here, one can create planets and watch them interact. Mode 3 is a combination of Mode 1 and Mode 2. In Mode 3, the program outputs position and velocity data based on what was done during the live simulation.
___
## HOW TO DOWNLOAD:
Download with git via "git clone https://github.com/KSHobbyProjs/planet_simulator.git"

___
## DEPENDENCIES:
Python
  - matplotlib (download in your local Python environment with pip via "pip install matplotlib")
  - pygame     (download in your local Python environment with pip via "pip install pygame")
  - pandas     (download in your local Python environment with pip via "pip install pandas")

## HOW TO USE:
The program is configured with `config.txt`, and the program is run with `main.py`. Data on planet positions and velocities over time is printed in the form of .dat files into an `output` directory. Dump files are printed as .pkl files into the `restart` directory; these files allow you to start a new simulation from a save point of a previous simulation. 

### config.txt
The config.txt file determines how the program runs. This needs to be configured before running the program. The config.txt file is setup in the following way:
  - 'NAME'      : '[the name of your simulation]',
  - 'RESTART'   : [which dump file, if any, should the program grab its initial data from]
  - 'OUTPUT'    : [how often data is output; e.g. 'OUTPUT' : 300 would output data files every 300 days]
  - 'DUMP'      : [how often the simulation is saved; e.g. 'DUMP' : 300 would dump simulation state data every 300 days] 
  - 'DURATION'  : [the length of the simulation in days]
  - 'DIMENSION' : [2D or 3D]
  - 'MODE'      : [1: data output only, 2: live simulation only, or 3: data output and live simulation] 

### main.py
After configuring the config.txt file, run the program by executing main.py with whichever Python interpreter you choose.

### output
If you chose Mode 1 or Mode 3, the data output files will be printed into the `output` directory. The data files have the form `[NAME]_[OUTPUTNUM]_[PLANETNAME].dat`, where NAME is the name of your simulation as set in the config.txt file, OUTPUTNUM is the number of the output cycle the data corresponds to, and PLANETNAME is the name of the planet that the data corresponds to (example: SolarSim_3_Mercury.dat). The .dat files are structured in columns. The first column gives the number of clock cycles that have passed; the second column gives the time at each cycle; the next three columns give the x, y, and z positions of the planet, respectively; the sixth column gives the planet's radial distance from the origin; the seventh column gives the planet's radial distance from the origin projected onto the x-y plane; and the last column gives the speed of the planet. All data uses meters for position and seconds for time.

The program also prints a `[NAME].hst` file in the `output` directory that includes simulation diagnostic information like when the simulation was started, when output files were printed, when dump files were printed, and when the simulation finished. 

### restart
If Mode 1 or Mode 3 were chosen, dump files will be stored in the `restart` directory. Dump files contain the simulation state at the time of outputting the dump file. These files have the form `[NAME]_[DUMPCHAR].pkl`, where DUMPCHAR is the tag representing which dump cycle the file belongs to (example: SolarSim_aa.pkl). DUMPCHARs start at 'aa' and move through the alphabet one letter at a time, starting with the first letter. `'RESTART'  : '[DUMPCHAR]'` in the `config.txt` file can then be used to start a new simulation using the simulation state of an old simulation (example: "'RESTART' : ac"). Use `'RESTART' : 'none'` if starting with no dump file.

___
IMPORTANT: <br>
The game uses real values for the position, velocity, and radius of each planet to calculate the gravity. However, in the live simulation, orbital distances are scaled by 100 / AU, so that the orbits can fit in the window. The scale can be changed at the header of the `Planet` class found within `planet.py`. The radii of the planets displayed are not scaled to 100 / AU (if they were, the planets would be less than a pixel wide); instead, the radii are scaled according to an arbitrary function `_rad_scaling` found in the `Planet` class of the `planet.py` module. The collision detection is set to trip when a planet enters the scaled-radius set by the _rad_scaling function. This can be changed with `_check_collision` found within the `Planet` class of the `planet.py` module. A planet is deleted once it leaves the current pygame window; this can also be changed with `_check_collision`.

The timestep is set to 1 day (60 * 60 * 24 seconds). This can be changed at the bottom of `constants.py`. The 'DURATION', 'RESTART' and 'OUTPUT' fields in the `config.txt` file are in units determined by the timestep. 

The width and height of the screen for the live simulation can be altered in `constants.py`.

To change the initial planetary setup, change the function `load_solar_system` found at the bottom of the `planet.py` module. Alternatively, add a new function at the bottom of the `planet.py` module, and call this function at the beginning of the main method in `main.py`.
___

## TODO
- Fix dump and restart capabilities (and use pickle instead of .csv)
- Make it easier to configure initial setups. Right now, users have to go into the planet.py module and either overwrite the 'load_solar_system()' function, or create a new function which would then need to be called in 'main()'.
- Add right click mechanic to control other attributes of the planets in the form of a drop-down menu
- Output more statistics. Output the motion of and about the COM and maybe some measure of the overall stability of the system. Right now, the simulation plots many pictures once the simulation is complete, but it doesn't save them. Fix that.
- Add future path of planet
  - Once the program detects the mouse being dragged, store the current x and v history, call the move method numerous times (within the main loop), draw the lines representing the planet's future path and store this path; once the mouse is let go, revert back to the stored x and v values.
- Add 3D functionality
- ~~Overhaul the way the gravity function works. Due to treating each planet as an object and pygame requirements, it was easier for me to calculate the force on each planet individually. It'd be better to calculate the force on a planet due to all of the other planets, then update the force that the other planets feel. I beleive I've done thus, but I keep this here for posterity.~~ I looked into it. I didn't overhaul the gravity. I remember now that I found out that this is much more intense a task than I thought it would be. Since, at each clock cycle, all planets are looped over, and within the planet class, the force is calculated by once again looping over all planets, I'd need to transfer the history of the force data to each planet and keep this in that planet's history so that it's still there when it is its turn in both loops. This is just not how i have this set up. It's possible, but tedious, and it would hinder readability (it also may not be nearly as computationally efficient as I think. Theoretically, it'd cut the number of operations in half, but given all the extra steps, that might not be much faster. Given that this is more a game than a true simulation environment, I probably won't end up doing this, but I keep it here as a strikethrough for posterity.
___

## AUTHOR
Name: Keanan Scarbro <br>
Email: scarbro.kms1@gmail.com

It's August 2022, and I'm currently a physics major going into my senior year at North Carolina State University. I'm applying for graduate school in physics, and I plan to conduct research on quantum gravity (childish ambition) 
upon receiving my P.H.D.

Update: It's February 2025. I'm a physics major in my second year in graduate school at North Carolina State University. I plan to conduct research on unification theories and BSM.
