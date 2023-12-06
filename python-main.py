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
import openai
from gpt_test import query_gpt_3_5_turbo


#GPT parameters
api_key = "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"
model_id = "ft:gpt-3.5-turbo-0613:personal::8Si57snJ"

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

# Init LED steup
LED_control.setup_leds(GPIO, GREEN_LED_PIN, RED_LED_PIN)
LED_control.turn_off_green_led(GPIO, GREEN_LED_PIN)
LED_control.turn_off_red_led(GPIO, GREEN_LED_PIN)

# Pydantic model
class MotorData(BaseModel):
    Frequency: int
    Duty_Cycle: int
    Direction: int
    Time: Optional[int] = None  # Make Time optional
    Degree: Optional[int] = None  # Make Degree optional

class GptData(BaseModel):
    prompt: str

# FastAPI instance
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
# def mock_lsm303_data():
#     # Simulate sensor data (e.g., accelerometer and magnetometer readings)
#     sucess = True
#     accelerometer_data = {"x": random.uniform(-1, 1), "y": random.uniform(-1, 1), "z": random.uniform(-1, 1)}
#     magnetometer_data = {"x": random.uniform(-30, 30), "y": random.uniform(-30, 30), "z": random.uniform(-30, 30)}
#     return {"accelerometer": accelerometer_data, "magnetometer": magnetometer_data, "sucess":sucess}

# Mock function of chatpgt
def mock_gpt(question):
    return "answer"


# POST endpoint
@app.post("/run-motor")
async def run_motor(data: MotorData):
   # Motor and sensor logic
    try:
        # Read sensor data before
        sensor_data_result_before = read_sensor_data(accel,mag)
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
        
        # Read sensor data after
        sensor_data_result = read_sensor_data(accel,mag)
        
        #request info
        print(data)
    
        # Call the mock LSM303 data function after motor operation
        #sensor_data = mock_lsm303_data()
        
        # Check if an error was returned from sensor data reading: if not tuple then error
        if isinstance(sensor_data_result, tuple):
            acc_x_b, acc_y_b, acc_z_b, m_x_b, m_y_b, m_z_b, heading_b = sensor_data_result_before
            acc_x, acc_y, acc_z, m_x, m_y, m_z, heading = sensor_data_result
            sensor_data = {
                "accelerometer": {"x": acc_x, "y": acc_y, "z": acc_z},
                "magnetometer": {"x": m_x, "y": m_y, "z": m_z},
                "heading":heading
            }
            sensor_data_b = {
                "accelerometer": {"x": acc_x_b, "y": acc_y_b, "z": acc_z_b},
                "magnetometer": {"x": m_x_b, "y": m_y_b, "z": m_z_b},
                "heading":heading_b
            }
            LED_control.turn_on_green_led(GPIO, GREEN_LED_PIN)
            LED_control.turn_off_red_led(GPIO, GREEN_LED_PIN)
            return {
                "message": "Motor run successfully with the provided data",
                "data": data,
                "sensor_data": sensor_data,
                "sensor_data_b" : sensor_data_b
            }
        else:
            LED_control.turn_off_green_led(GPIO, GREEN_LED_PIN)
            LED_control.turn_on_red_led(GPIO, GREEN_LED_PIN)
            raise ValueError(sensor_data_result)
        
    except Exception as e:
        # Return an error response
        return {
            "message": "Error during operation",
            "error": str(e),
            "data": data
    }

@app.post("/gpt-prompt")
async def gpt_prompt(data: GptData):
    print('question: ' + data.prompt)
    response_text = query_gpt_3_5_turbo(data.prompt, model_id, api_key)
    #response_text = mock_gpt(data.prompt)
    return {"responseText": response_text}


# Run the application using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
