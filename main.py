import pygame
import pyautogui
import threading
import tkinter as tk
import sys
import math
import time

# Global variable to control the program
running = False

# Function to handle joystick input
def joystick_handler():
    global running
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No joystick/controller detected.")
        running = False
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Detected controller: {joystick.get_name()}")

    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2

    try:
        while running:
            # Left joystick for circular movement
            left_x = joystick.get_axis(0)  # Left joystick horizontal
            left_y = joystick.get_axis(1)  # Left joystick vertical

            # Right joystick for free movement
            right_x = joystick.get_axis(2)  # Right joystick horizontal
            right_y = joystick.get_axis(3)  # Right joystick vertical

            # Move mouse freely with right joystick
            if abs(right_x) > 0.1 or abs(right_y) > 0.1:  # Deadzone
                x = pyautogui.position()[0]
                y = pyautogui.position()[1]
                pos_x = x + int(150*right_x)
                pos_y = y + int(150*right_y)
                pyautogui.moveTo(pos_x,pos_y, duration=0.1)

            for event in pygame.event.get():
                # Calculate new mouse position for left joystick (circular movement)
                if event.type == pygame.JOYAXISMOTION and abs(left_x) > 0.1 or abs(left_y) > 0.1:  # Deadzone
                    pos_x = center_x + int(50*left_x)
                    pos_y = center_y + int(50*left_y)
                    pyautogui.moveTo(pos_x,pos_y, duration=0.05)
                    pyautogui.leftClick()
                if event.type == pygame.JOYBUTTONDOWN and event.dict['button'] == 0:
                    pyautogui.leftClick()
                if event.type == pygame.JOYAXISMOTION and event.dict['axis'] == 5 and event.dict['value'] > 0.5:
                    pyautogui.leftClick()
                if event.type == pygame.JOYAXISMOTION and event.dict['axis'] == 4 and event.dict['value'] > 0.5:
                    pyautogui.rightClick()
            pygame.event.clear()

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        pygame.quit()

# Function to start the joystick thread
def start_program():
    global running
    if not running:
        running = True
        threading.Thread(target=joystick_handler, daemon=True).start()

# Function to stop the program
def stop_program():
    global running
    running = False
    root.destroy()
    sys.exit()

# GUI for start/stop controls
root = tk.Tk()
root.title("PS5 Controller Mouse Control")
root.geometry("500x500")

label = tk.Label(root, text="PS5 Controller Mouse Control", font=("Arial", 14))
label.pack(pady=10)

start_button = tk.Button(root, text="Start", command=start_program, bg="green", fg="white", width=10)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop", command=stop_program, bg="red", fg="white", width=10)
stop_button.pack(pady=5)

root.protocol("WM_DELETE_WINDOW", stop_program)  # Handle window close
root.mainloop()
