# Harikrishnan Kokkanthara Jeevan
# 016587116
# Program to test NEMA 17 motor with driver board on Jetson nano


def rotate_motor_degrees(GPIO, STEP_PIN, DIR_PIN, TIME, degrees, direction, frequency=200, duty_cycle=50):
    steps_per_revolution = 360 / 1.8  # Modify this according to your motor's specifications
    steps_to_move = int(degrees / 360 * steps_per_revolution)
    
    GPIO.output(DIR_PIN, direction)

    cycle_length = 1.0 / frequency
    on_time = cycle_length * (duty_cycle / 100.0)
    off_time = cycle_length - on_time

    for _ in range(steps_to_move):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        TIME.sleep(on_time)
        GPIO.output(STEP_PIN, GPIO.LOW)
        TIME.sleep(off_time)
