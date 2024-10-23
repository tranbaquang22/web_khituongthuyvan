from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import matplotlib.pyplot as plt
from models.weather_model import WeatherModel
from config import get_db_connection

app = Flask(__name__)

# Trang chủ: form nhập dữ liệu
@app.route('/')
def index():
    return render_template('index.html')

# Xử lý dữ liệu nhập vào, dự báo và lưu kết quả
@app.route('/forecast', methods=['POST'])
def forecast():
    if request.method == 'POST':
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        wind_speed = float(request.form['wind_speed'])
        pressure = float(request.form['pressure']) 
        precip_type = request.form['precip_type']

        # Mã hóa precip_type thành số
        
        precip_type_numeric = 0 if precip_type == "rain" else 1

        # Dự báo sử dụng mô hình mạng nơron
        model = WeatherModel()
        forecast_data = model.predict_next_3_days([temperature, humidity, wind_speed, pressure, precip_type_numeric])

        # Lưu dữ liệu nhập vào và kết quả vào MySQL
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO weather_data 
            (temperature, humidity, wind_speed, pressure, precip_type, 
            day_1_temp, day_2_temp, day_3_temp, day_1_humidity, day_2_humidity, day_3_humidity, 
            day_1_wind_speed, day_2_wind_speed, day_3_wind_speed, day_1_pressure, day_2_pressure, day_3_pressure) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (temperature, humidity, wind_speed, pressure, precip_type_numeric, 
             forecast_data['temperature'][0], forecast_data['temperature'][1], forecast_data['temperature'][2],
             forecast_data['humidity'][0], forecast_data['humidity'][1], forecast_data['humidity'][2],
             forecast_data['wind_speed'][0], forecast_data['wind_speed'][1], forecast_data['wind_speed'][2],
             forecast_data['pressure'][0], forecast_data['pressure'][1], forecast_data['pressure'][2])
        )
        conn.commit()
        cursor.close()
        conn.close()

        # Vẽ biểu đồ kết quả dự báo 3 ngày
        days = ['Day 1', 'Day 2', 'Day 3']
        plt.figure()
        plt.plot(days, forecast_data['temperature'], label="Temperature (C)")
        plt.plot(days, forecast_data['humidity'], label="Humidity")
        plt.plot(days, forecast_data['wind_speed'], label="Wind Speed (km/h)")
        plt.plot(days, forecast_data['pressure'], label="Pressure (millibars)")
        plt.xlabel('Days')
        plt.ylabel('Values')
        plt.title('3-Day Weather Forecast')
        plt.legend()
        plt.savefig('static/data/forecast.png')

        # Vẽ biểu đồ tán xạ 
        plt.figure()

        # Điểm dữ liệu 
        x_values = np.linspace(1, 100, 100)
        temperature_values = np.linspace(temperature, forecast_data['temperature'][0], 100)
        humidity_values = np.linspace(humidity, forecast_data['humidity'][0], 100)
        wind_speed_values = np.linspace(wind_speed, forecast_data['wind_speed'][0], 100)

        # Vẽ biểu đồ tán xạ với nhiều điểm
        plt.scatter(x_values, temperature_values, label="Temperature", color='blue', alpha=0.5)
        plt.scatter(x_values, humidity_values, label="Humidity", color='green', alpha=0.5)
        plt.scatter(x_values, wind_speed_values, label="Wind Speed", color='red', alpha=0.5)

        plt.xlabel('Time Steps')
        plt.ylabel('Values')
        plt.title('Neural Network Scatter Plot (Dense)')
        plt.legend()
        plt.savefig('static/data/neural_network_scatter.png')

        return redirect(url_for('result'))

# Trang kết quả dự báo
@app.route('/result')
def result():
    # Lấy kết quả dự báo gần nhất từ cơ sở dữ liệu
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather_data ORDER BY id DESC LIMIT 1")
    latest_result = cursor.fetchone()
    cursor.close()
    conn.close()

    # Kiểm tra xem có dữ liệu không
    if latest_result:
        forecast = {
            'temperature': [latest_result[6], latest_result[7], latest_result[8]],
            'humidity': [latest_result[9], latest_result[10], latest_result[11]],
            'wind_speed': [latest_result[12], latest_result[13], latest_result[14]],
            'pressure': [latest_result[15], latest_result[16], latest_result[17]],
        }
        return render_template('result.html', forecast=forecast)
    else:
        return "Không có dự báo nào trước đó. Vui lòng nhập dữ liệu dự báo."

if __name__ == '__main__':
    app.run(debug=True)
