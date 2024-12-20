from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(
            self.room_group_name,self.channel_layer
        )
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,self.channel_layer
        )
    
    async def receive(self,text_data):
        data = json.loads(text_data)
        message = data["message"]
        sender = data["username"]
        room = data["room"]

        await self.channel_layer.group_send(
            self.room_group_name,{
                "type":"chat_message",
                "message":message,
                "room":room,
                "sender":sender
            }
        )

    async def chat_message(self,event):
        message = event["message"]
        sender = event["username"]
        room = event["room"]
        await self.send(
            text_data=json.dumps({
                "message":message,
                "room":room,
                "sender":sender
            })
        )
