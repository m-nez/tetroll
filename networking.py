"""
Networking for Tetroll
"""

from collections import deque
import socket
from threading import Thread
import select
from os import system
import time
import pygame

class Connection:
    """
    Connection with an outside player
    """
    def __init__(self, bo, ip, send=True):
        self.command_buffer = deque()
        self.port = 5017
        self.ip = ip
        self.timeout = 0.005

        if ip[:7] != "192.168" and ip != "localhost" and ip != "LAN":
            self.auto_forward_port()
        if send:
            self.init_socket_send_request()
        else:
            self.init_socket_listen_request()

    def init_socket_listen_request(self):
        """
        Wait for a socket to connect.
        Establish connection with the second player.
        """
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((socket.gethostbyname(socket.gethostname()), self.port))

        self.socket.listen(5)

        end_term = [False]
        def term(end_term):
            while not end_term[0]:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.socket.shutdown(socket.SHUT_RDWR)
                        exit(1)
                        end_term[0] = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.socket.shutdown(socket.SHUT_RDWR)
                            exit(1)
                            end_term[0] = True
                time.sleep(0.2)

        t = Thread(target=term, args=(end_term,))
        t.start()

        self.client_socket, addr = self.socket.accept()
        end_term[0] = True
        t.join()
        self.client_socket.setblocking(0)

    def init_socket_send_request(self):
        """
        Connect to a socket
        Establish connection with the second player.
        """
        self.client_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        #self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.client_socket.connect((self.ip, self.port))
        self.client_socket.setblocking(0)

    def send(self, ba):
        """
        Takes a list of integers <0, 255> and sends them to the other end.
        """
        to_send = len(ba)
        sent = 0
        while sent < to_send:
            sent += self.client_socket.send(bytearray(ba[sent:]))

    def receive(self):
        """
        Try receiving.
        If nothing has been received return 0.
        """

        ready_to_read = select.select([self.client_socket], [], [], self.timeout)[0]

        if ready_to_read != []:
            return(self.client_socket.recv(1024))
        else:
            return 0

    def forward_port(self, int_port, ext_port, time):
        """
        Forward a port using miniupnp
        """
        command = "upnpc -a %r %r %r TCP %r" % (
            socket.gethostbyname(socket.gethostname()),
            int_port, ext_port, time
            )
        system(command)

    def auto_forward_port(self):
        """
        Forward current port for 30 minutes
        """
        self.forward_port(self.port, self.port, 1800)
