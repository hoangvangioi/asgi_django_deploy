import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from .models import Message
from django.utils import timezone
from tensorflow.keras.models import load_model
import joblib
import pandas as pd


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']

        # Lưu tin nhắn vào database với thông tin thời gian
        message = Message.objects.create(content=message_content, timestamp=timezone.now())

        # Gửi tin nhắn và thông tin thời gian tạo đến tất cả các clients
        self.send(text_data=json.dumps({
            'message': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }))



class TensorflowConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            # Nhận dữ liệu từ WebSocket (ở đây giả sử dữ liệu là JSON)
            data = json.loads(text_data)

            # Load mô hình và scaler
            model = load_model('./app/iot.keras')
            scaler = joblib.load('./app/scaler.joblib')

            # Chuẩn hóa dữ liệu
            new_data = pd.DataFrame(data, index=[0])
            new_data_scaled = scaler.transform(new_data)

            # Dự đoán với mô hình
            prediction = model.predict(new_data_scaled)

            # Chuyển đổi giá trị dự đoán thành nhãn (ví dụ: > 0.5 là 1, ngược lại là 0)
            predicted_label = (prediction > 0.5).astype('int32')

            # Gửi kết quả dự đoán qua WebSocket
            await self.send(text_data=json.dumps({'prediction': predicted_label[0][0]}))
        except Exception as e:
            # Gửi thông báo lỗi qua WebSocket
            await self.send(text_data=json.dumps({'error': str(e)}))
