from fastapi import APIRouter,WebSocket,WebSocketDisconnect,Depends


#from app.websocket.events.events import IdentifyEvent,ClientEvents,Event,ServerEvent,ServerResponse,JoinResult,LeaveResult
from app.websocket.events.client import InClientIdentifyEvent,InClientCommEvent,ClientEventType
from app.websocket.events.server import ServerEventType,OutMessageEvent,OutRoomCreatedEvent,OutRoomJoinedEvent,OutRoomLeftEvent,JoinResult,LeaveResult,ErrorEvent


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
        username_input=InClientIdentifyEvent.model_validate(username_data)
        #register client
        client_connection= manager.register(websocket,username_input.username)

        
        while True:
            data = await websocket.receive_json()
            client_data= InClientCommEvent.model_validate(data)

            #create room
            if client_data.event_type == ClientEventType.CREATE_ROOM:
                room_id= await manager.create_room(client_connection)

                response=OutRoomCreatedEvent(
                    event_type=ServerEventType.ROOM_CREATED,
                    room_id=room_id
                    )
                await websocket.send_json(response.model_dump())

            #join room
            elif client_data.event_type==ClientEventType.JOIN_ROOM:
                 result=manager.join_room(client_connection,client_data.room_id)

                 if result == JoinResult.SUCCESS:

                    response=OutRoomJoinedEvent(
                        username=client_connection.username,
                        room_id=client_data.room_id
                    )
                    await manager.broadcast_room(client_connection,response.model_dump())


                 elif result==JoinResult.ALREADY_JOINED:
                    response=ErrorEvent(
                        message='Room already joined!'
                    )
                    await websocket.send_json(response.model_dump())


                 elif result==JoinResult.ROOM_NOT_FOUND:
                     response=ErrorEvent(
                        message='Room does not exist or deleted!'
                    )
                     await websocket.send_json(response.model_dump())

            #leave room 
            elif client_data.event_type==ClientEventType.LEAVE_ROOM:
                 result=manager.leave_room(client_connection,client_data.room_id)

                 if result== LeaveResult.SUCCESS:

                    response=OutRoomLeftEvent(
                        username=client_connection.username,
                        room_id=client_data.room_id
                    )

                    payload=response.model_dump()
                    #broadcast leave event - client won't get it because he left
                    await manager.broadcast_room(client_connection,payload,False)

                 elif result==LeaveResult.NOT_A_MEMBER:
                    response=ErrorEvent(
                        message='Not a member of the room you are trying to leave'
                    )
                 elif result==LeaveResult.ROOM_NOT_FOUND:
                     response=ErrorEvent(
                        message='Room does not exist!'
                    )
                 await websocket.send_json(response.model_dump())


            #message
            elif client_data.event_type==ClientEventType.MESSAGE:  
                payload=OutMessageEvent(
                    username=client_connection.username,
                    room_id=client_data.room_id,
                    message=client_data.message
                )
                await manager.broadcast_room(client_connection,payload.model_dump())

    except WebSocketDisconnect:
        manager.unregister(websocket)