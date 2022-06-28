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
		elif message_type == "activate_grid":
			await database_sync_to_async(Grid.objects.filter(room__name=self.room_name).filter(status=1).update)(status=2)
			await database_sync_to_async(Grid.objects.filter(room__name=self.room_name).filter(id=int(message)).update)(status=1)

			grid = await database_sync_to_async(Grid.objects.filter(room__name=self.room_name).get)(status=1)
			gridAreaWithCharacter = await database_sync_to_async(list)(GridAreaWithCharacter.objects.filter(grid=grid))

			gridAreaWithCharacterIdList = []
			for i in range(len(gridAreaWithCharacter)):
				x = []
				x.append(gridAreaWithCharacter[i].column)
				x.append(gridAreaWithCharacter[i].row)
				x.append(gridAreaWithCharacter[i].character)
				x.append(gridAreaWithCharacter[i].color)
				gridAreaWithCharacterIdList.append(x)

			await self.channel_layer.group_send(
				self.room_group_name, {
					'type': 'chat_grid',
					'x': grid.columns,
					'y': grid.rows,
					'gridAreaWithCharacter': json.dumps(gridAreaWithCharacterIdList),
				})
		elif message_type == "set_token_name" or message_type == "set_token_color":
			grid = await database_sync_to_async(Grid.objects.filter(room__name=self.room_name).get)(status=1)
			gridAreaWithCharacter = await database_sync_to_async(list)(GridAreaWithCharacter.objects.filter(grid=grid))

			message = message.split(" ")
			message[0]=message[0].replace('x', '').split("y")
			x = int(message[0][0])
			y = int(message[0][1])
			if message_type == "set_token_name":
				name = message[1]
				color = "#ffffff"
			else:
				name = "?"
				color = message[1]

			id = -1
			for i in range(len(gridAreaWithCharacter)):
				if gridAreaWithCharacter[i].row == y and gridAreaWithCharacter[i].column == x:
					id = gridAreaWithCharacter[i].id

			girdArea = None

			if id != -1:
				if message_type == "set_token_name":
					await database_sync_to_async(GridAreaWithCharacter.objects.filter(id=id).update)(character=name)
				else:
					await database_sync_to_async(GridAreaWithCharacter.objects.filter(id=id).update)(color=color)
				
				gridArea = await database_sync_to_async(GridAreaWithCharacter.objects.filter(id=id).first)()
			else:
				gridArea = GridAreaWithCharacter(
					column=x,
					row=y,
					grid=grid,
					character=name,
					color=color,
				)
				await database_sync_to_async(gridArea.save)()
			
			await self.channel_layer.group_send(
				self.room_group_name, {
					'type': 'update_token',
					'x': gridArea.column,
					'y': gridArea.row,
					'character': gridArea.character,
					'color': gridArea.color,
				}
			)
		elif message_type == "token_move":
			element_id, key = message.split(" ")

			x, y = element_id.replace("x", "").split("y")
			x = int(x); y = int(y)

			grid = await database_sync_to_async(Grid.objects.filter(room__name=self.room_name).get)(status=1)
			gridAreaWithCharacter = await database_sync_to_async(list)(GridAreaWithCharacter.objects.filter(grid=grid))

			db_id = -1
			for i in range(len(gridAreaWithCharacter)):
				if gridAreaWithCharacter[i].row == y and gridAreaWithCharacter[i].column == x:
					db_id = gridAreaWithCharacter[i].id

			if(db_id!=-1):
				token = await database_sync_to_async(GridAreaWithCharacter.objects.filter(id=db_id).get)()

				if(key == "up"):
					if(y==0):
						await database_sync_to_async(GridAreaWithCharacter.objects.filter(id=db_id).delete)()
						new_x = -1; new_y = -1
					else:
						await database_sync_to_async(GridAreaWithCharacter.objects.filter(id=db_id).update)(row=y-1)
						new_x = token.column; new_y = token.row-1
				elif(key == "down"):
					if(y==(grid.rows-1)):
						await database_sync_to_async(GridAreaWithCharacter.objects.filter(id=db_id).delete)()
						new_x = -1; new_y = -1
					else:
						await database_sync_to_async(GridAreaWithCharacter.objects.filter(id=db_id).update)(row=y+1)
						new_x = token.column; new_y = token.row+1
				elif(key == "left"):
					if(x==0):
						await database_sync_to_async(GridAreaWithCharacter.objects.filter(id=db_id).delete)()
						new_x = -1; new_y = -1
					else:
						await database_sync_to_async(GridAreaWithCharacter.objects.filter(id=db_id).update)(column=x-1)
						new_x = token.column-1; new_y = token.row
				elif(key == "right"):
					if(x == (grid.columns-1)):
						await database_sync_to_async(GridAreaWithCharacter.objects.filter(id=db_id).delete)()
						new_x = -1; new_y = -1
					else:
						await database_sync_to_async(GridAreaWithCharacter.objects.filter(id=db_id).update)(column=x+1)
						new_x = token.column+1; new_y = token.row

				await self.channel_layer.group_send(
					self.room_group_name, {
						'type': 'move_token',
						'old_x': x,
						'old_y': y,
						'new_x': new_x,
						'new_y': new_y,
						'character': token.character,
						'color': token.color,
					}
				)

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
	
	async def update_token(self, event):
		x = event['x']
		y = event['y']
		character = event['character']
		color = event['color']

		await self.send(text_data=json.dumps({
			'type': "update_token",
			'x': x,
			'y': y,
			'character': character,
			'color': color,
		}, default=str))

	async def move_token(self, event):
		old_x = event['old_x']
		old_y = event['old_y']
		new_x = event['new_x']
		new_y = event['new_y']
		character = event['character']
		color = event['color']

		await self.send(text_data=json.dumps({
            'type': "move_token",
            'old_x': old_x,
            'old_y': old_y,
            'new_x': new_x,
        	'new_y': new_y,
            'character': character,
            'color': color,
        }, default=str))
