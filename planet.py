# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 2022

A module including a planet class and some functions 

@author: Keanan Scarbro
"""

import random
import math as m

import helpers.vector
import constants
import pygame


class Planet:
    AU = 1.496e+11
    SCALE = 100 / AU

    planet_list = []
    num_of_planets = 0

    def __init__(self, mass, radius, x0, v0, name=None, color=None):
        self.mass = mass
        self.radius = radius
        self.x = helpers.vector.Vector(x0)
        self._x0 = helpers.vector.Vector(x0)
        self.v = helpers.vector.Vector(v0)
        self._v0 = helpers.vector.Vector(v0)

        self.xhistory = []
        self.xhistory.append(self.x)
        self.vhistory = []
        self.vhistory.append(self.v)
        self.thistory = [0]

        if color == None:
            self.color = random.choice(constants.COLOR_LIST)
        else:
            self.color = color

        Planet.num_of_planets += 1
        self.planet_num = Planet.num_of_planets
        if name == None:
            self.name = f'Planet: {self.planet_num}'
        else:
            self.name = name

        Planet.planet_list.append(self)

    def __str__(self):
        return f'Planet{self.planet_num}'

    def reinit(self):
        self.x = self._x0
        self.v = self._v0
        self.xhistory = []
        self.xhistory.append(self.x)
        self.vhistory = []
        self.vhistory.append(self.v)
        self.thistory = [0]

    def move(self):
        self.x += self.v * constants.DT
        self.v += Planet._gravity(self) / self.mass * constants.DT
        self.xhistory.append(self.x)
        self.vhistory.append(self.v)
        self.thistory.append(self.thistory[-1] + constants.DT)

        self._check_collision()

    def draw(self, surface):
        _updated_points = [(item[0] * Planet.SCALE + constants.SCREEN_WIDTH // 2,
                            item[1] * Planet.SCALE + constants.SCREEN_HEIGHT // 2) for item in self.xhistory]
        if len(_updated_points) < 2:
            _updated_points.append(_updated_points[-1])
        elif len(_updated_points) > 150:
            _updated_points = _updated_points[-149:]
        x = self.x[0] * Planet.SCALE + constants.SCREEN_WIDTH // 2
        y = self.x[1] * Planet.SCALE + constants.SCREEN_HEIGHT // 2
        pygame.draw.circle(surface, self.color, (x, y),
                           Planet._rad_scaling(self.radius))
        pygame.draw.lines(surface, self.color, False, _updated_points)
        #surface.blit(constants.COMICSANS_12.render(f'{int(self.v.norm()):.2e} m/s', True, constants.SOFT_WHITE), (x - 30, y - 30))

    @classmethod
    def _gravity(cls, planet):
        G = 6.67e-11  # m^3 kg^-1 s^-2

        m1 = planet.mass
        r1 = planet.x

        vector_sum = helpers.vector.Vector([0, 0, 0])
        for other_planet in cls.planet_list:
            if other_planet is planet:
                continue

            m2 = other_planet.mass
            r2 = other_planet.x
            d = (r1 - r2).norm()
            if d == 0:
                d = .01  # To guard against an infinite force
            # if d < other_planet.radius:
            #    f_mag = G * m1 * m2  * d / other_planet.radius**3
            # else:
            f_mag = G * m1 * m2 / d**2
            f_direction = (r2 - r1).unit_vec()

            vector_sum += f_mag * f_direction
        return vector_sum

    @staticmethod
    def _rad_scaling(radius):
        scaled_radius = 2.5**(m.log10(radius)) / 75
        if scaled_radius > 25:
            scaled_radius = 25
        if scaled_radius < 3:
            scaled_radius = 3
        return scaled_radius

    @classmethod
    def draw_planets(cls, surface, sim_speed):
        for planet in cls.planet_list:
            planet.draw(surface)
            for _ in range(sim_speed):
                if planet not in cls.planet_list:
                    break
                planet.move()

    @classmethod
    def clear(cls):
        del cls.planet_list[:]
        Planet.num_of_planets = 0

    # Similar to __del__, but __del__ is only called after the instance is
    # garbage collected, which happens inconsistently (or not at all)
    def _remove(self):
        Planet.num_of_planets -= 1
        Planet.planet_list = [item for item in Planet.planet_list if item is not self]

    def _check_collision(self):
        # Did it leave the screen
        x = self.x[0] * Planet.SCALE + constants.SCREEN_WIDTH // 2
        y = self.x[1] * Planet.SCALE + constants.SCREEN_HEIGHT // 2
        if (x > constants.SCREEN_WIDTH or x < 0) or (y > constants.SCREEN_HEIGHT or y < 0):
            self._remove()
            return
        # Did it collide with another planet?
        for other_planet in Planet.planet_list:
            if other_planet is self: continue
            if (self.x * Planet.SCALE - other_planet.x * Planet.SCALE).norm() < Planet._rad_scaling(other_planet.radius):
                if self.mass < other_planet.mass:
                    other_planet.mass += self.mass
                    other_planet.radius = (
                        other_planet.radius**3 + self.radius**3)**(1 / 3)
                    other_planet.v = (other_planet.mass * other_planet.v + self.mass * self.v + (Planet._gravity(
                        self) + Planet._gravity(other_planet)) * constants.DT) / (self.mass + other_planet.mass)
                    self._remove()
                else:
                    self.mass += other_planet.mass
                    self.radius = (other_planet.radius**3 +
                                   self.radius**3)**(1 / 3)
                    self.v = (other_planet.mass * other_planet.v + self.mass * self.v + (Planet._gravity(
                        self) + Planet._gravity(other_planet)) * constants.DT) / (self.mass + other_planet.mass)
                    other_planet._remove()
                break       
        
# Load specific default systems
def load_solar_system():
    Planet.clear()
    solar_system = {}
    solar_system['Mercury'] = Planet(3.30E+23, 2.44E+06, [6.98e+10, 0, 0], [
                                     0, 4.74e+04, 0], name="Mercury", color=constants.SOFT_YELLOWGREEN)
    solar_system['Venus'] = Planet(4.87E+24, 6.05E+06, [1.089e+11, 0, 0], [
                                   0, 3.5e+04, 0], name="Venus", color=constants.SOFT_CYAN)
    solar_system['Earth'] = Planet(5.972e24, 6.371e6, [
                                   1.02 * Planet.AU, 0, 0], [0, 2.92e4, 0], name="Earth", color=constants.SOFT_BLUE)
    #solar_system['Moon'] = Planet(7.30E+22, 1.74E+06, [4.06e+08 + solar_system['Earth'].x[0], 0, 0], [0, 1.0e+03 + solar_system['Earth'].v[1], 0], name = "Moon")
    solar_system['Mars'] = Planet(6.42E+23, 3.40E+06, [2.493e+11, 0, 0],
                                  [0, 2.41e+04, 0], name="Mars", color=constants.SOFT_RED)
    #solar_system['Jupiter'] = Planet(1.90E+27, 7.15E+07, [8.164e+11, 0, 0], [0, 1.31e+04, 0], name = "Jupiter")
    #solar_system['Saturn'] = Planet(5.68E+26, 6.03E+07, [1.5065e+12, 0, 0], [0, 9.7e+03, 0], name = "Saturn")
    #solar_system['Uranus'] = Planet(8.68E+25, 2.56E+07, [3.0014e+12, 0, 0], [0, 6.8e+03, 0], name = "Uranus")
    #solar_system['Neptune'] = Planet(1.02E+26, 2.48E+07, [4.5589e+12, 0, 0], [0, 5.4e+03, 0], name = "Neptune")
    #solar_system['Pluto'] = Planet(1.30E+22, 1.19E+06, [7.3759e+12, 0, 0], [0, 4.7e+03, 0], name = "Pluto")
    solar_system['Sun'] = Planet(1.989e30, 6.96e8, [0, 0, 0], [
                                 0, 0, 0], name="Sun", color=constants.SOFT_YELLOW)

    return solar_system

