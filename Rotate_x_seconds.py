# Harikrishnan Kokkanthara Jeevan
# 016587116
# Program to control NEMA 17 motor with driver board on Jetson Nano

import Jetson.GPIO as GPIO
import time

STEP_PIN = 33
DIR_PIN = 31

# Set up GPIO
GPIO.setmode(GPIO.BOARD)  
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)

def rotate_motor_time(seconds, direction, frequency=200, duty_cycle=50):
    steps_per_revolution = 360 / 1.8  # Modify this according to your motor's specifications
    # Calculate steps per second
    steps_per_second = frequency * steps_per_revolution / 360
    total_steps = int(steps_per_second * seconds)
    
    GPIO.output(DIR_PIN, direction)

    cycle_length = 1.0 / frequency
    on_time = cycle_length * (duty_cycle / 100.0)
    off_time = cycle_length - on_time

    for _ in range(total_steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(on_time)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(off_time)

if __name__ == "__main__":
    print('*****Harikrishnan Kokkanthara Jeevan, SID:016587116*****')
    try:
        seconds = float(input("Enter the time in seconds for rotation: "))
        direction_input = input("Enter the rotation direction (CW for clockwise, CCW for counterclockwise): ")
        frequency = float(input("Enter the step frequency (in Hz): "))
        duty_cycle = float(input("Enter the duty cycle (0-100): "))

        # Set direction based on user input
        direction = GPIO.HIGH if direction_input.upper() == 'CW' else GPIO.LOW

        # Rotate motor
        print("Rotating motor...")
        rotate_motor_time(seconds, direction, frequency, duty_cycle)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        GPIO.cleanup()
