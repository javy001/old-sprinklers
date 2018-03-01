import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def pickSprinkler():
    choice = input('Choose sprinkler: \n1. Bush \n2. Front \n3. Back Left \n4. Back Right \n')
    pins = {1: 17, 2: 27, 3: 22, 4: 18}
    GPIO.setup(pins[choice], GPIO.OUT)
    GPIO.output(pins[choice], GPIO.LOW)
    raw_input('Press any key to turn off')
    GPIO.output(pins[choice], GPIO.HIGH)

while True:
    choice = input('Make Selection: \n1. Turn on sprinklers \n2. Quit \n')
    if choice == 1:
        pickSprinkler()
    elif choice == 2:
        break

GPIO.cleanup()
