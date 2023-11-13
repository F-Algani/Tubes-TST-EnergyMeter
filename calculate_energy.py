from fastapi import APIRouter, HTTPException
import json
from typing import List
from auth import *

json_filename="rooms.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)

router = APIRouter()

def energy_usage(power: int, time: int):
    
    default_price = 1444.70
    total_price = (power/1000)*default_price*(time/60)
    return total_price

@router.get('/{room_id}')
async def calculate_energy(room_id: int, current_user: User = Depends(get_current_active_user)):
    price = 0
    
    for room_item in data['rooms']:
        if room_item['room_id'] == room_id:
            for appliances in room_item['room_appliances']:
                price += energy_usage(appliances['appliance_power_watt'], appliances['appliance_usage_in_minute'])
            return (f"Ruangan dengan ID {room_item['room_id']} dan nama {room_item['room_name']} memiliki biaya sebesar Rp{price}")
    raise HTTPException(
		status_code=404, detail=f'Room Not Found'
	)