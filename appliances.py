from fastapi import APIRouter, HTTPException
import json
from pydantic import BaseModel
from typing import List
from auth import *

########################################
################# CRUD #################
########################################

class Appliances(BaseModel):	
	appliance_id: int
	appliance_name: str
	appliance_power_watt: int
	appliance_usage_in_minute: int

json_filename="appliances.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)

router = APIRouter(tags=["Appliances"])
#app = FastAPI()

@router.get('/')
async def read_all_appliances(current_user: User = Depends(get_current_active_user)):
	return data['appliances']


@router.get('/{appliance_id}')
async def read_appliance(appliance_id: int, current_user: User = Depends(get_current_active_user)):
	for appliance_item in data['appliances']:
		print(appliance_item)
		if appliance_item['appliance_id'] == appliance_id:
			return appliance_item
	raise HTTPException(
		status_code=404, detail=f'Appliance Not Found'
	)

@router.post('/')
async def add_appliance(appliance: Appliances, current_user: User = Depends(get_current_active_user)):
	if current_user.is_admin:
		appliance_dict = appliance.dict()
		appliance_found = False
		for appliance_item in data['appliances']:
			if appliance_item['appliance_id'] == appliance_dict['appliance_id']:
				appliance_found = True
				return "Appliance ID "+str(appliance_dict['appliance_id'])+" sudah tersedia."
		
		if not appliance_found:
			data['appliances'].append(appliance_dict)
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file, indent=2)

			return appliance_dict
		raise HTTPException(
			status_code=404, detail=f'Appliance Not Found'
		)
	else:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized access"
		)

@router.put('/')
async def update_appliance(appliance: Appliances, current_user: User = Depends(get_current_active_user)):
	if current_user.is_admin:
		appliance_dict = appliance.dict()
		appliance_found = False
		for appliance_idx, appliance_item in enumerate(data['appliances']):
			if appliance_item['appliance_id'] == appliance_dict['appliance_id']:
				appliance_found = True
				data['appliances'][appliance_idx] = appliance_dict
				
				with open(json_filename,"w") as write_file:
					json.dump(data, write_file, indent=2)
				return "Appliance updated"	
		
		if not appliance_found:
			return "Appliance ID not found."
		raise HTTPException(
			status_code=404, detail=f'Appliance Not Found'
		)
	else:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized access"
		)

@router.delete('/{appliance_id}')
async def delete_appliance(appliance_id: int, current_user: User = Depends(get_current_active_user)):
	if current_user.is_admin:
		appliance_found = False
		for appliance_idx, appliance_item in enumerate(data['appliances']):
			if appliance_item['appliance_id'] == appliance_id:
				appliance_found = True
				data['appliances'].pop(appliance_idx)
				
				with open(json_filename,"w") as write_file:
					json.dump(data, write_file, indent=2)
				return "Appliance updated"
		
		if not appliance_found:
			return "Appliance ID not found."
		raise HTTPException(
			status_code=404, detail=f'Appliance Not Found'
		)
	else:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized access"
		)