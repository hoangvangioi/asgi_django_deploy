import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from keras.layers import Input
import joblib

# Load dữ liệu từ file CSV
dataset_path = './app/data.csv'
data = pd.read_csv(dataset_path)

# Xác định đặc trưng (features) và nhãn (labels)
features = data[['moisture', 'temp']]
labels = data['pump']

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Lưu scaler vào tệp
joblib.dump(scaler, './app/scaler.joblib')

# Xây dựng mô hình Neural Network
model = Sequential([
    Input(shape=(2,)),
    Dense(10, activation='relu'),
    Dense(5, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile mô hình
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Huấn luyện mô hình
history = model.fit(X_train_scaled, y_train, epochs=100, batch_size=8, validation_data=(X_test_scaled, y_test))

# Lưu mô hình đã huấn luyện
model.save('./app/iot.keras')

# Đánh giá mô hình trên tập kiểm tra
y_pred = (model.predict(X_test_scaled) > 0.5).astype('int32')
test_accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy on Test Set: {test_accuracy}')

# Vẽ đồ thị độ chính xác trên tập huấn luyện và tập kiểm tra
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Dự đoán với dữ liệu mới
new_data = pd.DataFrame({'moisture': [900], 'temp': [33]})

# Load lại scaler từ tệp đã lưu
scaler = joblib.load('./app/scaler.joblib')

# Chuẩn hóa dữ liệu mới
new_data_scaled = scaler.transform(new_data)

# Dự đoán với mô hình đã được load
prediction = model.predict(new_data_scaled)

# Chuyển đổi giá trị dự đoán thành nhãn (0 hoặc 1)
predicted_label = (prediction > 0.5).astype('int32')

# In kết quả dự đoán và nhãn
print(f'Prediction for new data: {predicted_label}')