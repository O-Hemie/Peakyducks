import RPi.GPIO as GPIO
import time

#GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

#GPIO pin for PIR sensor (you can change pin based on set up)
pir_sensor_pin = 17

# GPIO pin for the heating system (you can change pin based on set up)
heating_system_pin = 18

# initial state of the heating system = off
heating_system_state = False

# temperature threshold for reducing the pressure from heating system
temperature_threshold = 25  # room temperature

# the initial number of humans in the building 
num_humans = 0

# GPIO pins as input or output
GPIO.setup(pir_sensor_pin, GPIO.IN)
GPIO.setup(heating_system_pin, GPIO.OUT)

# Function to turn on the heating system


def turn_on_heating_system():
    global heating_system_state
    GPIO.output(heating_system_pin, GPIO.HIGH)
    heating_system_state = True

# Function to turn off the heating system


def turn_off_heating_system():
    global heating_system_state
    GPIO.output(heating_system_pin, GPIO.LOW)
    heating_system_state = False


# Loop for detecting human and controlling the heating system
while True:
    # value from PIR sensor
    pir_sensor_value = GPIO.input(pir_sensor_pin)

    if pir_sensor_value == 1:
        # Human detected
        num_humans += 1

        # Turn on the heating system if it is still off
        if not heating_system_state:
            turn_on_heating_system()

        # Reduce pressure if there are more humans
        if num_humans > 1:
            if temperature_threshold > 0:
                temperature_threshold -= 1

    else:
        # No human detected
        num_humans -= 1

        # Turn off the heating system if no humans are present
        if num_humans == 0:
            turn_off_heating_system()

        # Increase temperature threshold if only one human is present
        if num_humans == 1:
            if temperature_threshold < 25:
                temperature_threshold += 1

    # Wait for 1 second before detecting again
    time.sleep(1)
