from fastapi import APIRouter,WebSocket,WebSocketDisconnect,Depends


from app.websocket.events import IdentifyEvent,ClientEvents,Event,ServerEvent,ServerResponse,JoinResult,LeaveResult
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
                 result=manager.join_room(client_connection,client_data.group_id)

                 if result == JoinResult.SUCCESS:
                    response=ServerResponse(
                        event_type=ServerEvent.ROOM_JOINED,
                        group_id=client_data.group_id,
                        join_result=result

                    )
                    payload={
                        'group_id':client_data.group_id,
                        'type':'event',
                        'message':'joined room'
                    }
                    await manager.broadcast_room(client_connection,payload)
                 elif result==JoinResult.ALREADY_JOINED:
                    response=ServerResponse(
                        event_type=ServerEvent.ERROR,
                        group_id=client_data.group_id,
                        result=result
                    )
                    await websocket.send_json(response.model_dump())
                 elif result==JoinResult.ROOM_NOT_FOUND:
                     response=ServerResponse(
                        event_type=ServerEvent.ERROR,
                        group_id=client_data.group_id,
                        result=result
                    )
                     await websocket.send_json(response.model_dump())

            #leave room 
            elif client_data.event_type==Event.LEAVE_ROOM:
                 result=manager.leave_room(client_connection,client_data.group_id)

                 if result== LeaveResult.SUCCESS:
                    response=ServerResponse(
                        leave_result=result,
                        event_type=ServerEvent.ROOM_LEFT,
                        group_id=client_data.group_id
                    )

                    payload={
                        'group_id':client_data.group_id,
                        'type':'event',
                        'message':'left_room'
                    }
                    #broadcast leave event - client won't get it because he left
                    await manager.broadcast_room(client_connection,payload)
                 elif result==LeaveResult.NOT_A_MEMBER:
                    response=ServerResponse(
                        leave_result=result,
                        event_type=ServerEvent.ROOM_LEFT,
                        group_id=client_data.group_id
                    )
                 elif result==LeaveResult.ROOM_NOT_FOUND:
                     response=ServerResponse(
                        leave_result=result,
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