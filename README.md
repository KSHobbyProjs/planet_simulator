# PLANET SIMULATOR

Developers: Keanan Scarbro

Version: Alpha 1.0 <br>
Date: 8/16/2022

___
## DESCRIPTION

This game is a mock universe sandbox.

It uses Newtonian gravity to simulate the behavior of the planets. The default setup is the solar system, but the game allows you to make more planets upon clicking
___
## HOW TO DOWNLOAD:

Download with gut via git clone 

___
## HOW TO USE:

IMPORTANT: <br>
The game uses real values for the position, velocity, and radius of each planet to calculate the gravity. However, in the live simulation, the position is scaled (by 100 / AU), so that the orbits can fit in the window. 
The radii of the planets displayed are calculated using an arbitrary formula (_rad_scaling in planet.Planet). This means that the radii of the planets displayed is no where near the true radius (based on the 100 / AU position
scaling). The true (position-scaled) radii are actually incredibly small (less than one pixel). This makes sense; the radii of the planets are infinitesmal compared to the orbital distance, afterall. The collision detection is set
to trip when a planet enters the fake-radius set by the _rad_scaling function. This can be altered to trip when a planets is within the true (position-scaling) radius by altering the _check_collision method in the planet.Planet 
class (not recommended). But, this means that the planets will almost never trip the detection function. Instead, the _check_collision function should be altered, so that the collision is tripped at a smaller radius, or the 
_rad_scaling function should be altered (this affects the displayed size of the planets). Also, a planet is deleted once it leaves the current pygame window, but this can also be changed within _check_collision.

The timestep is set to 1 day (60 * 60 * 24 seconds), so the duration is set in days (for _ in range(duration): move(dt)). This means that the restart dump and output dump values in the config file correspond to days as well.
___

## TODO
- Fix this README. It doesn't even detail how to use the damn program.
- Overhaul the way the gravity function works. Currently, it calculates the gravity on a planet by cycling through each of the other planets and calculating the force vector. This function is then called for each planet. Due to Newton's 
third law, this is unnecessary. It would be better to calculate the force on one planet due to another, then automatically add equal and opposite this force to the other planet. This would split the computational time approximately in half.
Plus, it would solve issues where the force on planet A due to planet B is easy to calculate, but the force on planet B by planet A isn't. With Newton's third law, we need not even calculate the force on planet B by planet A directly;
we just use what we calculated earlier.

- Add right click mechanic to control other attributes of the planets

- Add future path of planet [once the program detects the mouse being dragged, store the current x and v history, call the move method numerous times (within the main loop), draw the lines representing the planet in questions future 
path; once the mouse is let go, revert back to the stored x and v values, and let the planet go. It should follow the future path]

- Move to 3D
___

## AUTHOR
Name: Keanan Scarbro <br>
Email: scarbro.kms1@gmail.com

It's August 2022, and I'm currently a physics major going into my senior year at North Carolina State University. I'm applying for graduate school in physics, and I plan to conduct research on quantum gravity (childish ambition) 
upon receiving my P.H.D.
