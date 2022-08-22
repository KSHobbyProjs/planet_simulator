# -*- coding: utf-8 -*-
"""
A module to handle the external constants used in the planet_simulation module.
Not necessary and probably bad practice to export so few constants to a whole 
new module, but I wanted to practice it.

@author: Keanan Scarbro
"""

import helpers.configure
import pygame

# Screen params
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 750

# Colors
# Primary colors
#RED = (255, 0, 0)
#GREEN = (0, 255, 0)
#BLUE = (0, 0, 255)
# Secondary colors
#YELLOW = (255, 255, 0)
#CYAN = (0, 255, 255)
#MAGENTA = (255, 0, 255)
# Tertiary colors
#ORANGE = (255, 128, 0)
#YELLOWGREEN = (128, 255, 0)
#GREENCYAN = (0, 255, 128)
#CYANBLUE = (0, 128, 255)
#BLUEMAGENTA = (128, 0, 255)
#MAGENTARED = (255, 0, 128)
# Extreme colors
#WHITE = (255, 255, 255)
#BLACK = (0, 0, 0)



# Primary colors
SOFT_RED = (255, 153, 153)
SOFT_GREEN = (191, 227, 180)
SOFT_BLUE = (147, 202, 237)
# Secondary colors
SOFT_YELLOW = (244, 241, 134)
SOFT_CYAN = (114, 255, 255)
SOFT_MAGENTA = (255, 129, 255)
# Tertiary colors
SOFT_ORANGE = (255, 204, 153)
SOFT_YELLOWGREEN = (176, 255, 97)
SOFT_GREENCYAN = (108, 255, 182)
SOFT_CYANBLUE = (102, 179, 255)
SOFT_BLUEMAGENTA = (191, 127, 255)
SOFT_MAGENTARED = (255, 98, 177)
# Extreme colors
SOFT_WHITE = (230, 230, 230)
SOFT_BLACK = 	(43, 43, 43)

COLOR_LIST = [SOFT_RED, SOFT_GREEN, SOFT_BLUE, SOFT_YELLOW,\
              SOFT_CYAN, SOFT_MAGENTA, SOFT_ORANGE, SOFT_YELLOWGREEN,\
              SOFT_GREENCYAN, SOFT_CYANBLUE, SOFT_BLUEMAGENTA,\
              SOFT_MAGENTARED]

# Timestep
DT = 60 * 60 * 24

# Configure constants
CONFIG = helpers.configure.configure()

# Pygame
pygame.init()
# Fonts
COMICSANS_18 = pygame.font.SysFont('comicsans', 18)
COMICSANS_12 = pygame.font.SysFont('comicsans', 12) 