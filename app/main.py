from fastapi import FastAPI


from app.websocket.socket_route.websocket import router as chat_main_router

app = FastAPI()
app.include_router(chat_main_router)






'''
@app.websocket("/echo")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(message)
    except WebSocketDisconnect:
        print('client disconnected')


@app.websocket('/global')
async def global_chat(websocket:WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            message= await websocket.receive_text()
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
'''


'''@app.websocket('/group')
async def group_chat(websocket:WebSocket):
    await websocket.accept()
    try:
        while True:
            data= await websocket.receive_json()
            event_type=data['type']

            if event_type=='join_room':
                await manager.join_room(data['target'],websocket)
            elif event_type=='leave_room':
                #due check if room exist or present in room
                await manager.leave_room(data['target'],websocket)
            elif event_type=='message':
                if data['target'] not in manager.rooms or websocket not in manager.rooms[data['target']]:
                    continue
                await manager.broadcast_room(data['target'],data['content'])
    except WebSocketDisconnect:
        await manager.disconnect(websocket)'''
       


'''
ConnectionManager

│
├── rooms
│     │
│     ├── room_a → [WS1, WS2, WS3]
│     ├── room_b → [WS1, WS4]
│     └── room_c → [WS1, WS5]
│
└── connection_rooms
      │
      ├── WS1 → {room_a, room_b, room_c}
      ├── WS2 → {room_a}
      ├── WS3 → {room_a}
      ├── WS4 → {room_b}
      └── WS5 → {room_c}
'''




