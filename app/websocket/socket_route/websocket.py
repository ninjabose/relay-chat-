from fastapi import APIRouter,WebSocket,WebSocketDisconnect,Depends


from app.websocket.events import IdentifyEvent,ClientEvents,Event,ServerEvent,ServerResponse
from app.websocket.manager import ConnectionManagerV3 as manager


router =APIRouter()

@router.websocket('/')
async def group_chat(websocket:WebSocket):

    await websocket.accept()
    #identify handshake

    try:
        #username receive
        username_data= await websocket.receive_json()
        #validation
        username_input=IdentifyEvent.model_validate(username_data)
        #register client
        client_connection= manager.register(websocket,username_input.username)

        
        while True:
            data = await websocket.receive_json()
            client_data= ClientEvents.model_validate(data)

            #create room
            if client_data.event_type == Event.CREATE_ROOM:
                group_id= await manager.create_room(client_connection)

                response=ServerResponse(
                    event_type=ServerEvent.ROOM_CREATED,
                    group_id=group_id
                    )
                await websocket.send_json(response.model_dump())

            #join room
            elif client_data.event_type==Event.JOIN_ROOM:
                 manager.join_room(client_connection,client_data.group_id)
                 response=ServerResponse(
                     event_type=ServerEvent.ROOM_JOINED,
                     group_id=client_data.group_id
                 )
                 await websocket.send_json(response.model_dump())

            #leave room 
            elif client_data.event_type==Event.LEAVE_ROOM:
                 manager.leave_room(client_connection,client_data.group_id)
                 response=ServerResponse(
                     event_type=ServerEvent.ROOM_LEFT,
                     group_id=client_data.group_id
                 )
                 await websocket.send_json(response.model_dump())

            #message
            elif client_data.event_type==Event.MESSAGE:
                
                response=ServerResponse(
                    event_type=ServerEvent.MESSAGE,
                    group_id=client_data.group_id,
                    message=client_data.message

                )

                await manager.broadcast_room(client_connection,response.model_dump())

            
    except WebSocketDisconnect:
        manager.unregister(websocket)