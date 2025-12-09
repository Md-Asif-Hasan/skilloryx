import json
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync


class VideoCallConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'video_call_{self.room_name}'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive_json(self, content):
        # Broadcast message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'video_call_message',
                'message': content,
                'sender_channel_name': self.channel_name,
            }
        )

    def video_call_message(self, event):
        message = event['message']
        sender_channel_name = event['sender_channel_name']

        # Send message to WebSocket (exclude sender)
        if self.channel_name != sender_channel_name:
            self.send_json(message)


class NotificationConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.user_group_name = f'user_{self.username}'

        # Join user group
        async_to_sync(self.channel_layer.group_add)(
            self.user_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave user group
        async_to_sync(self.channel_layer.group_discard)(
            self.user_group_name,
            self.channel_name
        )

    def user_notification(self, event):
        message = event['message']
        self.send_json(message)
