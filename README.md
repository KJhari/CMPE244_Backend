# CMPE-244-backend

Project Name: FastAPI Backend for Motor Control and Sensor Data Processing
Description
This project implements a backend server using FastAPI to control a NEMA17 stepper motor and process data from an LSM303 sensor. The server provides endpoints to initiate motor movements and read sensor data, facilitating precise control and monitoring of the motor's orientation.

Features
Control of a NEMA17 stepper motor via GPIO.
Integration with an LSM303 sensor for heading and angle measurements.
RESTful API endpoints for motor control and sensor data retrieval.
Calibration routine for the LSM303 sensor.
Installation
Prerequisites
Python 3.6+
Jetson GPIO (for Jetson Nano users)
FastAPI and Uvicorn
Setup
Install FastAPI and Uvicorn:

bash
Copy code
pip install fastapi uvicorn
Clone the Repository (if applicable):

bash
Copy code
git clone <repository-url>
cd <repository-directory>
Install Additional Dependencies:

bash
Copy code
```
pip install fastapi uvicorn
```

Usage
Running the Server
To start the FastAPI server, run the following command in your terminal:

bash
Copy code

To run the application run
```
uvicorn python-main:app --reload
```

for jetson
```
python -m uvicorn python-main:app --host 0.0.0.0 --port 8000 --reload
```
The server will be available at http://0.0.0.0:8000.

API Endpoints
/gpt-prompt (POST)
Receives a prompt and returns a string response.

Payload: { "prompt": "Your prompt here" }
Response: { "response": "Received prompt: Your prompt here" }
/run-motor (POST)
Controls the rotation of the NEMA17 stepper motor and reads sensor data.

Payload: { "Frequency": 1000, "Duty_Cycle": 100, "Direction": 0, "Time": 2, "Degree": 90 }
Response: JSON containing motor operation status and sensor data.
Calibration
Before using the sensor data, calibrate the LSM303 sensor by running the calibration script provided. Follow the instructions in the script to rotate the sensor through various orientations.

Development
Modifying the Code
You can modify the code to suit specific requirements, such as changing GPIO pin configurations, adjusting motor control parameters, or modifying API response structures.

Testing
Ensure to test the API endpoints and motor control functionality thoroughly before deploying in a production environment. Use tools like curl or Postman for API testing.

License
