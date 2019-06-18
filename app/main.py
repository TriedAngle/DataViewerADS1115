from flask import Flask, render_template, flash, redirect, send_from_directory
import os
import glob
import random
import time
import socket
import threading
import pickle
import csv
import subprocess


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
def dict_from_csv(year, month, day, hour, minute, values):
    dic = {}
    dic["year"] = year
    dic["month"] = month
    dic["day"] = day
    dic["hour"] = hour
    dic["minute"] = minute
    dic["value-0"] = values[0]
    dic["value-1"] = values[1]
    dic["value-2"] = values[2]
    dic["value-3"] = values[3]
    return dic

def read_data():
    if os.path.isfile(os.getcwd() + "/data.csv"):
        with open('data.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    pass
                
                values = [row[0],row[1],row[2],row[3]]
                year = row[4]
                month = row[5]
                day = row[6]
                hour = row[7]
                minute = row[8]
                data.append(dict_from_csv(year, month, day, hour, minute, values))
                line_count += 1
        
    if os.path.isfile(os.getcwd() + "/data.csv"):
        amount = 0
        for i in glob.glob(os.getcwd() + "/data_backups/*"):
            amount += 1

        subprocess.call(["cp", os.getcwd() + "/data.csv", os.getcwd() + "/data_backups/data" + str(amount) + ".csv" ])


def saveData(data_to_save):
    if not os.path.isfile(os.getcwd() + "/data.csv"):
        subprocess.call(["touch", os.getcwd() + "/data.csv"])

    with open('data.csv', mode='w') as employee_file:
        writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for entry in data_to_save:
            writer.writerow([entry["value-0"], entry["value-1"], entry["value-2"], entry["value-3"], entry["year"], entry["month"], entry["day"], entry["hour"], entry["minute"] ])
            

def get_data():
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
            temp_data_dict = pickle.loads(s.recv(2048))
            data.append(temp_data_dict)
        except:
            print("Error - Could not Retrieve Data")


# sites
@app.route('/')
@app.route('/home')
def home():
    return render_template('Home.html', title='Home', user=user)


@app.route('/data')
def rtmeasure():
    return render_template('Data.html', title='Data', data=data, user=user)


@app.route('/download', methods=["POST"])
def download():
    saveData(data)
    if os.path.isfile(os.getcwd() + "/data.csv"):
        return send_from_directory(os.getcwd(), filename="data.csv", as_attachment=True)
    else:
        return redirect("/data")


read_data()
thread_receive = threading.Thread(target=get_data, args=())
thread_receive.start()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
