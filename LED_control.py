def setup_leds(GPIO, GREEN_LED_PIN, RED_LED_PIN):
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
    GPIO.setup(RED_LED_PIN, GPIO.OUT)

def turn_on_green_led(GPIO, GREEN_LED_PIN):
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)

def turn_off_green_led(GPIO, GREEN_LED_PIN):
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)

def turn_on_red_led(GPIO, GREEN_LED_PIN):
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)

def turn_off_red_led(GPIO, GREEN_LED_PIN):
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)