# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 08:31:02 2023

@author: ROMEROM
"""

import pyautogui
import time

def mouse_jiggler(interval=30):
    """
    Jiggle the mouse cursor every given interval (default is 10 seconds).

    Args:
    - interval (int): Time in seconds to wait between each jiggle.
    """
    try:
        print("Mouse jiggler started. Press Ctrl+C to stop.")
        while True:
            current_position = pyautogui.position()
            pyautogui.move(10, 0, duration=0.5)   # Move the cursor to the right
            pyautogui.click() # make a click
            pyautogui.move(-10, 0, duration=0.5)  # Move the cursor back to the original position
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Mouse jiggler stopped.")
        return

if __name__ == "__main__":
    mouse_jiggler()
