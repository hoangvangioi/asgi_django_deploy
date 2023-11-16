# import json
# from channels.generic.websocket import WebsocketConsumer
# from .models import Message


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Lưu tin nhắn vào database
#         Message.objects.create(content=message)

#         self.send(text_data=json.dumps({
#             'message': message
#         }))


import json
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from django.utils import timezone

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
