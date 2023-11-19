import Jetson.GPIO as GPIO

# Define the GPIO pin numbers
GREEN_LED_PIN = 36  # First LED
RED_LED_PIN = 38  # Second LED

def setup():
    GPIO.setmode(GPIO.BOARD)  # Use the physical pin numbering scheme
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
    GPIO.setup(RED_LED_PIN, GPIO.OUT)

def turn_on_green_led():
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)

def turn_off_green_led():
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)

def turn_on_red_led():
    GPIO.output(RED_LED_PIN, GPIO.HIGH)

def turn_off_red_led():
    GPIO.output(RED_LED_PIN, GPIO.LOW)

setup()