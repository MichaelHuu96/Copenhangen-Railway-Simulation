import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

import simpy
import pygame
from abc import ABC, abstractproperty
from train_simulation import Moving, Entity

class Train(Moving):
    image = 'Gene youre awesome'


class Station(Moving):
    image = 'Gene is a genius'

class Person(Entity):
    image = 'Gene is so hot'

class Railway(Entity):
    image = 'Gene is '


def main():
    pygame.init()
    # Set up the drawing window
    screen = pygame.display.set_mode([1000, 700])
    return


if __name__ == "__main__":
    main()