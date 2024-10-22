import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor

class WeatherModel:
    def __init__(self):
        # Load dữ liệu từ file CSV
        self.data = pd.read_csv('static/data/weatherHistory.csv')
        
        # Xử lý dữ liệu
        self.X, self.y = self.process_data()
        
        # Chia dữ liệu train/test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

        # Khởi tạo mô hình mạng nơron (MLP Regressor)
        self.model = MLPRegressor(hidden_layer_sizes=(100, 100), max_iter=500)

        # Huấn luyện mô hình
        self.train_model()

    def process_data(self):
        # Chọn các cột sử dụng để dự đoán: Temperature (C), Humidity, Wind Speed (km/h), Pressure (millibars), Precip Type
        features = ['Temperature (C)', 'Humidity', 'Wind Speed (km/h)', 'Pressure (millibars)', 'Precip Type']
        target = ['Temperature (C)', 'Humidity', 'Wind Speed (km/h)', 'Pressure (millibars)']
        
        # Loại bỏ các giá trị thiếu
        self.data = self.data.dropna(subset=features)
        
        # Mã hóa cột 'Precip Type': 'rain' -> 0, 'snow' -> 1
        self.data['Precip Type'] = self.data['Precip Type'].apply(lambda x: 0 if x == 'rain' else 1)
        
        X = self.data[features].values
        y = self.data[target].values
        
        return X, y

    def train_model(self):
        # Huấn luyện mô hình
        self.model.fit(self.X_train, self.y_train)

    def predict_next_3_days(self, input_data):
    # Chuyển input_data thành mảng numpy có dạng 2D với 1 hàng (dòng) và nhiều cột
        input_data = np.array(input_data).reshape(1, -1)
        
        # Tạo mảng để lưu kết quả dự đoán cho 3 ngày
        predictions = []

        # Dự đoán cho ngày thứ nhất
        day_1_pred = self.model.predict(input_data)
        predictions.append(day_1_pred[0])  # Lưu kết quả dự đoán cho ngày 1

        # Dự đoán cho ngày thứ hai, sử dụng toàn bộ thông tin từ ngày thứ nhất và thêm precip_type từ input_data
        day_2_input = np.concatenate([day_1_pred, input_data[:, -1:]], axis=1)  # Ghép thêm precip_type vào kết quả ngày 1
        day_2_pred = self.model.predict(day_2_input)
        predictions.append(day_2_pred[0])  # Lưu kết quả dự đoán cho ngày 2

        # Dự đoán cho ngày thứ ba, sử dụng toàn bộ thông tin từ ngày thứ hai và thêm precip_type từ input_data
        day_3_input = np.concatenate([day_2_pred, input_data[:, -1:]], axis=1)  # Ghép thêm precip_type vào kết quả ngày 2
        day_3_pred = self.model.predict(day_3_input)
        predictions.append(day_3_pred[0])  # Lưu kết quả dự đoán cho ngày 3

        # Chuyển kết quả thành dictionary để trả về
        predictions = np.array(predictions)
        forecast_data = {
            'temperature': predictions[:, 0].tolist(),
            'humidity': predictions[:, 1].tolist(),
            'wind_speed': predictions[:, 2].tolist(),
            'pressure': predictions[:, 3].tolist()
        }

        return forecast_data
