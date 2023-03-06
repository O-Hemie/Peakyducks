import RPi.GPIO as GPIO
import time

# GPIO pin for sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN)

# GPIO pin for heating system
GPIO.setup(18, GPIO.OUT)
heating_on = False
max_pressure = 100

# Wait for sensor to stabilize
print("Sensor initializing...")
time.sleep(2)
print("Ready")

# Main loop
while True:
    # Read sensor input
    num_people = 0
    for i in range(10):
        if GPIO.input(14):
            num_people += 1
        time.sleep(0.01)
    
    # heating pressure based on number of people
    if num_people > 0:
        pressure = (num_people / 10) * max_pressure
        if not heating_on:
            print(f"{num_people} human(s) detected - turning heating on (pressure: {pressure})")
            heating_on = True
            GPIO.output(18, GPIO.HIGH)
        else:
            print(f"{num_people} human(s) detected - heating pressure: {pressure}")
    else:
        if heating_on:
            print("No humans detected - turning heating off")
            heating_on = False
            GPIO.output(18, GPIO.LOW)
        else:
            print("No humans detected")

    time.sleep(1)
