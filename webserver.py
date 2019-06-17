from flask import Flask
from flask import render_template
import random
import time
import socket
import threading

# variables
app = Flask(__name__)

ip = "localhost"
data_port = 5555
retrieve_interval = 5

user = {
    'username': 'Sebastian',
    'age': 17
}

data = []


# methods

def getData():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect((ip, data_port))
            break
        except:
            print("Error - Could not connect to Data Source. Retrying in 3 Seconds")
            time.sleep(3)
    while True:
        try:
            time.sleep(retrieve_interval)
            temp_data = s.recv(2048).decode()
            print("received: ", temp_data)
            current_time = str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min) + ":" + str(time.localtime())
            data.append(temp_data + " : " + current_time)
            # data.append(temp_data)
        except:
            print("Error - Could not Retrieve Data")


thread_receive = threading.Thread(target=getData, args=())
thread_receive.start()

# sites

@app.route('/')
def home():
    return render_template('Home.html', title='Home', user=user)

@app.route('/measure')
def rtmeasure():
    return render_template('RealtimeMeasurement.html', data=data, user=user)


if __name__ == "__name__":
    app.run(debug=True, port=5000)