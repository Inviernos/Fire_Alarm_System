import RPi.GPIO as GPIO
from twilio.rest import Client

# my Account SID 
account_sid = "?????????????"

# my Auth Token 
auth_token  = "?????????????????"

#set up client api
client = Client(account_sid, auth_token)

#set the gpio mode  
GPIO.setmode(GPIO.BOARD)

#turn off warnings
GPIO.setwarnings(False)
   
#variables
BUZZER_PIN = 18
FLAME_PIN = 12
messageState = 1

#set up pins
GPIO.setup(FLAME_PIN ,GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT, initial= GPIO.LOW)
   
PHONE_NUM = "999-999-9999"
TWILLIO_PHONE_NUM = "888-888-8888"
try:
    while True:

        #Fire sensor detects a fire
        if GPIO.input(12) == GPIO.HIGH:

            if messageState == 1:

                #send text message to user
                message = client.messages.create(
                    to=PHONE_NUM, 
                    from_=TWILLIO_PHONE_NUM,
                    body="There is a fire in your home! Call 911")

                #change state
                messageState = 0

            #Turn on the buzzer
            GPIO.output(BUZZER_PIN,GPIO.HIGH)
           
        else:
            
            #turn off the buzzer
            GPIO.output(BUZZER_PIN,GPIO.LOW)

            if messageState == 0:

                #send message to user
                message = client.messages.create(
                    to=PHONE_NUM, 
                    from_=TWILLIO_PHONE_NUM,
                    body="The Fire Has Been Put Out!")

                #change state
                messageState = 1
            
   
    
# User interrupted the program
except KeyboardInterrupt:
     GPIO.output(BUZZER_PIN,GPIO.LOW)
     GPIO.cleanup()
