from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 
import Rotate_x_degrees # for running motor based on degrees
import Rotate_x_seconds    # based on time in s
import Jetson.GPIO as GPIO
import random
from typing import Optional 
import LED_control
from LSM303 import  read_sensor_data, calculate_heading
from math import atan2, degrees as math_degrees
import time as TIME
import board
import busio
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag


# Define the GPIO pin numbers
GREEN_LED_PIN = 36  # First LED
RED_LED_PIN = 38  # Second LED
STEP_PIN = 33   # Motor step pin Nano
DIR_PIN = 31   # Motor direction pin Nano

# Clean up GPIO settings at the start
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)

# LSM303 Sensor Setup
i2c = busio.I2C(board.SCL, board.SDA)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)

#Init LED steup
LED_control.setup_leds(GPIO, GREEN_LED_PIN, RED_LED_PIN)
LED_control.turn_off_green_led(GPIO, GREEN_LED_PIN)
LED_control.turn_off_red_led(GPIO, GREEN_LED_PIN)

# Define a Pydantic model for the request data
class MotorData(BaseModel):
    Frequency: int
    Duty_Cycle: int
    Direction: int
    Time: Optional[int] = None  # Make Time optional
    Degree: Optional[int] = None  # Make Degree optional

# Create an instance of FastAPI
app = FastAPI()
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mock function to simulate LSM303 sensor data
def mock_lsm303_data():
    # Simulate sensor data (e.g., accelerometer and magnetometer readings)
    sucess = True
    accelerometer_data = {"x": random.uniform(-1, 1), "y": random.uniform(-1, 1), "z": random.uniform(-1, 1)}
    magnetometer_data = {"x": random.uniform(-30, 30), "y": random.uniform(-30, 30), "z": random.uniform(-30, 30)}
    return {"accelerometer": accelerometer_data, "magnetometer": magnetometer_data, "sucess":sucess}

# Define the POST endpoint
@app.post("/run-motor")
async def run_motor(data: MotorData):
    # Process the data here
    # For example, you can print it or pass it to another function
    try:
        Frequency = data.Frequency
        Duty_Cycle = data.Duty_Cycle
        if(data.Direction == 0):
            Direction = GPIO.HIGH
        elif(data.Direction == 1):
            Direction = GPIO.LOW
        if(data.Time):
            Degree = 360
            Time = data.Time
            Rotate_x_seconds.rotate_motor_time(GPIO, STEP_PIN,DIR_PIN, TIME ,Time, Direction, Frequency, Duty_Cycle)
        elif(data.Degree):
            Time = 2
            Degree = data.Degree
            Rotate_x_degrees.rotate_motor_degrees(GPIO, STEP_PIN,DIR_PIN, TIME ,Degree, Direction, Frequency, Duty_Cycle)
        
        # Read sensor data
        sensor_data_result = read_sensor_data(accel,mag)
        print(data)
        # call your function
        # result = yourFunction(value1, value2, value3)
        
        
        # Call the mock LSM303 data function after motor operation
        #sensor_data = mock_lsm303_data()
        
        # Check if an error was returned from sensor data reading
        if isinstance(sensor_data_result, tuple):
            acc_x, acc_y, acc_z, m_x, m_y, m_z, angle_yz, heading = sensor_data_result
            sensor_data = {
                "accelerometer": {"x": acc_x, "y": acc_y, "z": acc_z},
                "magnetometer": {"x": m_x, "y": m_y, "z": m_z},
                "angle_yz": angle_yz,
                "heading":heading
            }
            LED_control.turn_on_green_led(GPIO, GREEN_LED_PIN)
            LED_control.turn_off_red_led(GPIO, GREEN_LED_PIN)
            return {
                "message": "Motor run successfully with the provided data",
                "data": data,
                "sensor_data": sensor_data
            }
        else:
            LED_control.turn_off_green_led(GPIO, GREEN_LED_PIN)
            LED_control.turn_on_red_led(GPIO, GREEN_LED_PIN)
            # If sensor_data_result is not a tuple, it's an error message
            raise ValueError(sensor_data_result)
        
    except Exception as e:
        # Return an error response
        return {
            "message": "Error during operation",
            "error": str(e),
            "data": data
    }
# Run the application using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
