import time                   # Allows use of time.sleep() for delays
from mqtt import MQTTClient   # For use of MQTT protocol to talk to Adafruit IO
import machine                # Interfaces with hardware components
import micropython            # Needed to run any MicroPython code
import random                 # Random number generator
from machine import Pin       # Define pin
import keys                   # Contain all keys used here
import wifiConnection         # Contains functions to connect/disconnect from WiFi 
import dht					  # Contains functions to initilize the DHT11 sensor 

# BEGIN SETTINGS
# These need to be change to suit your environment
RANDOMS_INTERVAL = 20000    # milliseconds
last_random_sent_ticks = 0  # milliseconds
sensor = dht.DHT11(19) 		# DHT11 Sensor pinout 


# Function to generate a random number between 0 and the upper_bound
def random_integer(upper_bound):
    return random.getrandbits(32) % upper_bound

# Function to publish random number to Adafruit IO MQTT server at fixed interval
def send_sensor_data():
    global last_random_sent_ticks 
    global RANDOMS_INTERVAL

    if ((time.ticks_ms() - last_random_sent_ticks) < RANDOMS_INTERVAL):
        return; # Too soon since last one sent.
    try:
        sensor.measure() # Gets the temperature from the sensor
        t_c = sensor.temperature() # Saves the temperature in celsius in a variable
        t_f = t_c * (9/5) + 32.0 # converts the temperature to fareheit and saves in a variable
        h = sensor.humidity() # Gets the humidity from the sensor
        print("Temp in c: ",t_c, "\n","Temp in f", t_f, "\n","humidity", h) # prints in the terminal for debugging purposes
        client.publish(topic=keys.AIO_TEMP_C_FEED, msg=str(t_c)) # publishes the temerature in celsius 
        client.publish(topic=keys.AIO_TEMP_F_FEED, msg=str(t_f)) # publishes the temprature in farenheit
        client.publish(topic=keys.AIO_HUMI_FEED, msg=str(h)) # publishes the humidity
        print("DONE")
    except Exception as e:
        print("FAILED") # if anything goes wrong it prints FAILED in the terminal 
    finally:
        last_random_sent_ticks = time.ticks_ms()


# Try WiFi Connection
try:
    ip = wifiConnection.connect()
except KeyboardInterrupt:
    print("Keyboard interrupt")

# Use the MQTT protocol to connect to Adafruit IO
client = MQTTClient(keys.AIO_CLIENT_ID, keys.AIO_SERVER, keys.AIO_PORT, keys.AIO_USER, keys.AIO_KEY)

# Subscribed messages will be delivered to this callback
client.connect()


try:                      # Code between try: and finally: may cause an error
                          # so ensure the client disconnects the server if
                          # that happens.
    while 1:              # Repeat this loop forever
        send_sensor_data()     # Send a random number to Adafruit IO if it's time.
finally:                  # If an exception is thrown ...
    client.disconnect()   # ... disconnect the client and clean up.
    client = None
    wifiConnection.disconnect()
    print("Disconnected from Adafruit IO.")
