# Flask Weather Forecasting App

This is a Flask web application that predicts weather conditions for the next 3 days based on user input. The predictions are made using a neural network model, and the results are stored in a MySQL database.

## Features
- Input: Temperature, Humidity, Wind Speed, Pressure, Precipitation Type (Rain or Snow).
- Neural network prediction for 3-day weather forecast.
- Saves input and forecast data into a MySQL database.
- Generates two plots: 
  1. Line plot of predicted data over 3 days.
  2. Scatter plot of neural network predictions.

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/tranbaquang22/web_khituongthuyvan.git
    ```
    

2. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Configure your MySQL connection settings in `config.py` (which is not included in this repo for security reasons).

4. Run the Flask app:
    ```
    flask run
    
    or

    python app.py
    ```

## Database

To create the MySQL database table, use the following SQL:

```sql
CREATE TABLE weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperature FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    wind_speed FLOAT NOT NULL,
    pressure FLOAT NOT NULL,
    precip_type INT NOT NULL,  -- 0: Rain, 1: Snow
    day_1_temp FLOAT NOT NULL,
    day_2_temp FLOAT NOT NULL,
    day_3_temp FLOAT NOT NULL,
    day_1_humidity FLOAT NOT NULL,
    day_2_humidity FLOAT NOT NULL,
    day_3_humidity FLOAT NOT NULL,
    day_1_wind_speed FLOAT NOT NULL,
    day_2_wind_speed FLOAT NOT NULL,
    day_3_wind_speed FLOAT NOT NULL,
    day_1_pressure FLOAT NOT NULL,
    day_2_pressure FLOAT NOT NULL,
    day_3_pressure FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
