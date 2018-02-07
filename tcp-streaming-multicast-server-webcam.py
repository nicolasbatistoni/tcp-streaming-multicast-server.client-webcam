#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import time
import json
import socket
import base64
import numpy as np
from threading import Thread

"""
    File name: tcp-streaming-multicast-server-webcam.py
    Author: Jäger Cox // jagercox@gmail.com
    Date created: 04/08/2016
    License: MIT
    Python Version: 2.7
    Revision: PEP8
"""

__author__ = "Jäger Cox // jagercox@gmail.com"
__created__ = "04/08/2016"
__license__ = "MIT"
__version__ = "0.1"
__python_version__ = "2.7"
__email__ = "jagercox@gmail.com"

SERVER_IP = "0.0.0.0"
SERVER_PORT = 1025
MAX_NUM_CONNECTIONS = 20
DEVICE_NUMBER = 0

IMAGE_HEIGHT = 480
IMAGE_WIDTH = 640
COLOR_PIXEL = 3  # RGB


class ConnectionPool(Thread):

    def __init__(self, ip_, port_, conn_):
        Thread.__init__(self)
        self.ip = ip_
        self.port = port_
        self.conn = conn_
        print "[+] New server socket thread started for " + self.ip + ":" + \
            str(self.port)

    def run(self):
        try:
            while True:
                fileDescriptor = self.conn.makefile(mode='rb')
                result = fileDescriptor.readline()
                fileDescriptor.close()
                result = base64.b64decode(result)

                frame = np.fromstring(result, dtype=np.uint8)
                frame_matrix = np.array(frame)
                frame_matrix = np.reshape(frame_matrix, (IMAGE_HEIGHT, IMAGE_WIDTH,
                                                         COLOR_PIXEL))
                cv2.imshow('Window title', frame_matrix)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except Exception, e:
            print "Connection lost with " + self.ip + ":" + str(self.port) + \
                  "\r\n[Error] " + str(e.message)
        self.conn.close()

if __name__ == '__main__':
    print "Waiting connections..."
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind((SERVER_IP, SERVER_PORT))
    connection.listen(MAX_NUM_CONNECTIONS)
    while True:
        (conn, (ip, port)) = connection.accept()
        thread = ConnectionPool(ip, port, conn)
        thread.start()
    connection.close()
camera.release()
