import RPi.GPIO as GPIO
import time
import requests
import os

#Setup GPIO pins, pin 18 as UP
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    #Wait until falling edge detected on GPIO
    GPIO.wait_for_edge(18, GPIO.FALLING)

    #Look for low input on GPIO (vs. just falling)
    input_state = GPIO.input(18)
    if input_state == False:

        #Download image from camera
        img = requests.get("*** IMAGE URL ***")
        snap = "snap.jpg"
        with open(snap, "w") as code:
            code.write(img.content)

        #Send photo
        files = {"photo": open(snap, "r")}
        requests.post("https://api.telegram.org/bot*** BOT TOKEN ***/sendPhoto?chat_id=*** CHAT ID ***&caption=Ding! Dong!", files=files)

        #Delete photo from disk
        if os.path.exists(snap):
            try:
                os.remove(snap)
            except OSError, e:
                print ("Error: %s - %s." % (e.snap,e.strerror))
        else:  
            print("Sorry, I can not find %s file." % snap)

        #Prevent multiple rings in less than one second
        time.sleep(1)

#If program exits outside of loop, cleanup GPIO
GPIO.cleanup()
