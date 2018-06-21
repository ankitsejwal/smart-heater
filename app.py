from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import RPi.GPIO as GPIO
from thing import PiThing

pi_thing = PiThing()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    message_body = request.form['Body']
    resp = MessagingResponse()
    
    if message_body.lower() == 'on':
        pi_thing.set_led(True)
        resp.message_body('LED turned ON')

    elif message_body.lower() == 'off' :
        pi_thing.set_led(False)
        resp.message_body('LED turned OFF')
    
    return str(resp)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)