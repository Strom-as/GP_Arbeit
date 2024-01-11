import pandas as pd
#import pymysql
import mysql.connector
from datetime import datetime
from datetime import timedelta
import time
import random
 
dataBase = mysql.connector.connect(
    host= "localhost",
    user="root",
    passwd="123456",
    database="london_weather"
)

#df = pd.read_csv(r"C:\Users\thoma\london_weather_mysql.csv")
#print(df)

#READ
#preparing a cursor object
cursorObject = dataBase.cursor()
#creating database
cursorObject.execute("SELECT * from london_weather")
response = cursorObject.fetchall()
"""
#print(response)
for o in response:
    print(o)
#disconnecting from server
dataBase.close()
"""


#WRITE
# Funktion zum Zufallsdaten generieren (durch echte Sensorwerte zu ersetzen)
def generate_random_data():
    date = datetime.now().strftime('%Y-%m-%d')
    cloud_cover = random.uniform(0, 8)
    sunshine = random.uniform(0, 15)
    max_temperature = random.uniform(-4, 32)
    min_temperature = random.uniform(-10, 22)
    mean_temperature = (max_temperature + min_temperature) / 2
    precipitation = random.uniform(0, 60)
    pressure = random.uniform(96000, 105000)
    snow_depth = random.uniform(0, 22)

    return date, cloud_cover, sunshine, max_temperature, mean_temperature, min_temperature, precipitation, pressure, snow_depth
    # print(date, cloud_cover, sunshine, max_temperature, mean_temperature, min_temperature, precipitation, pressure, snow_depth)


# Funktion zum Einfügen von Daten in die MySQL-Datenbank
def insert_london_weather(data):
    cursorObject = dataBase.cursor()
    query = "INSERT INTO london_weather (date, cloud_cover, sunshine, max_temperature, mean_temperature, min_temperature, precipitation, pressure, snow_depth) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursorObject.execute(query, data)
    dataBase.commit()
    cursorObject.close()

# Funktion, um die Stunden und Minuten einer Zeit zu überprüfen
def is_time_to_run():
    now = datetime.now()
    return now.hour == 16 and now.minute == 0

# Tägliche Ausführung des Programms um 23 Uhr
while True:
    if is_time_to_run():
        # Daten generieren
        sensor_data = generate_random_data()

        # Daten in die MySQL-Datenbank einfügen
        insert_london_weather(sensor_data)

        # Warte bis zum nächsten Tag um 23 Uhr
        tomorrow = datetime.now() + timedelta(days=1)
        next_run_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 23, 0, 0)
        sleep_time = (next_run_time - datetime.now()).seconds
        time.sleep(sleep_time)
    else:
        # Warte 1 Minute und überprüfe erneut
        time.sleep(60)