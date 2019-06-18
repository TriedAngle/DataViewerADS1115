import socket
import random
import time
import pickle
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

def getDateDict():
    dic = {}
    dic["year"] = str(time.localtime().tm_year)
    dic["month"] = str(time.localtime().tm_mon)
    dic["day"] = str(time.localtime().tm_mday)
    dic["hour"] = str(time.localtime().tm_hour)
    dic["minute"] = str(time.localtime().tm_min)
    return pickle.dumps(dic)


def formatDate(dicBytes):
    dAttributes = ['month', 'day', 'hour', 'minute']
    dic = pickle.loads(dicBytes)
    for attr in dAttributes:
        if len(dic[attr]) < 2:
            dic[attr] = (dic[attr] + "0")[::-1]
    return pickle.dumps(dic)


def makeSendData(values):
    data = pickle.loads(formatDate(getDateDict()))
    data["value-0"] = values[0]
    data["value-1"] = values[1]
    data["value-2"] = values[2]
    data["value-3"] = values[3]

    return pickle.dumps(data)

while True:
    time.sleep(send_interval)
    
    value = []
    for i in range(4):
        value.append(random.randint(0,20))
        #value.append(adc.read_adc(i, gain=GAIN)*4.096/32768.0)
    
    print(value)
    
    client.send(makeSendData(value))
