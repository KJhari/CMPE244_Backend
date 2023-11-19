from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Rotate_x_degrees import rotate_motor_degrees # for running motor based on degrees
from Rotate_x_seconds import rotate_motor_time    # based on time in s
import Jetson.GPIO as GPIO
import random
from typing import Optional 
from LED_control import setup,turn_on_green_led,turn_off_green_led,turn_on_red_led,turn_off_red_led 


#Init LED steup
setup()
turn_off_green_led() 
turn_off_red_led()


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
    Frequency = data.Frequency
    Duty_Cycle = data.Duty_Cycle
    if(data.Direction == 0):
        Direction = GPIO.HIGH
    elif(data.Direction == 1):
        Direction = GPIO.LOW
    if(data.Time):
        Degree = 360
        Time = data.Time
        rotate_motor_time(Time, Direction, Frequency, Duty_Cycle)
    elif(data.Degree):
        Time = 2
        Degree = data.Degree
        rotate_motor_degrees(Degree, Direction, Frequency, Duty_Cycle)
    
    print(data)
    # call your function
    # result = yourFunction(value1, value2, value3)
    
    
    # Call the mock LSM303 data function after motor operation
    sensor_data = mock_lsm303_data()
    
    
    # Return a response
    if(sensor_data.get("sucess")  ==True):
        turn_off_red_led()
        turn_on_green_led()
        return {
            "message": "Motor run successfully with the provided data",
            "data": data,
            "sensor_data": sensor_data
        }
    
    elif(sensor_data.get("sucess")==False):
         turn_off_green_led()
         turn_on_red_led()
         return {
            "message": "system Error, Motor did not run correctly",
            "data": data,
            "sensor_data": sensor_data
        }

# Run the application using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
