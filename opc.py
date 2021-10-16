from opcua import Client
from opcua import Server
import time
import numpy as np
import argparse
import imutils
import cv2
import numpy as npFF

url = "opc.tcp://192.168.100.40:4840"

colors = []

client = Client(url)
client.connect()
print("\nConnected\n")
Robo_x = client.get_node("ns=5;s=MotionDeviceSystem.ProcessData.Benthor.new_pos_Y")
Robo_start = client.get_node("ns=5;s=MotionDeviceSystem.ProcessData.Benthor.Start_follow")
print(Robo_x.get_value())


def get_contour_precedence(contour, cols):
    tolerance_factor = 10
    origin = cv2.boundingRect(contour)
    return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]


def main():
    return

if __name__ == "__main__":
    main()
