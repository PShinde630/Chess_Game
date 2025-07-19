# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class ChessConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.game_id = self.scope['url_route']['kwargs']['game_id']
#         self.group_name = f"game_{self.game_id}"

#         # Add this connection to the group
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Remove this connection from the group
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         if data['type'] == 'make_move':
#             await self.channel_layer.group_send(
#                 self.group_name,
#                 {
#                     'type': 'broadcast_move',
#                     'move': data['move']
#                 }
#             )

#     async def broadcast_move(self, event):
#         await self.send(text_data=json.dumps({
#             'type': 'update_board',
#             'move': event['move']
#         }))




# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class ChessConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.game_id = self.scope['url_route']['kwargs']['game_id']
#         self.group_name = f"game_{self.game_id}"

#         # Add this connection to the group
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()
#         print(f"WebSocket connected for game: {self.game_id}")

#     async def disconnect(self, close_code):
#         # Remove this connection from the group
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )
#         print(f"WebSocket disconnected for game: {self.game_id}")

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message_type = data.get('type')

#         if message_type == 'make_move':
#             await self.handle_make_move(data)
#         elif message_type == 'resign':
#             await self.handle_resign(data)
#         elif message_type == 'send_challenge':
#             await self.handle_challenge(data)
#         elif message_type == 'accept_challenge':
#             await self.handle_accept_challenge(data)
#         elif message_type == 'decline_challenge':
#             await self.handle_decline_challenge(data)

#     async def handle_make_move(self, data):
#         move = data.get('move')
#         if not move:
#             return

#         # Broadcast the move to the group
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type': 'broadcast_move',
#                 'move': move,
#             }
#         )

#     async def handle_resign(self, data):
#         # Broadcast resignation to the group
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type': 'broadcast_resign',
#                 'player': self.scope['user'].username,
#             }
#         )

#     async def handle_challenge(self, data):
#         opponent_id = data.get('opponent_id')
#         if not opponent_id:
#             return

#         # Notify the challenged player
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type': 'broadcast_challenge',
#                 'challenger': self.scope['user'].username,
#                 'opponent_id': opponent_id,
#             }
#         )

#     async def handle_accept_challenge(self, data):
#         challenge_id = data.get('challenge_id')
#         if not challenge_id:
#             return

#         # Notify the group that the challenge was accepted
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type': 'broadcast_accept_challenge',
#                 'challenger': self.scope['user'].username,
#             }
#         )

#     async def handle_decline_challenge(self, data):
#         challenge_id = data.get('challenge_id')
#         if not challenge_id:
#             return

#         # Notify the group that the challenge was declined
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type': 'broadcast_decline_challenge',
#                 'challenger': self.scope['user'].username,
#             }
#         )

#     async def broadcast_move(self, event):
#         # Send the move to the WebSocket client
#         await self.send(text_data=json.dumps({
#             'type': 'update_board',
#             'move': event['move']
#         }))

#     async def broadcast_resign(self, event):
#         # Notify all clients about resignation
#         await self.send(text_data=json.dumps({
#             'type': 'resign',
#             'player': event['player']
#         }))

#     async def broadcast_challenge(self, event):
#         # Notify the opponent about the challenge
#         await self.send(text_data=json.dumps({
#             'type': 'challenge',
#             'challenger': event['challenger'],
#             'opponent_id': event['opponent_id'],
#         }))

#     async def broadcast_accept_challenge(self, event):
#         # Notify all clients about the accepted challenge
#         await self.send(text_data=json.dumps({
#             'type': 'accept_challenge',
#             'challenger': event['challenger']
#         }))

#     async def broadcast_decline_challenge(self, event):
#         # Notify all clients about the declined challenge
#         await self.send(text_data=json.dumps({
#             'type': 'decline_challenge',
#             'challenger': event['challenger']
#         }))




# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class ChessConsumer(AsyncWebsocketConsumer):
    # async def connect(self):
    #     self.group_name = "active_users"
    #     self.game_id = self.scope['url_route']['kwargs'].get('game_id')

    #     # Join the active users group
    #     await self.channel_layer.group_add(
    #         self.group_name,
    #         self.channel_name
    #     )
    #     await self.accept()
    #     print(f"WebSocket connected for group: {self.group_name}")

    #     # Notify all users of a new active user
    #     await self.channel_layer.group_send(
    #         self.group_name,
    #         {
    #             "type": "update_active_users",
    #             "user": self.scope["user"].username,
    #             "action": "connect",
    #         }
    #     )
    
    # async def connect(self):
    # if self.scope["user"].is_anonymous:
    #     await self.close()  # Reject the connection for unauthenticated users
    #     return

    # self.group_name = "active_users"

    # # Join the active users group
    # await self.channel_layer.group_add(
    #     self.group_name,
    #     self.channel_name
    # )
    # await self.accept()
    # print(f"WebSocket connected for user: {self.scope['user'].username}")

    # # Notify all users of a new active user
    # await self.channel_layer.group_send(
    #     self.group_name,
    #     {
    #         "type": "update_active_users",
    #         "user": self.scope["user"].username,
    #         "action": "connect",
    #     }
    # )

    # async def disconnect(self, close_code):
    #     # Leave the active users group
    #     await self.channel_layer.group_discard(
    #         self.group_name,
    #         self.channel_name
    #     )
    #     print(f"WebSocket disconnected for group: {self.group_name}")

    #     # Notify all users of a disconnected user
    #     await self.channel_layer.group_send(
    #         self.group_name,
    #         {
    #             "type": "update_active_users",
    #             "user": self.scope["user"].username,
    #             "action": "disconnect",
    #         }
    #     )

    # async def update_active_users(self, event):
    #     # Send active users update to all clients
    #     await self.send(text_data=json.dumps({
    #         "type": "active_users",
    #         "user": event["user"],
    #         "action": event["action"],
    #     }))

    # async def receive(self, text_data):
    #     data = json.loads(text_data)
    #     message_type = data.get('type')

    #     if message_type == 'make_move':
    #         await self.handle_make_move(data)
    #     elif message_type == 'resign':
    #         await self.handle_resign(data)
    #     elif message_type == 'send_challenge':
    #         await self.handle_challenge(data)
    #     elif message_type == 'accept_challenge':
    #         await self.handle_accept_challenge(data)
    #     elif message_type == 'decline_challenge':
    #         await self.handle_decline_challenge(data)

    # async def handle_make_move(self, data):
    #     move = data.get('move')
    #     if not move:
    #         return

    #     # Broadcast the move to the game group
    #     await self.channel_layer.group_send(
    #         self.group_name,
    #         {
    #             'type': 'broadcast_move',
    #             'move': move,
    #         }
    #     )

    # async def handle_resign(self, data):
    #     # Broadcast resignation to the group
    #     await self.channel_layer.group_send(
    #         self.group_name,
    #         {
    #             'type': 'broadcast_resign',
    #             'player': self.scope['user'].username,
    #         }
    #     )

    # async def handle_challenge(self, data):
    #     opponent_id = data.get('opponent_id')
    #     if not opponent_id:
    #         return

    #     # Notify the challenged player
    #     await self.channel_layer.group_send(
    #         self.group_name,
    #         {
    #             'type': 'broadcast_challenge',
    #             'challenger': self.scope['user'].username,
    #             'opponent_id': opponent_id,
    #         }
    #     )

    # async def handle_accept_challenge(self, data):
    #     challenge_id = data.get('challenge_id')
    #     if not challenge_id:
    #         return

    #     # Notify the group that the challenge was accepted
    #     await self.channel_layer.group_send(
    #         self.group_name,
    #         {
    #             'type': 'broadcast_accept_challenge',
    #             'challenger': self.scope['user'].username,
    #         }
    #     )

    # async def handle_decline_challenge(self, data):
    #     challenge_id = data.get('challenge_id')
    #     if not challenge_id:
    #         return

    #     # Notify the group that the challenge was declined
    #     await self.channel_layer.group_send(
    #         self.group_name,
    #         {
    #             'type': 'broadcast_decline_challenge',
    #             'challenger': self.scope['user'].username,
    #         }
    #     )

    # async def broadcast_move(self, event):
    #     # Send the move to the WebSocket client
    #     await self.send(text_data=json.dumps({
    #         'type': 'update_board',
    #         'move': event['move']
    #     }))

    # async def broadcast_resign(self, event):
    #     # Notify all clients about resignation
    #     await self.send(text_data=json.dumps({
    #         'type': 'resign',
    #         'player': event['player']
    #     }))

    # async def broadcast_challenge(self, event):
    #     # Notify the opponent about the challenge
    #     if str(self.scope["user"].id) == str(event["opponent_id"]):
    #         await self.send(text_data=json.dumps({
    #             "type": "challenge",
    #             "challenger": event["challenger"],
    #         }))

    # async def broadcast_accept_challenge(self, event):
    #     # Notify all clients about the accepted challenge
    #     await self.send(text_data=json.dumps({
    #         'type': 'accept_challenge',
    #         'challenger': event['challenger']
    #     }))

    # async def broadcast_decline_challenge(self, event):
    #     # Notify all clients about the declined challenge
    #     await self.send(text_data=json.dumps({
    #         'type': 'decline_challenge',
    #         'challenger': event['challenger']
    #     }))


# import json
# from channels.generic.websocket import AsyncWebsocketConsumer


# class ChessConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         if self.scope["user"].is_anonymous:
#             await self.close()  # Reject unauthenticated users
#             return

#         self.group_name = "active_users"

#         # Join the active users group
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()
#         print(f"WebSocket connected for user: {self.scope['user'].username}")

#         # Notify all users of a new active user
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "update_active_users",
#                 "user": self.scope["user"].username,
#                 "action": "connect",
#             }
#         )

#     async def disconnect(self, close_code):
#         # Leave the active users group
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )
#         print(f"WebSocket disconnected for group: {self.group_name}")

#         # Notify all users of a disconnected user
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "update_active_users",
#                 "user": self.scope["user"].username,
#                 "action": "disconnect",
#             }
#         )

#     async def update_active_users(self, event):
#         # Send active users update to all clients
#         await self.send(text_data=json.dumps({
#             "type": "active_users",
#             "user": event["user"],
#             "action": event["action"],
#         }))

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message_type = data.get("type")

#         if message_type == "make_move":
#             await self.handle_make_move(data)
#         elif message_type == "resign":
#             await self.handle_resign(data)
#         elif message_type == "send_challenge":
#             await self.handle_challenge(data)
#         elif message_type == "accept_challenge":
#             await self.handle_accept_challenge(data)
#         elif message_type == "decline_challenge":
#             await self.handle_decline_challenge(data)

#     async def handle_make_move(self, data):
#         move = data.get("move")
#         if not move:
#             return

#         # Broadcast the move to the game group
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "broadcast_move",
#                 "move": move,
#             }
#         )

#     async def handle_resign(self, data):
#         # Broadcast resignation to the group
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "broadcast_resign",
#                 "player": self.scope["user"].username,
#             }
#         )

#     async def handle_challenge(self, data):
#         opponent_id = data.get("opponent_id")
#         if not opponent_id:
#             return

#         # Notify the challenged player
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "broadcast_challenge",
#                 "challenger": self.scope["user"].username,
#                 "opponent_id": opponent_id,
#             }
#         )

#     async def handle_accept_challenge(self, data):
#         challenge_id = data.get("challenge_id")
#         if not challenge_id:
#             return

#         # Notify the group that the challenge was accepted
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "broadcast_accept_challenge",
#                 "challenger": self.scope["user"].username,
#             }
#         )

#     async def handle_decline_challenge(self, data):
#         challenge_id = data.get("challenge_id")
#         if not challenge_id:
#             return

#         # Notify the group that the challenge was declined
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "broadcast_decline_challenge",
#                 "challenger": self.scope["user"].username,
#             }
#         )

#     async def broadcast_move(self, event):
#         # Send the move to the WebSocket client
#         await self.send(text_data=json.dumps({
#             "type": "update_board",
#             "move": event["move"]
#         }))

#     async def broadcast_resign(self, event):
#         # Notify all clients about resignation
#         await self.send(text_data=json.dumps({
#             "type": "resign",
#             "player": event["player"]
#         }))

#     async def broadcast_challenge(self, event):
#         # Notify the opponent about the challenge
#         if str(self.scope["user"].id) == str(event["opponent_id"]):
#             await self.send(text_data=json.dumps({
#                 "type": "challenge",
#                 "challenger": event["challenger"],
#             }))

#     async def broadcast_accept_challenge(self, event):
#         # Notify all clients about the accepted challenge
#         await self.send(text_data=json.dumps({
#             "type": "accept_challenge",
#             "challenger": event["challenger"]
#         }))

#     async def broadcast_decline_challenge(self, event):
#         # Notify all clients about the declined challenge
#         await self.send(text_data=json.dumps({
#             "type": "decline_challenge",
#             "challenger": event["challenger"]
#         }))




# from channels.generic.websocket import AsyncWebsocketConsumer
# from .utils import add_active_user, remove_active_user, get_active_users
# # from django.contrib.auth.models import User
# import json


# REDIS_ACTIVE_USERS_KEY = "active_users"
# class ChessConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.challenge_group_name = f"user_{self.scope['user'].username}"
#         self.group_name = "active_users"
#         self.username = self.scope["user"].username

#         if not self.username:
#             await self.close()
#             return

#         # Add the current user to Redis
#         add_active_user(self.username)

#         # Join the WebSocket group
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#         await self.channel_layer.group_add(
#             self.challenge_group_name,
#             self.channel_name
#         )
#         await self.accept()

#         # Broadcast the updated active users list
#         await self.broadcast_active_users()

#     async def disconnect(self, close_code):
#         if self.username:
#             remove_active_user(self.username)

#         # Leave the WebSocket group
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#         await self.channel_layer.group_discard(
#             self.challenge_group_name,
#             self.channel_name
#         )
#         # Broadcast the updated active users list
#         await self.broadcast_active_users()

#     async def broadcast_active_users(self):
#         # Get the active users from Redis
#         active_users = list(get_active_users())
        
#         # Prevent sending empty or invalid usernames
#         active_users = [user for user in active_users if user]
        
#         # active_users = [user for user in active_users if user != self.username]

#         # Broadcast the active users list to all clients
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "update_active_users_list",
#                 "active_users": active_users,
                
                
#             }
#         )

#     async def update_active_users_list(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "active_users",
#             "active_users": event["active_users"],
#         }))

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message_type = data.get("type")

#         if message_type == "send_challenge":
#             await self.handle_challenge(data)
#         if message_type == "accept_challenge":
#             await self.handle_accept_challenge(data)

#     async def handle_challenge(self, data):
#         opponent_username = data.get("opponent_username")
#         if not opponent_username:
#             return

#         # Notify the specific opponent via their WebSocket group
#         await self.channel_layer.group_send(
#             f"user_{opponent_username}",  # Opponent's group
#             {
#                 "type": "challenge_notification",
#                 "challenger": self.username,  # Include challenger's username
#             }
#         )

#     async def challenge_notification(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "challenge_notification",
#             "challenger": event["challenger"],  # Send challenger username to the opponent
#         }))

#     async def game_start(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "game_start",
#             "game_id": event["game_id"],
#             "opponent": event["opponent"],
#         }))



# from channels.generic.websocket import AsyncWebsocketConsumer
# from .utils import add_active_user, remove_active_user, get_active_users
# import json


# REDIS_ACTIVE_USERS_KEY = "active_users"

# class ChessConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.challenge_group_name = f"user_{self.scope['user'].username}"
#         self.group_name = "active_users"
#         self.username = self.scope["user"].username

#         if not self.username:
#             await self.close()
#             return

#         # Add the current user to Redis
#         add_active_user(self.username)

#         # Join the WebSocket group
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.channel_layer.group_add(self.challenge_group_name, self.channel_name)
#         await self.accept()

#         # Broadcast the updated active users list
#         await self.broadcast_active_users()

#     async def disconnect(self, close_code):
#         if self.username:
#             remove_active_user(self.username)

#         # Leave the WebSocket groups
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)
#         await self.channel_layer.group_discard(self.challenge_group_name, self.channel_name)

#         # Broadcast the updated active users list
#         await self.broadcast_active_users()

#     async def broadcast_active_users(self):
#         active_users = list(get_active_users())
#         active_users = [user for user in active_users if user]

#         # Broadcast the active users list to all clients
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "update_active_users_list",
#                 "active_users": active_users,
#             },
#         )

#     async def update_active_users_list(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "active_users",
#             "active_users": event["active_users"],
#         }))

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message_type = data.get("type")

#         if message_type == "send_challenge":
#             await self.handle_challenge(data)
#         if message_type == "accept_challenge":
#             await self.handle_accept_challenge(data)
#         if message_type == "accept_challenge":
#             await self.handle_accept_challenge(data)

#     async def handle_challenge(self, data):
#         opponent_username = data.get("opponent_username")
#         if not opponent_username:
#             return

#         # Notify the specific opponent via their WebSocket group
#         await self.channel_layer.group_send(
#             f"user_{opponent_username}",
#             {
#                 "type": "challenge_notification",
#                 "challenger": self.username,
#             },
#         )

#     async def challenge_notification(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "challenge_notification",
#             "challenger": event["challenger"],
#         }))

#     async def request_active_users(self):
#         active_users = list(get_active_users())
#         active_users = [user for user in active_users if user]

#         await self.send(text_data=json.dumps({
#             "type": "active_users",
#             "active_users": active_users,
#         }))

#     async def game_start(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "game_start",
#             "game_id": event["game_id"],
#             "opponent": event["opponent"],
#         }))



# from channels.generic.websocket import AsyncWebsocketConsumer
# from .utils import add_active_user, remove_active_user, get_active_users
# # from django.contrib.auth.models import User
# import json


# REDIS_ACTIVE_USERS_KEY = "active_users"
# class ChessConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.challenge_group_name = f"user_{self.scope['user'].username}"
#         self.group_name = "active_users"
#         self.username = self.scope["user"].username

#         if not self.username:
#             await self.close()
#             return

#         # Add the current user to Redis
#         add_active_user(self.username)

#         # Join the WebSocket group
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#         await self.channel_layer.group_add(
#             self.challenge_group_name,
#             self.channel_name
#         )
#         await self.accept()

#         # Broadcast the updated active users list
#         await self.broadcast_active_users()

#     async def disconnect(self, close_code):
#         if self.username:
#             remove_active_user(self.username)

#         # Leave the WebSocket group
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#         await self.channel_layer.group_discard(
#             self.challenge_group_name,
#             self.channel_name
#         )
#         # Broadcast the updated active users list
#         await self.broadcast_active_users()

#     async def broadcast_active_users(self):
#         # Get the active users from Redis
#         active_users = list(get_active_users())
        
#         # Prevent sending empty or invalid usernames
#         active_users = [user for user in active_users if user]

#         # Broadcast the active users list to all clients
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "update_active_users_list",
#                 "active_users": active_users,
#             }
#         )

#     async def update_active_users_list(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "active_users",
#             "active_users": event["active_users"],
#         }))

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message_type = data.get("type")

#         if message_type == "send_challenge":
#             await self.handle_challenge(data)
#         if message_type == "accept_challenge":
#             await self.handle_accept_challenge(data)
#         if message_type == "accept_challenge":
#             await self.handle_accept_challenge(data)

#     async def handle_challenge(self, data):
#         opponent_username = data.get("opponent_username")
#         if not opponent_username:
#             return

#         # Notify the specific opponent via their WebSocket group
#         await self.channel_layer.group_send(
#             f"user_{opponent_username}",  # Opponent's group
#             {
#                 "type": "challenge_notification",
#                 "challenger": self.username,  # Include challenger's username
#             }
#         )

#     async def challenge_notification(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "challenge_notification",
#             "challenger": event["challenger"],  # Send challenger username to the opponent
#         }))

#     async def game_start(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "game_start",
#             "game_id": event["game_id"],
#             "opponent": event["opponent"],
#         }))


# from channels.generic.websocket import AsyncWebsocketConsumer
# from .utils import add_active_user, remove_active_user, get_active_users
# # from django.contrib.auth.models import User
# import json


# REDIS_ACTIVE_USERS_KEY = "active_users"
# class ChessConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.challenge_group_name = f"user_{self.scope['user'].username}"
#         self.group_name = "active_users"
#         self.username = self.scope["user"].username

#         if not self.username:
#             await self.close()
#             return

#         # Add the current user to Redis
#         add_active_user(self.username)

#         # Join the WebSocket group
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#         await self.channel_layer.group_add(
#             self.challenge_group_name,
#             self.channel_name
#         )
#         await self.accept()

#         # Broadcast the updated active users list
#         await self.broadcast_active_users()

#     async def disconnect(self, close_code):
#         if self.username:
#             remove_active_user(self.username)

#         # Leave the WebSocket group
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#         await self.channel_layer.group_discard(
#             self.challenge_group_name,
#             self.channel_name
#         )
#         # Broadcast the updated active users list
#         await self.broadcast_active_users()

#     async def broadcast_active_users(self):
#         # Get the active users from Redis
#         active_users = list(get_active_users())
        
#         # Prevent sending empty or invalid usernames
#         active_users = [user for user in active_users if user]

#         # Broadcast the active users list to all clients
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "update_active_users_list",
#                 "active_users": active_users,
#             }
#         )

#     async def update_active_users_list(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "active_users",
#             "active_users": event["active_users"],
#         }))

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message_type = data.get("type")

#         if message_type == "send_challenge":
#             await self.handle_challenge(data)
#         if message_type == "accept_challenge":
#             await self.handle_accept_challenge(data)
#         if message_type == "make_move":
#             await self.handle_make_move(data)
#         if message_type == "decline_challenge":  
#             await self.handle_decline_challenge(data)
#         if message_type == "resign":
#             await self.handle_resign(data)  
            
#     async def handle_resign(self, data):
#         opponent_username = data.get("opponent_username")
#         if not opponent_username:
#             return

#         # Notify the specific opponent via their WebSocket group
#         await self.channel_layer.group_send(
#             f"user_{opponent_username}",  # Opponent's group
#             {
#                 "type": "resign",
#                 "challenger": self.username,  # Include challenger's username
#             }
#         ) 
            
#     async def handle_make_move(self, data):
#         opponent_username = data.get("opponent_username")
#         if not opponent_username:
#             return

#         # Notify the specific opponent via their WebSocket group
#         await self.channel_layer.group_send(
#             f"user_{opponent_username}",  # Opponent's group
#             {
#                 "type": "make_move",
#                 "challenger": self.username,  # Include challenger's username
#             }
#         )

#     async def handle_challenge(self, data):
#         opponent_username = data.get("opponent_username")
#         if not opponent_username:
#             return

#         # Notify the specific opponent via their WebSocket group
#         await self.channel_layer.group_send(
#             f"user_{opponent_username}",  # Opponent's group
#             {
#                 "type": "challenge_notification",
#                 "challenger": self.username,  # Include challenger's username
#             }
#         )

#     async def challenge_notification(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "challenge_notification",
#             "challenger": event["challenger"],  # Send challenger username to the opponent
#         }))

#     async def game_start(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "game_start",
#             "game_id": event["game_id"],
#             "opponent": event["opponent"],
#         }))
        
#     async def make_move(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "make_move",
#             "game_id": event.get("game_id"),  # Add game_id if needed
#             "move": event.get("move")  # Add move details
#         }))

         
#     async def resign(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "resign",
#         }))
        
#     async def handle_decline_challenge(self, data):
#         challenger_username = data.get("challenger_username")
#         if not challenger_username:
#             return

#         # Notify the challenger that the challenge was declined
#         await self.channel_layer.group_send(
#             f"user_{challenger_username}",
#             {
#                 "type": "challenge_declined",
#                 "declined_by": self.username,
#             }
#         )

#     async def challenge_declined(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "challenge_declined",
#             "declined_by": event["declined_by"],
#         }))
                
                
                
                
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import add_active_user, remove_active_user, get_active_users
import json

REDIS_ACTIVE_USERS_KEY = "active_users"

class ChessConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_group_name = f"user_{self.scope['user'].username}"
        self.global_group_name = "active_users"
        self.current_user = self.scope["user"].username

        if not self.current_user:
            await self.close()
            return

        add_active_user(self.current_user)  

        # Join global and user-specific groups
        await self.channel_layer.group_add(self.global_group_name, self.channel_name)
        await self.channel_layer.group_add(self.user_group_name, self.channel_name)

        await self.accept()

        # Notify all clients about the updated active users
        await self.send_active_users_update()

    async def disconnect(self, close_code):
        if self.current_user:
            remove_active_user(self.current_user)

        # Leave all groups
        await self.channel_layer.group_discard(self.global_group_name, self.channel_name)
        await self.channel_layer.group_discard(self.user_group_name, self.channel_name)

        await self.send_active_users_update()

    async def send_active_users_update(self):
        # Retrieve active users from Redis and notify all clients
        active_users = list(get_active_users())
        active_users = [user for user in active_users if user]  # Exclude invalid usernames

        await self.channel_layer.group_send(
            self.global_group_name,
            {
                "type": "update_user_list",
                "active_users": active_users,
            }
        )

    async def update_user_list(self, event):
        await self.send(text_data=json.dumps({
            "type": "active_users",
            "active_users": event["active_users"],
        }))

    async def receive(self, text_data):
        payload = json.loads(text_data)
        event_type = payload.get("type")

        if event_type == "send_challenge":
            await self.process_challenge_request(payload)
        if event_type == "accept_challenge":
            await self.process_challenge_accept(payload)
        if event_type == "decline_challenge":
            await self.process_challenge_decline(payload)
        if event_type == "make_move":
            await self.process_move(payload)
        if event_type == "resign":
            await self.process_resignation(payload)

    async def process_challenge_request(self, data):
        opponent = data.get("opponent_username")
        if not opponent:
            return

        await self._send_to_group(
            f"user_{opponent}",
            {
                "type": "challenge_received",
                "challenger": self.current_user,
            }
        )

    async def process_challenge_accept(self, data):
        
        pass

    async def process_move(self, data):
        opponent = data.get("opponent_username")
        if not opponent:
            return

        await self._send_to_group(
            f"user_{opponent}",
            {
                "type": "move_notification",
                "challenger": self.current_user,
                "move": data.get("move"),
            }
        )

    async def process_challenge_decline(self, data):
        challenger = data.get("challenger_username")
        if not challenger:
            return

        await self._send_to_group(
            f"user_{challenger}",
            {
                "type": "challenge_rejected",
                "declined_by": self.current_user,
            }
        )

    async def process_resignation(self, data):
        opponent = data.get("opponent_username")
        if not opponent:
            return

        await self._send_to_group(
            f"user_{opponent}",
            {
                "type": "game_resignation",
                "resigned_by": self.current_user,
            }
        )

    async def challenge_received(self, event):
        await self.send(text_data=json.dumps({
            "type": "challenge_notification",
            "challenger": event["challenger"],
        }))
    
    async def _send_to_group(self, group_name, message):
        await self.channel_layer.group_send(group_name, message)
        
    async def game_resignation(self, event):
        await self.send(text_data=json.dumps({
            "type": "resign",
            "resigned_by": event["resigned_by"],
        }))


    async def move_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": "make_move",
            "move": event.get("move"),
        }))

    async def challenge_rejected(self, event):
        await self.send(text_data=json.dumps({
            "type": "challenge_declined",
            "declined_by": event["declined_by"],
        }))

    
