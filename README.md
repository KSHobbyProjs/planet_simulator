# PLANET SIMULATOR

Developers: Keanan Scarbro

Version: Alpha 1.0 <br>
Date: 8/16/2022
Updated Date: 2/19/2025

___
## DESCRIPTION
This game is a mock universe sandbox.

It uses Newtonian gravity to simulate the behavior of the planets. There are three modes. In Mode 1, a simulation of the N-body graviation is run with initial planet information that you provide. Data on the positions and velocities of the planets over time is output in the form of plots and data files. Mode 2 is an interactive game. Here, one can create new planets and watch them interact. Mode 3 is a combination of Mode 1 and Mode 2. In Mode 3, the program outputs position and velocity data based on what you did during the live simulation.
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
The program is configured with 'config.txt', and the program is run with 'main.py'. Data on planet positions and velocities is printed in the form of '.dat' files into an 'output' directory. Restart files are printed as '.pkl' files into the 'restart' directory; these files allow you to start a new simulation from a save point of a previous simulation. 

### config.txt
The config.txt file determines how the program runs. This needs to be configured before running the program. The config.txt file is setup in the following way:
  - 'NAME'      : '[the name of your simulation]',
  - 'RESTART'   : [which dump file, if any, should the program grab its initial data from]
  - 'OUTPUT'    : [how often data is output; e.g. 'OUTPUT' : 300 would output data files every 300 days]
  - 'DUMP'      : [how often the simulation is saved; e.g. 'DUMP' : 300 would dump simulation data ever 300 days] 
  - 'DURATION'  : [the length of the simulation in days]
  - 'DIMENSION' : [2D or 3D]
  - 'MODE'      : [1: data output only, 2: live simulation only, or 3: data output and live simulation] 

### main.py
After configuring the config.txt file, run the program by executing main.py with whichever Python interpreter you choose. The 'output' directory will contain the data output from the simulation, and the 'restart' directory will contain all dump files.

### output
If you chose Mode 1 or Mode 3, the data output files will be printed into the 'output' directory. The data files have the form 'NAME_DUMPNUM_PLANETNAME.dat', where NAME is the name of your simulation as set in the config.txt file, DUMPNUM is the number representing which dump cycle the data corresponds to, and PLANETNAME is the name of the planet that the data corresponds to. The .dat files are structured in columns. The first column gives the number of clock cycles that have passed; the second column gives the time at each cycle; the next three columns give the x, y, and z positions of the planet, respectively; the sixth column gives the planet's radial distance from the origin; the seventh column gives the planet's radial distance from the origin projected onto the x-y plane; and the last column gives the speed of the planet. All data uses meters for position and seconds for time.

The program also prints a 'NAME.hst' file in the 'output' directory that includes simulation diagnostic information like when the simulation was started, when output files were printed, when dump files were printed, and when the simulation finished. 

### restart
If Mode 1 or Mode 3 were chosen, and 'DUMP' in the config.txt file was given a , the dump files will be stored in the 'restart' directory. These files provide a 



___
IMPORTANT: <br>
The game uses real values for the position, velocity, and radius of each planet to calculate the gravity. However, in the live simulation, the position is scaled (by 100 / AU), so that the orbits can fit in the window. The radii of the planets displayed are calculated using an arbitrary formula (_rad_scaling in planet.Planet). This means that the radii of the planets displayed is no where near the true radius (based on the 100 / AU position scaling). The true (position-scaled) radii are actually incredibly small (less than one pixel). This makes sense; the radii of the planets are infinitesmal compared to the orbital distance, afterall. The collision detection is set to trip when a planet enters the fake-radius set by the _rad_scaling function. This can be altered to trip when a planets is within the true (position-scaling) radius by altering the _check_collision method in the planet.Planet class (not recommended). But, this means that the planets will almost never trip the detection function. Instead, the _check_collision function should be altered, so that the collision is tripped at a smaller radius, or the _rad_scaling function should be altered (this affects the displayed size of the planets). Also, a planet is deleted once it leaves the current pygame window, but this can also be changed within _check_collision.

The timestep is set to 1 day (60 * 60 * 24 seconds), so the duration is set in days (for _ in range(duration): move(dt)). This means that the restart dump and output dump values in the config file correspond to days as well.
___

## TODO
- Update README
- Fix dump and restart capabilities (and use pickle instead of .csv)
- Make it easier to configure initial setups. Right now, users have to go into the planet module and either overwrite the 'load_solar_system()' function, or create a new function which would then need to be called in 'main()'.
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
