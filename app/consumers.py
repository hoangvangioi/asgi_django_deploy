import json
from channels.generic.websocket import WebsocketConsumer
from .models import Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Lưu tin nhắn vào database
        Message.objects.create(content=message)

        self.send(text_data=json.dumps({
            'message': message
        }))
