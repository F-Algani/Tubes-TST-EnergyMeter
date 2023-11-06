from fastapi import APIRouter, HTTPException
import json
from pydantic import BaseModel
from typing import List

########################################
################# CRUD #################
########################################

class Appliances(BaseModel):	#ubah isinya
	appliance_id: int
	appliance_name: str
	appliance_power_watt: int

json_filename="appliances.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)

router = APIRouter()
#app = FastAPI()

@router.get('/')
async def read_all_appliances():
	return data['appliances']


@router.get('/{appliance_id}')
async def read_appliance(appliance_id: int):
	for appliance_item in data['appliances']:
		print(appliance_item)
		if appliance_item['appliance_id'] == appliance_id:
			return appliance_item
	raise HTTPException(
		status_code=404, detail=f'Appliance Not Found'
	)

@router.post('/')
async def add_appliance(appliance: Appliances):
	appliance_dict = appliance.dict()
	appliance_found = False
	for appliance_item in data['appliances']:
		if appliance_item['appliance_id'] == appliance_dict['appliance_id']:
			appliance_found = True
			return "Appliance ID "+str(appliance_dict['appliance_id'])+" exists." #ubah jadi fungsi nambah store & bukunya
	
	if not appliance_found:
		data['appliances'].append(appliance_dict)
		with open(json_filename,"w") as write_file:
			json.dump(data, write_file)

		return appliance_dict
	raise HTTPException(
		status_code=404, detail=f'Appliance Not Found'
	)

@router.put('/')
async def update_appliance(appliance: Appliances):
	appliance_dict = appliance.dict()
	appliance_found = False
	for appliance_idx, appliance_item in enumerate(data['appliances']):
		if appliance_item['appliance_id'] == appliance_dict['appliance_id']:
			appliance_found = True
			data['appliances'][appliance_idx] = appliance_dict
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "Appliance updated"	#ubah jadi fungsi ganti bukunya
	
	if not appliance_found:
		return "Appliance ID not found."
	raise HTTPException(
		status_code=404, detail=f'Store not found'
	)

@router.delete('/{appliance_id}')
async def delete_appliance(appliance_id: int):

	appliance_found = False
	for appliance_idx, appliance_item in enumerate(data['appliances']):
		if appliance_item['appliance_id'] == appliance_id:
			appliance_found = True
			data['appliances'].pop(appliance_idx)
			
			with open(json_filename,"w") as write_file:
				json.dump(data, write_file)
			return "Appliance updated"
	
	if not appliance_found:
		return "Appliance ID not found."
	raise HTTPException(
		status_code=404, detail=f'Appliance not found'
	)