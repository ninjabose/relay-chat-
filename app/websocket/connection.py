from fastapi import WebSocket

class ClientConnection:
    def __init__(self,websocket:WebSocket,username:str):
        self.websocket=websocket
        self.username=username
        self.rooms:set[str]=set()  #set will contain str

