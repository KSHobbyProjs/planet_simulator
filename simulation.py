# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 2022

A module to handle the live simulation of the planets

@author: Keanan Scarbro
"""

import pygame
import math

import constants
import planet

def run_simulation():
    # Reinitialize planets to their default attributes
    for planet_ in planet.Planet.planet_list: planet_.reinit()
    
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Planet Simulation')
    SCREEN = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    
    # Loop vars
    loop_counter = 0 # How many times has the loop looped (over the planet.move() function)
    loop_vars = {'run': True, 'sim_speed': 1, 'mass': 5.972e24, 'radius': 6.371e6}
    # Main loop
    while loop_vars['run']:
        clock.tick(60)
        
        # Initial drawings
        SCREEN.fill(constants.SOFT_BLACK)
        SCREEN.blit(constants.COMICSANS_18.render(f'{loop_counter * constants.DT // (60 * 60 * 24 * 365)} years', True, constants.SOFT_WHITE), (10, 10))
        planet.Planet.draw_planets(SCREEN, loop_vars['sim_speed'])
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop_vars['run'] = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop_vars['run'] = False
                elif event.key == pygame.K_s:
                    loop_vars['sim_speed'] += 1
                    if loop_vars['sim_speed'] > 5: loop_vars['sim_speed'] = 1
                elif event.key == pygame.K_p:
                    loop_vars['sim_speed'] = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    xpos = pygame.mouse.get_pos()[0]
                    ypos = pygame.mouse.get_pos()[1]
                    xinit = (xpos - constants.SCREEN_WIDTH // 2) / planet.Planet.SCALE
                    yinit = (ypos - constants.SCREEN_HEIGHT // 2) / planet.Planet.SCALE
                elif event.button == 3:
                    loop_vars['mass'] *= 5
                    loop_vars['radius'] = ( (3 * loop_vars['mass']) / (4 * math.pi * 5515) )**(1 / 3)
                    if loop_vars['mass'] > 1e33:
                        loop_vars['mass'] = 5.972e24
                        loop_vars['radius'] = 6.371e6
            elif event.type == pygame.MOUSEBUTTONUP:   
                if event.button == 1:
                    xfin = (pygame.mouse.get_pos()[0] - constants.SCREEN_WIDTH // 2) / planet.Planet.SCALE
                    yfin = (pygame.mouse.get_pos()[1] - constants.SCREEN_HEIGHT // 2) / planet.Planet.SCALE
                    planet.Planet(loop_vars['mass'], loop_vars['radius'], [xinit, yinit, 0], _calculate_velocity((xinit, yinit), (xfin, yfin)))
        
        # As long as the mouse button is pressed, draw a line where you drag. This (the left mouse button being held) can only
        # ever happen after it's been pressed once, so it's ok for it to be outside of the main event handler
        if pygame.mouse.get_pressed()[0]:            
            pygame.draw.line(SCREEN, constants.SOFT_WHITE, (xpos, ypos), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), width = 3)
            pygame.draw.circle(SCREEN, constants.SOFT_WHITE, (xpos, ypos), 5)
        
        # Draw a mini planet in the top right corner to represent the current planet size selected
        pygame.draw.circle(SCREEN, constants.SOFT_WHITE, (constants.SCREEN_WIDTH - 30, 33), int(math.log(loop_vars['radius'])))
        SCREEN.blit(constants.COMICSANS_18.render(f"Mass: {loop_vars['mass']:.2e}", True, constants.SOFT_WHITE), (constants.SCREEN_WIDTH - 200, 10))
        SCREEN.blit(constants.COMICSANS_18.render(f"Radius: {loop_vars['radius']:.2e}", True, constants.SOFT_WHITE), (constants.SCREEN_WIDTH - 200, 30))
        # Update screen
        pygame.display.update()
        loop_counter += 1 * loop_vars['sim_speed'] # Multiplying by sim speed because this is the number of times planet.move() is called for each planet
    pygame.quit()


def _calculate_velocity(init_coods, fin_coods):
    dx, dy = (fin_coods[0] - init_coods[0], fin_coods[1] - init_coods[1])
    ds = (dx**2 + dy**2)**.5
    mag = ds * planet.Planet.SCALE * 1e2
    if ds == 0: return [0, 0, 0]
    return [-1 * (dx / ds) * mag, -1 * (dy / ds) * mag, 0]
    