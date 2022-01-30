#!python3

from __future__ import print_function

SEND_ADDR = ('192.168.1.203', 7778)
RECV_ADDR = ('', 5010)
MULTICAST_IP = '239.255.50.10'

import socket
from threading import Event,Thread
import sys
import struct
import pygame
import pygame_gui
import os
from logging import getLogger
from dcsbios import ProtocolParser, StringBuffer, IntegerBuffer

pygame.init()
pygame.mouse.set_visible(False)

LOG = getLogger(__name__)

def _handle_connection(parser: ProtocolParser, sock: socket.socket, event: Event) -> None:
    while not event.is_set():
        try:
            dcs_bios_resp = sock.recv(2048)
            for int_byte in dcs_bios_resp:
                parser.process_byte(int_byte)
        except socket.error as exp:
            _sock_err_handler( exp)



def _sock_err_handler(exp: Exception) -> None:
    print(exp)
    """
    Show basic data when DCS is disconnected.
    :param lcd: type of Logitech keyboard with LCD
    :param start_time: time when connection to DCS was lost
    :param current_ver: logger.info about current version to show
    :param support_iter: iterator for banner supporters
    :param exp: caught exception instance
    """


def _prepare_socket() -> socket.socket:
    """
    Preparing multi-cast UDP socket for DCS-BIOS communication.
    :return: socket object
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(RECV_ADDR)
    mreq = struct.pack('=4sl', socket.inet_aton(MULTICAST_IP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    sock.settimeout(1)
    return sock

def update_display(address, data):
    #print(hex(address))
    if hex(address) == '0x7494':
        print("RPM R:")
        data_bytes = struct.pack("<H", data)
        print(int(data_bytes))
    if hex(address) == '0x7496':
        print("RPM L:")
        data_bytes = struct.pack("<H", data)
        print(int(data_bytes))
        
def dcspy_run( event: Event) -> None:
    """
    Real starting point of DCSpy.
    :param lcd_type: LCD handling class as string
    :param event: stop event for main loop
    """
    parser = ProtocolParser()
    parser.write_callbacks.add(update_display)
    _handle_connection(parser, _prepare_socket(), event)

th = Thread(target=dcspy_run, args=[Event()])
th.start()
#dcspy_run(event=Event())
 
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
