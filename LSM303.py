
from math import atan2, degrees as math_degrees


def calculate_heading(m_x, m_y):
    heading = math_degrees(atan2(m_y, m_x))
    return heading


def read_sensor_data(accel,mag):
    try:
        acc_x, acc_y, acc_z = accel.acceleration
    except Exception as e:
        return f"Error reading accelerometer data: {e}"

    try:
        m_x, m_y, m_z = mag.magnetic
        heading = calculate_heading(m_x, m_y)
    except Exception as e:
        return f"Error reading magnetometer data: {e}"

    return acc_x, acc_y, acc_z, m_x, m_y, m_z, heading


