import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from datetime import datetime
from .models import Chat, ChatRoom

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = 'chat_%s' % self.room_name

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		date = datetime.now()
		minutes = date.minute
		if date.minute == "":
			minutes = "00"
		elif len(str(date.minute))==1:
			minutes = "0" + str(date.minute)

		room = await database_sync_to_async(ChatRoom.objects.get)(name=self.room_name)

		chat = Chat(
					content=message,
                    #content=run_commands(message),
                    user=self.scope['user'],
                    room=room,
               		timestamp="[%s:%s]" % (date.hour, minutes)
                )

		await database_sync_to_async(chat.save)()

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat_message',
				'message': message,
				'user': str(self.scope["user"]),
				'date': "%s:%s" % (date.hour, minutes),
			})

	async def chat_message(self, event):
		msg = event['message']
		msgDate = event['date']
		msgAuth = event['user']

		await self.send(text_data=json.dumps({
			'messageDateSent': msgDate,
			'messageAuthor': msgAuth,
			'message': msg,
		}, default=str))
