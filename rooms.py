from fastapi import APIRouter, HTTPException
import json
from pydantic import BaseModel
from typing import List
from appliances import Appliances
from auth import *

########################################
################# CRUD #################
########################################

class Room(BaseModel):	
	room_id: int
	room_name: str
	room_appliances: List[Appliances]

json_filename="rooms.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)

router = APIRouter()

@router.get('/')
async def read_all_rooms(current_user: User = Depends(get_current_active_user)):
	return data['rooms']


@router.get('/{room_id}')
async def read_room(room_id: int, current_user: User = Depends(get_current_active_user)):
	for room_item in data['rooms']:
		print(room_item)
		if room_item['room_id'] == room_id:
			return room_item
	raise HTTPException(
		status_code=404, detail=f'Room Not Found'
	)

@router.post('/')
async def add_room(room: Room, current_user: User = Depends(get_current_active_user)):
	if current_user.is_admin:
		room_dict = room.dict()
		room_found = False
		for room_item in data['rooms']:
			if room_item['room_id'] == room_dict['room_id']:
				room_found = True
				return "Room ID "+str(room_dict['room_id'])+" sudah tersedia." 
		
		if not room_found:
			data['rooms'].append(room_dict)
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file, indent=3)

			return room_dict
		raise HTTPException(
			status_code=404, detail=f'Room Not Found'
		)
	else:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized access"
		)

@router.put('/')
async def update_room(room: Room, current_user: User = Depends(get_current_active_user)):
	if current_user.is_admin:
		room_dict = room.dict()
		room_found = False
		for room_idx, room_item in enumerate(data['rooms']):
			if room_item['room_id'] == room_dict['room_id']:
				room_found = True
				data['rooms'][room_idx] = room_dict
				
				with open(json_filename,"w") as write_file:
					json.dump(data, write_file, indent=3)
				return "Room updated"	
		
		if not room_found:
			return "Room ID not found."
		raise HTTPException(
			status_code=404, detail=f'Room Not Found'
		)
	else:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized access"
		)

@router.delete('/{room_id}')
async def delete_room(room_id: int, current_user: User = Depends(get_current_active_user)):
	if current_user.is_admin:
		room_found = False
		for room_idx, room_item in enumerate(data['rooms']):
			if room_item['room_id'] == room_id:
				room_found = True
				data['rooms'].pop(room_idx)
				
				with open(json_filename,"w") as write_file:
					json.dump(data, write_file, indent=3)
				return "Room updated"
		
		if not room_found:
			return "Room ID not found."
		raise HTTPException(
			status_code=404, detail=f'Room Not Found'
		)
	else:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized access"
		)