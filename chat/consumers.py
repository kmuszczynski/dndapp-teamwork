import json
from turtle import update
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from datetime import datetime
from .models import Chat, ChatRoom
from grid.models import Grid, GridAreaWithCharacter


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
		message_type = text_data_json['type']
		message = text_data_json['message']
		room = await database_sync_to_async(ChatRoom.objects.get)(name=self.room_name)

		if message_type=="grid":
			args = message.split(" ")

			grid = Grid(
				name = args[0],
				columns = int(args[1]),
				rows = int(args[2]),
				status = 2,
				room = room,
			)

			await database_sync_to_async(grid.save)()

			await self.channel_layer.group_send(
				self.room_group_name,{
					'type': 'add_grid_to_list',
					'id': grid.id,
					'name': grid.name,
					'x': grid.columns,
					'y': grid.rows,
				})
		elif message_type=="message" or message_type=="roll":
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
		elif message_type == "activate_grid" or message_type == "set_token_name":
			grid = await database_sync_to_async(Grid.objects.filter(room__name=self.room_name).get)(status=1)
			gridAreaWithCharacter = await database_sync_to_async(list)(GridAreaWithCharacter.objects.filter(grid=grid))

			if message_type == "activate_grid":
				print("dupa")
				await database_sync_to_async(Grid.objects.filter(room__name=self.room_name).filter(status=1).update)(status=2)
				await database_sync_to_async(Grid.objects.filter(room__name=self.room_name).filter(id=int(message)).update)(status=1)
			else:
				message = message.split(" ")
				message[0]=message[0].replace('x', '').split("y")
				x = int(message[0][0])
				y = int(message[0][1])
				name = message[1]

				id = -1
				for i in range(len(gridAreaWithCharacter)):
					if gridAreaWithCharacter[i].row == y and gridAreaWithCharacter[i].column == x:
						id = gridAreaWithCharacter[i].id
				
				if id != -1:
					await database_sync_to_async(GridAreaWithCharacter.objects.filter(id=id).update)(character=name)
				else:
					gridArea = GridAreaWithCharacter(
						column=x,
						row=y,
						grid=grid,
						character=name,
					)
					await database_sync_to_async(gridArea.save)()

			grid = await database_sync_to_async(Grid.objects.filter(room__name=self.room_name).get)(status=1)
			gridAreaWithCharacter = await database_sync_to_async(list)(GridAreaWithCharacter.objects.filter(grid=grid))
			gridAreaWithCharacterIdList = []
			for i in range(len(gridAreaWithCharacter)):
				x = []
				x.append(gridAreaWithCharacter[i].column)
				x.append(gridAreaWithCharacter[i].row)
				x.append(gridAreaWithCharacter[i].character)
				gridAreaWithCharacterIdList.append(x)

			await self.channel_layer.group_send(
				self.room_group_name,{
					'type': 'chat_grid',
					'x': grid.columns,
					'y': grid.rows,
					'gridAreaWithCharacter': json.dumps(gridAreaWithCharacterIdList),
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
		gridAreaWithCharacter = event['gridAreaWithCharacter']

		await self.send(text_data=json.dumps({
			'type': "change_grid",
			'x': x,
			'y': y,
			'gridAreaWithCharacter': gridAreaWithCharacter,
		}, default=str))

	async def add_grid_to_list(self, event):
		id = event['id']
		name = event['name']
		x = event['x']
		y = event['y']

		await self.send(text_data=json.dumps({
			'type': "add_grid_to_list",
			'id': id,
			'name': name,
			'x': x,
			'y': y,
		}, default=str))