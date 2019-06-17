import socket
import random
import time
#import Adafruit_ADS1x15

#adc = Adafruit_7ADS1x15.ADS1115()
GAIN = 1

ip = "localhost"
data_port = 5555
send_interval = 5

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((ip, data_port))

s.listen(10)

client, (clientIp, clientPort) = s.accept()

while True:
    time.sleep(send_interval)
    value = random.randint(1, 20)
    # temp_value = [value, value, value, value]
    temp_value = str(value) + " | " + str(value) + " | " + str(value) + " | " + str(value)
    

    # value =  adc.read_adc(0, gain=GAIN)*4.096/32768.0
    print("Value to be sent", temp_value)
    data = str(temp_value)
    client.send(data.encode())
    print("Sending ", data)