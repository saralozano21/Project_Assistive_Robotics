import os
import time
import socket
import tkinter as tk
from tkinter import messagebox
from math import radians, degrees, pi
import math
from robodk.robolink import *
from robodk.robomath import *

# Load RoboDK project from relative path
relative_path = "Assistive_UR5e.rdk"
absolute_path = os.path.abspath(relative_path)
RDK = Robolink()
# RDK.AddFile(absolute_path)

# Robot setup
robot = RDK.Item("UR5e")
base = RDK.Item("UR5e Base")
tool = RDK.Item('Hand')
Init_target = RDK.Item('Init')
wave_start_target = RDK.Item('wave_start')
wave_left_target = RDK.Item('wave_left')
wave_right_target = RDK.Item('wave_right')

robot.setPoseFrame(base)
robot.setPoseTool(tool)
robot.setSpeed(20)

# Robot Constants
ROBOT_IP = '192.168.1.5'
ROBOT_PORT = 30002
accel_mss = 1.2
speed_ms = 0.75
blend_r = 0.0
timej = 6
timel = 3

# URScript commands
set_tcp = "set_tcp(p[0.000000, 0.000000, 0.050000, 0.000000, 0.000000, 0.000000])"

deg_init = [-57.835746, -65.391528, -107.167117, 172.558645, -57.835746, 0.000000]
rad_init = [math.radians(j) for j in deg_init]
movej_init = f"movej({rad_init},{accel_mss},{speed_ms},{timel},0.0000)"

deg_start = [-61.661349, -60.826168, -126.275295, 227.862971, -67.780209, -18.054745]
rad_start =[math.radians(j) for j in deg_start]
movel_wave_start = f"movel({rad_start},{accel_mss},{speed_ms},{timel},0.000)"

deg_left = [-72.331751, -93.354688, -127.409127, 325.269567, -94.561656, -17.087400]
rad_left = [math.radians(j) for j in deg_left]
movel_wave_left = f"movel({rad_left},{accel_mss},{speed_ms},{timel/2},0.000)"

deg_right = [-63.680100, -63.491305, -130.156774, 245.118521, -72.874121, -20.294912]
rad_right = [math.radians(j) for j in deg_right]
movel_wave_right = f"movel({rad_right},{accel_mss},{speed_ms},{timel/2},0.000)"

# Check robot connection
def check_robot_port(ip, port):
    global robot_socket
    try:
        robot_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        robot_socket.settimeout(1)
        robot_socket.connect((ip, port))
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False
# Send URScript command
def send_ur_script(command):
    robot_socket.send((command + "\n").encode())


# Movements
def Init():
    print("Init")
    robot.MoveL(Init_target, True)
    print("Init_target REACHED") 
    if robot_is_connected:
        print("Init REAL UR5e")
        send_ur_script(set_tcp)
        send_ur_script(movej_init)

def Wave():
    robot.MoveL(wave_start_target, True)
    for _ in range(3):
        robot.MoveL(wave_left_target, True)
        robot.MoveL(wave_right_target, True)
    robot.MoveL(wave_start_target, True)

    if robot_is_connected:
        send_ur_script(set_tcp)
        send_ur_script(movel_wave_left)
        send_ur_script(movel_wave_right)
        send_ur_script(movel_wave_left)


# Confirmation dialog to close RoboDK
def confirm_close():
    root = tk.Tk()
    root.withdraw()
    response = messagebox.askquestion(
        "Close RoboDK",
        "Do you want to save changes before closing RoboDK?",
        icon='question'
    )
    if response == 'yes':
        RDK.Save()
        RDK.CloseRoboDK()
        print("RoboDK saved and closed.")
    else:
        RDK.CloseRoboDK()
        print("RoboDK closed without saving.")

# Main function
def main():
    global robot_is_connected
    robot_is_connected = False
    Init()
    Wave()

# Run and close
if __name__ == "__main__":
    main()
    #confirm_close()
