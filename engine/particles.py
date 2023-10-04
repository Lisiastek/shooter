import engine.basic as basic
import pygame
from pygame.math import Vector2

import abc
import sys
from random import randint
import copy


import numpy as np

def genParticles(scene, image, number, pos, *args, **kwargs):

    # kwargs


    # spread Area kwargs
    if 'spreadAreax' in kwargs:
        spreadAreax = 40
    else:
        spreadAreax = 40

    if 'spreadAreay' in kwargs:
        spreadAreay = 40
    else:
        spreadAreay = 40


    # for set one direction in random spread
    if 'alwaysXSign' in kwargs:
        if kwargs['alwaysXSign'] == '+' or kwargs['alwaysXSign'] == '-' or 'not':
            alwaysXSign = kwargs['alwaysXSign']
        else:
            raise Exception('Invalid AlwaysXSign kwarg')
    else:
        alwaysXSign = 'not'

    if 'alwaysYSign' in kwargs:
        if kwargs['alwaysYSign'] == '+' or kwargs['alwaysYSign'] == '-' or 'not':
            alwaysYSign = kwargs['alwaysYSign']
        else:
            raise Exception('Invalid AlwaysYSign kwarg')
    else:
        alwaysYSign = 'not'







    randPosListX = np.random.randint(0, spreadAreax, number)
    randPosListY = np.random.randint(0, spreadAreay, number)



    for i in range(number):

        # randPosListX[i] += pos.x
        #
        # randPosListY[i] += pos.y

        normalParticle(scene, image, (randPosListX[i] + pos.x, randPosListY[i] + pos.y), *args, **kwargs)



class normalParticle(basic.AdvancedElement):
    @abc.abstractmethod
    def loop3(self, *args, **kwargs):
        pass

    def loop2(self, *args, **kwargs):
        if self.particle_time < 0:
            self.kill()
        else:
            self.particle_time -= 1
            size = (self.image.get_width() - (self.image.get_width() * self.particle_psmal /100) ,
                    self.image.get_height() - (self.image.get_height() * self.particle_psmal / 100))
            # print(self.image.get_width())
            # sys.exit()
            self.image = pygame.transform.smoothscale(self.image, (size)).convert_alpha()


            self.pos += self.particle_pdirection
            self.update()

        self.loop3(args, kwargs)

    def __init__(self, scene, image, cords, group="NO", *args, **kwargs):
        super().__init__(scene, image, cords, group="NO", *args, collision=False, **kwargs)


        # time how long particle exist
        if 'time' in kwargs:
            self.particle_time = int(kwargs['time'])
        else:
            self.particle_time = 60


        # time how much particle getting smaller
        if 'psmal' in kwargs:
            self.particle_psmal = int(kwargs['psmal'])
        else:
            self.particle_psmal = 1

        # direction of particle
        if 'pdirection' in kwargs:
            self.particle_pdirection = kwargs['pdirection']
        else:
            self.particle_pdirection = Vector2(0, -1)

