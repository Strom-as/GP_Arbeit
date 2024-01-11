import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
import random

# Verbindung zur MySQL-Datenbank herstellen
dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123456",
    database="london_weather"
)

# Funktion zum Daten aus der Datenbank abrufen
def fetch_data():
    cursor = dataBase.cursor()
    query = "SELECT * FROM london_weather"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data

# Funktion zum Daten in die Datenbank einfügen
def insert_data(date, cloud_cover, sunshine, max_temp, mean_temp, min_temp, precipitation, pressure, snow_depth):
    try:
        cursor = dataBase.cursor()
        query = "INSERT INTO london_weather (date, cloud_cover, sunshine, max_temp, mean_temp, min_temp, precipitation, pressure, snow_depth) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (date, cloud_cover, sunshine, max_temp, mean_temp, min_temp, precipitation, pressure, snow_depth)
        cursor.execute(query, values)
        dataBase.commit()
        cursor.close()
        st.success("Data added successfully!")
    except Exception as e:
        st.error(f"Error adding data: {e}")

# Funktion zum Daten in der Datenbank aktualisieren
def update_data(row_id, date, cloud_cover, sunshine, max_temp, mean_temp, min_temp, precipitation, pressure, snow_depth):
    try:
        cursor = dataBase.cursor()
        query = "UPDATE london_weather SET date=%s, cloud_cover=%s, sunshine=%s, max_temp=%s, mean_temp=%s, min_temp=%s, precipitation=%s, pressure=%s, snow_depth=%s WHERE id=%s"
        values = (date, cloud_cover, sunshine, max_temp, mean_temp, min_temp, precipitation, pressure, snow_depth, row_id)
        cursor.execute(query, values)
        dataBase.commit()
        cursor.close()
        st.success("Data updated successfully!")
    except Exception as e:
        st.error(f"Error updating data: {e}")

# Streamlit-Anwendung
def main():
    # Seite konfigurieren
    st.set_page_config(page_title='London Weather App', page_icon=':sunny:', layout='wide', initial_sidebar_state='expanded')

    # Daten aus der Datenbank abrufen
    data = fetch_data()

    # Daten in DataFrame konvertieren
    columns = ["id", "date", "cloud_cover", "sunshine", "max_temp", "mean_temp", "min_temp", "precipitation", "pressure", "snow_depth"]
    df = pd.DataFrame(data, columns=columns)

    # Seitenmenü erstellen
    st.sidebar.title('Navigation')
    menu_options = {
        "Raw Data": {"icon": "📊", "title": "Raw Data"},
        "Temperature Chart": {"icon": "🌡️", "title": "Temperature Chart"},
        "Precipitation and Snow Depth Chart": {"icon": "🌧️", "title": "Precipitation and Snow Depth Chart"},
        "Cloud Cover and Sunshine Chart": {"icon": "⛅", "title": "Cloud Cover and Sunshine Chart"},
        "Manual Data Entry": {"icon": "📝", "title": "Manual Data Entry"},
    }
    page = st.sidebar.radio("", list(menu_options.keys()), format_func=lambda option: f"{menu_options[option]['icon']} {menu_options[option]['title']}")

    # Seite für Rohdaten anzeigen
    if page == "Raw Data":
        st.title('London Weather Data')
        st.write("### Raw Data")
        st.dataframe(df, height=400, width=1000)  # Höhe auf 400 Pixel und Breite auf 1000 Pixel setzen

    # Seite für Temperaturdiagramme anzeigen
    elif page == "Temperature Chart":
        st.title(menu_options[page]["title"])
        st.write("### Temperature Chart")
        st.line_chart(df.set_index('date')[["max_temp", "min_temp", "mean_temp"]])

    # Seite für Niederschlags- und Schneehöhendiagramme anzeigen
    elif page == "Precipitation and Snow Depth Chart":
        st.title(menu_options[page]["title"])
        st.write("### Precipitation and Snow Depth Chart")
        st.line_chart(df.set_index('date')[["precipitation", "snow_depth"]])

    # Seite für Cloud Cover und Sunshine Diagramm anzeigen
    elif page == "Cloud Cover and Sunshine Chart":
        st.title(menu_options[page]["title"])
        st.write("### Cloud Cover and Sunshine Chart")
        st.line_chart(df.set_index('date')[["cloud_cover", "sunshine"]])

    # Seite für manuelle Dateneingabe anzeigen
    elif page == "Manual Data Entry":
        st.title(menu_options[page]["title"])
        st.write("### Manual Data Entry")

        # Daten manuell hinzufügen
        date_input = st.date_input("Date", datetime.now())
        cloud_cover_input = st.number_input("Cloud Cover", min_value=0.0, max_value=10.0, value=0.0)
        sunshine_input = st.number_input("Sunshine", min_value=0.0, max_value=16.0, value=0.0)
        max_temp_input = st.number_input("Max Temperature", value=0.0)
        min_temp_input = st.number_input("Min Temperature", value=0.0)
        mean_temp_input = (max_temp_input + min_temp_input) / 2  # Berechnung des Durchschnitts
        precipitation_input = st.number_input("Precipitation", value=0.0)
        pressure_input = st.number_input("Pressure", min_value=90000, max_value=110000, value=100000)
        snow_depth_input = st.number_input("Snow Depth", value=0.0)

        if st.button("Add Data"):
            insert_data(date_input, cloud_cover_input, sunshine_input, max_temp_input, mean_temp_input, min_temp_input, precipitation_input, pressure_input, snow_depth_input)


if __name__ == '__main__':
    main()
