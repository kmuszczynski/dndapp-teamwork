import json
from turtle import update
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
		type = text_data_json['type']
		message = text_data_json['message']
		room = await database_sync_to_async(ChatRoom.objects.get)(name=self.room_name)

		if type=="grid":
			grid = message.split(" ")
			await database_sync_to_async(ChatRoom.objects.filter(name=self.room_name).update)(grid_x=int(grid[0]))
			await database_sync_to_async(ChatRoom.objects.filter(name=self.room_name).update)(grid_y=int(grid[1]))

			await self.channel_layer.group_send(
				self.room_group_name,
				{
					'type': 'chat_grid',
					'x': grid[0],
					'y': grid[1],
				})

		if type=="message" or type=="roll":
			date = datetime.now().ctime().split(' ')[3][:5]

			chat = Chat(
						content=message,
                    	#content=run_commands(message),
                    	user=self.scope['user'],
                    	room=room,
               			timestamp="[%s]" % date
                	)

			await database_sync_to_async(chat.save)()

			await self.channel_layer.group_send(
				self.room_group_name,
				{
					'type': 'chat_message',
					'message': message,
					'user': str(self.scope["user"]),
					'date': "%s" % date,
				})

	async def chat_message(self, event):
		msg = event['message']
		msgDate = event['date']
		msgAuth = event['user']

		await self.send(text_data=json.dumps({
			'type': "message",
			'messageDateSent': msgDate,
			'messageAuthor': msgAuth,
			'message': msg,
		}, default=str))

	async def chat_grid(self, event):
		x = event['x']
		y = event['y']

		await self.send(text_data=json.dumps({
			'type': "grid",
			'x': x,
			'y': y,
		}, default=str))