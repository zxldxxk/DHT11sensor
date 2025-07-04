import ubinascii              # Conversions between binary data and various encodings
import machine                # To Generate a unique id from processor

# Wireless network
WIFI_SSID =  "" # input your own ssid name 
WIFI_PASS = "" # input wifi password 

# Adafruit IO (AIO) configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "" #input your own adafruit username
AIO_KEY = "" #input your own adafruit key
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything
AIO_TEMP_C_FEED = ""  #
AIO_TEMP_F_FEED = ""  # enter each respective feed link here.
AIO_HUMI_FEED = ""    #
