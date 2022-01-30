#!python3

from __future__ import print_function

import socket
from threading import Event
import sys
import struct
import pygame
import os
from logging import getLogger
from dcsbios import ProtocolParser, StringBuffer, IntegerBuffer

pygame.init()
pygame.mouse.set_visible(False)
 
screen = pygame.display.set_mode((800, 480))

screen.fill((0,255,0))

pygame.display.update()
