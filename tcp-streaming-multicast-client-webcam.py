#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import socket
import base64
import numpy as np

"""
    File name: tcp-streaming-multicast-client-webcam.py
    Author: Jäger Cox // jagercox@gmail.com
    Date created: 04/08/2016
    License: MIT
    Python Version: 2.7
    Code guide line: PEP8
"""

__author__ = "Jäger Cox // jagercox@gmail.com"
__created__ = "04/08/2016"
__license__ = "MIT"
__version__ = "0.1"
__python_version__ = "2.7"
__email__ = "jagercox@gmail.com"

IP_SERVER = "0.0.0.0"
PORT_SERVER = 1025
TIMEOUT_SOCKET = 10
SIZE_PACKAGE = 4096

IMAGE_HEIGHT = 480
IMAGE_WIDTH = 640
COLOR_PIXEL = 3  # RGB

DEVICE_NUMBER = 0

if __name__ == '__main__':
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.settimeout(TIMEOUT_SOCKET)
    connection.connect((IP_SERVER, PORT_SERVER))

    camera = cv2.VideoCapture(DEVICE_NUMBER)

    while True:
        try:
            ret, frame = camera.read()
            if ret:
                data = frame.tostring()
                connection.sendall(base64.b64encode(data) + '\r\n')


        except Exception as e:
            print "[Error] " + str(e)

connection.close()
