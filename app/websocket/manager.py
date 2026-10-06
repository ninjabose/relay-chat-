from fastapi import WebSocket,HTTPException,Depends
import secrets
import string

from app.websocket.connection import ClientConnection
from app.websocket.events import IdentifyEvent,JoinResult,LeaveResult


class ConnectionManagerV3:
    def __init__(self):
        self.clients:dict[WebSocket,ClientConnection]={} #socket->client
        self.rooms:dict[str,set[ClientConnection]]={}    #room_id->set of clients

    def register(self,websocket:WebSocket,username:str):
        #basically : {websocket,username,set[user joined rooms]}
        client_connection=ClientConnection(websocket,username)

        #Load it in memory - this lad needs to be online
        self.clients[websocket]=client_connection

        return client_connection

    #DISCONNECT
    def unregister(self,websocket:WebSocket):

        #Remove him from rooms
        client_connection=self.clients[websocket]
        rooms=client_connection.rooms.copy()

        for room in rooms:
            self.rooms[room].remove(client_connection)
            if not self.rooms[room]:
                del self.rooms[room]

        self.clients[websocket].rooms.clear() #not needed auto garbage collector will delete it
        del self.clients[websocket]

    async def join_room(self,client_connection:ClientConnection,room_id:str):

        if room_id not in self.rooms:
            return JoinResult.ROOM_NOT_FOUND

        if client_connection in self.rooms[room_id] or room_id in client_connection.rooms:
            return JoinResult.ALREADY_JOINED
        #websocket=client_connection.websocket
        self.rooms[room_id].add(client_connection)
        #self.clients[websocket]=client_connection
        client_connection.rooms.add(room_id)
        
        return JoinResult.SUCCESS
        

    def create_room(self,client_connection:ClientConnection): #room_id:str->

        #Generate group id
        while True:
            alphabet=string.ascii_uppercase + string.digits
            room_id=''.join(secrets.choice(alphabet) for _ in range(6))
            if room_id not in self.rooms:
                self.rooms[room_id]={client_connection}
                break
        client_connection.rooms.add(room_id)
        return room_id

    def leave_room(self,client_connection:ClientConnection,room_id:str):

        if room_id not in self.rooms:
            return LeaveResult.ROOM_NOT_FOUND

        if room_id not in client_connection.rooms or client_connection not in self.rooms[room_id]:
            return LeaveResult.NOT_A_MEMBER

        self.rooms[room_id].remove(client_connection)
        client_connection.rooms.remove(room_id)

        #Delete room if lust guy leaves
        if not self.rooms[room_id]:
            del self.rooms[room_id]


        return LeaveResult.SUCCESS

    async def broadcast_room(self,client_connection:ClientConnection,payload:dict):

        group_id=payload['group_id']

        if group_id not in self.rooms or client_connection not in self.rooms[group_id]:
            return

        if group_id not in client_connection.rooms:
            return

        room=self.rooms[group_id]

        for recipient in room:
            webskt=recipient.websocket
            await webskt.send_json({
                'from':client_connection.username,
                'type':payload['type'],
                'room_id':group_id,
                'content':payload['message']
            })

        return



        









        

        









    
    

    
    

'''class ConnectionManager:

    def __init__(self):
        self.connections: list[WebSocket]=[]
        self.rooms={}

    async def connect(self,websocket:WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def join_room(self,room_id:str,websocket:WebSocket):
        if room_id not in self.rooms:
            self.rooms[room_id]=[]
        self.rooms[room_id].append(websocket)

    def disconnect(self,websocket:WebSocket):
        self.connections.remove(websocket)

    async def broadcast(self,message:str):
        for websocket in self.connections:
            await websocket.send_text(message)

    async def broadcast_room(self,room_id:str,message:str,websocket:WebSocket):

        if not self.rooms.get(room_id) or websocket not in self.rooms.get('room_id'): 
            raise HTTPException(status_code=403, detail='Forbidden')

        for webskt in self.rooms[room_id]:
            await webskt.send_text(message)

    async def leave_room(self,room_id:str,websocket:WebSocket):

        if room_id not in self.rooms or websocket not in self.rooms[room_id]:
            raise HTTPException(status_code=403, detail='Forbidden')

        self.rooms[room_id].remove(websocket)

        if len(self.rooms[room_id])==0:
            del self.rooms[room_id]
'''

'''class ConnectionManager2:

    def __init__(self):
        self.rooms = {}
        self.client_rooms={}

    async def join_room(self, room_id: str, websocket: WebSocket):
        if room_id not in self.rooms:
            self.rooms[room_id] = []

        if websocket in self.rooms[room_id]:
            return
        
        if websocket not in self.client_rooms:
            self.client_rooms[websocket]=set()

        self.rooms[room_id].append(websocket)
        self.client_rooms[websocket].add(room_id)

    async def leave_room(self, room_id: str, websocket: WebSocket):
        if websocket not in self.client_rooms or room_id not in self.client_rooms[websocket]:
            return
        if room_id not in self.rooms:
            return

        self.rooms[room_id].remove(websocket)
        self.client_rooms[websocket].remove(room_id)

        if not self.rooms[room_id]:
            del self.rooms[room_id]
        if not self.client_rooms[websocket]:
            del self.client_rooms[websocket]

    async def broadcast_room(self, room_id: str, message: str):

        for websocket in self.rooms.get(room_id, []):
            await websocket.send_text(message)

    async def disconnect(self,websocket):
        if websocket not in self.client_rooms:
            return
        rooms=self.client_rooms[websocket].copy()
        for room in rooms:
            self.leave_room(self,room,websocket)
        #del self.client_rooms[websocket]
        


'''