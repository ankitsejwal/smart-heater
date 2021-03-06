#!bin/python3

from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse
import RPi.GPIO as GPIO
from heater import Heater

# create heater object
heater = Heater()

# ON and OFF phrase that we want to match with recieved SMS
on_phrase = ['on', 'heater on', 'turn heater on', 'turn on']
off_phrase = ['off', 'heater off', 'turn heater off', 'turn off']

app = Flask(__name__)

@app.route('/')
def home():
    led_status = heater.get_status()
    return render_template('home.html', led_status = led_status)

@app.route('/led/<int:led_state>', methods=['POST'])
def led(led_state):
    if led_state == 1:
        heater.set_led(True)
    elif led_state == 0:
        heater.set_led(False)
    else:
        return ('Bad request', 400)
    # return success 204 
    return ('', 204)


@app.route('/sms', methods=['GET', 'POST'])
def sms():
    # Get message from twilio
    message_body = request.form['Body']
    resp = MessagingResponse()
    
    # if user wants to turn heater ON
    if message_body.lower() in on_phrase:
        heater.set_led(True)
        resp.message('LED turned ON')

    # if user wants to turn heater OFF
    elif message_body.lower() in off_phrase :
        heater.set_led(False)
        resp.message('LED turned OFF')
    
    # get led status
    elif message_body.lower() == 'status':
        status = 'ON' if heater.get_status() == 1 else 'OFF'
        resp.message('The LED is currently ' + status)

    return str(resp)
    
if __name__ == '__main__':
    # host 0.0.0.0 allows you to access your raspi from a web browser of
    # other computers on the same network http://0.0.0.0:5005
    app.run(host='0.0.0.0', port=5005, debug=True)