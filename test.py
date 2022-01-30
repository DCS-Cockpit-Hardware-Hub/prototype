#!python3

from __future__ import print_function

import socket
from threading import Event
import sys
import struct
import pygame
import pygame_gui
import os
from logging import getLogger
from dcsbios import ProtocolParser, StringBuffer, IntegerBuffer

pygame.init()
pygame.mouse.set_visible(False)
 
window_surface = pygame.display.set_mode((800, 480))
background = pygame.Surface((800, 480))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 480))

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                            text='Say Hello',
                                            manager=manager)

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
