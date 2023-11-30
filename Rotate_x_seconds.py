# Harikrishnan Kokkanthara Jeevan
# 016587116
# Program to control NEMA 17 motor with driver board on Jetson Nano


def rotate_motor_time(GPIO, STEP_PIN, DIR_PIN,TIME,seconds, direction, frequency=200, duty_cycle=50):
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
        TIME.sleep(on_time)
        GPIO.output(STEP_PIN, GPIO.LOW)
        TIME.sleep(off_time)

