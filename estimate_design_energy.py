from fastapi import APIRouter, HTTPException
import json, requests
from pydantic import BaseModel
from typing import List
from auth import *
from calculate_energy import energy_usage

class ApplianceInstance(BaseModel):
    id: int
    appliance_power_watt: int
    appliance_usage_in_min: int

class DesainAppliances(BaseModel):
    id: int
    appliances: List[ApplianceInstance]

external_service_url = 'https://desain-psikologi-fastapi.whitecliff-184c41f4.southeastasia.azurecontainerapps.io/'

def get_token():
    token_url = external_service_url+'token'   #Sesuain sama pathnya razan
    token_response = requests.post(token_url, data = {'username': 'testacc', 'password': 'testacc1234'})
    token = token_response.json().get('access_token')
    return token

def get_desain():
    headers = {'Authorization': f'Bearer {get_token()}'}
    desain = requests.get(external_service_url+'desain', headers=headers)
    return desain.json()

print(get_desain())

with open("desain_appliances.json", "r") as read_file:
    data = json.load(read_file)

with open("appliances.json", "r") as read_file_2:
    data_appliances = json.load(read_file_2)

router = APIRouter(tags=["Estimate Design Energy"])

#koding service baru brutal
# Plan Service Baru
# 1. Generate Template/General appliances untuk jenis desain tertentu
# desainname = {minimalist, greendays, oldgarden, modern, tranquil oasis, serenity space, innovative zen}
# 2. Bisa customize (add/delete) appliances listnya
# 3. Calculate estimated energy costnya

@router.get('/{desain_id}')
async def get_estimated_energy_cost(desain_id: int, current_user: User = Depends(get_current_active_user)):
    price = 0
    desain_data = get_desain()
    print(desain_data)

    id_found = False
    for d in desain_data:
        if desain_id == d['id']:
            id_found = True
            break
    if not id_found:
        raise HTTPException(
            status_code=404, detail="Desain ID Not Found"
        )
    
    for d in desain_data:
        if desain_id == d['id']:
            found = False
            for id in data['desain_appliances']:
                if desain_id == id['id']:
                    found = True
            if not found:
                print(d['id'])
                create_default_appliances(d['id'], d['desainname'])

    for d in desain_data:
        if desain_id == d['id']:
            found = False
            for id in data['desain_appliances']:
                if desain_id == id['id'] and not found:
                    found = True
                    for appliances in id['appliances']:
                        price += energy_usage(appliances['appliance_power_watt'], appliances['appliance_usage_in_min'])
                    return (f"Desain dengan id {desain_id} memiliki kisaran biaya sebesar Rp{price}")
        # else:
        #     create_default_appliances(d['id'], d['desainname'])

    # for d in desain_data:
    #     if desain_id == d['id'] and desain_id in data['desain_appliances']['id']:
    #         for appliances in data['desain_appliances']['appliances']:
    #             price += energy_usage(appliances['appliance_power_watt'], appliances['appliance_usage_in_minute'])
    #         return (f"Desain dengan id {desain_id} memiliki kisaran biaya sebesar Rp{price}")

    return 'Error'

def create_default_appliances(desain_id: int, desain_name: str):
    des = DesainAppliances(id=desain_id, appliances=[])
    # appl = ApplianceInstance()

    if desain_name == "minimalist":
        for d in data_appliances['appliances']:
            if d['appliance_id'] in [1,2,6]:
                # appl['id'] = d['id']
                # appl['appliance_power_watt'] = d['appliance_power_watt']
                # appl['appliance_usage_in_min'] = d['appliance_usage_in_min']
                # appl.dict()
                # des['appliances'].append(appl.dict())
                appl = ApplianceInstance(
                    id=d['appliance_id'],
                    appliance_power_watt=d['appliance_power_watt'],
                    appliance_usage_in_min=120
                )
                des.appliances.append(appl)
    elif desain_name == "greendays":
        for d in data_appliances['appliances']:
            if d['appliance_id'] in [1,4,5]:
                appl = ApplianceInstance(
                    id=d['appliance_id'],
                    appliance_power_watt=d['appliance_power_watt'],
                    appliance_usage_in_min=120
                )
                des.appliances.append(appl)
    elif desain_name == "oldgarden":
        for d in data_appliances['appliances']:
            if d['appliance_id'] in [3,5,6]:
                appl = ApplianceInstance(
                    id=d['appliance_id'],
                    appliance_power_watt=d['appliance_power_watt'],
                    appliance_usage_in_min=120
                )
                des.appliances.append(appl)
    elif desain_name == "modern":
        for d in data_appliances['appliances']:
            if d['appliance_id'] in [1,2,4]:
                appl = ApplianceInstance(
                    id=d['appliance_id'],
                    appliance_power_watt=d['appliance_power_watt'],
                    appliance_usage_in_min=120
                )
                des.appliances.append(appl)
    elif desain_name == "tranquil oasis":
        for d in data_appliances['appliances']:
            if d['appliance_id'] in [2,3,5]:
                appl = ApplianceInstance(
                    id=d['appliance_id'],
                    appliance_power_watt=d['appliance_power_watt'],
                    appliance_usage_in_min=120
                )
                des.appliances.append(appl)
    elif desain_name == "serenity space":
        for d in data_appliances['appliances']:
            if d['appliance_id'] in [1,2,3]:
                appl = ApplianceInstance(
                    id=d['appliance_id'],
                    appliance_power_watt=d['appliance_power_watt'],
                    appliance_usage_in_min=120
                )
                des.appliances.append(appl)
    else:
        for d in data_appliances['appliances']:
            if d['appliance_id'] in [4,5,6]:
                appl = ApplianceInstance(
                    id=d['appliance_id'],
                    appliance_power_watt=d['appliance_power_watt'],
                    appliance_usage_in_min=120
                )
                des.appliances.append(appl)
    data['desain_appliances'].append(des.dict())

    with open("desain_appliances.json", "w") as write:
        json.dump(data, write, indent=2)

    return ("OK")

@router.post('/{desain_id}')
async def add_appliances(desain_id: int, appliance_id: int, appliance_usage: int, current_user: User = Depends(get_current_active_user)):
    # cek apakah desain_id valid dan terdapat di database layanan eksternal dan di file desain_appliances.json
    desain_found = False
    for d in data['desain_appliances']:
        if desain_id == d['id']:
            desain_found = True
            break
    if not desain_found:
        raise HTTPException(status_code=404, detail="Desain Not Found")
    
    # cek apakah appliance_id valid dan terdapat di file appliances.json
    appl_found = False
    for a in data_appliances['appliances']:
        if appliance_id == a['appliance_id']:
            appl_found = True
            break
    if not appl_found:
        raise HTTPException(status_code=404, detail="Appliance Not Found")
    
    # tambahkan appliance baru ke data di file desain_appliances.json
    for a in data_appliances['appliances']:
        if a['appliance_id'] == appliance_id:
            power = a['appliance_power_watt']

    for appl_idx, appl in enumerate(data['desain_appliances']):
        if appl['id'] == desain_id:
            for appl2 in appl['appliances']:
                if appl2['id'] == appliance_id:
                    return (f"Appliance dengan ID {appliance_id} sudah tersedia")
            inserted_appl = ApplianceInstance(
                id=appliance_id,
                appliance_power_watt=power,
                appliance_usage_in_min=appliance_usage
            )
            data['desain_appliances'][appl_idx]['appliances'].append(inserted_appl.dict())

            with open("desain_appliances.json", "w") as write:
                json.dump(data, write, indent=2)

            return (appl)

@router.delete('/{desain_id}')
async def delete_appliances(desain_id: int, appliance_id: int, current_user: User = Depends(get_current_active_user)):
    # cek apakah desain_id valid dan terdapat di database layanan eksternal dan di file desain_appliances.json
    desain_found = False
    for d in data['desain_appliances']:
        if desain_id == d['id']:
            desain_found = True
            break
    if not desain_found:
        raise HTTPException(status_code=404, detail="Desain Not Found")

    # hapus appliance dengan id yang diberikan dari data di file desain_appliances.json
    appl_found = False
    for appl_idx, appl in enumerate(data['desain_appliances']):
        if appl['id'] == desain_id:
            for appl_idx_2, appl2 in enumerate(appl['appliances']):
                if appl2['id'] == appliance_id:
                    appl_found = True
                    data['desain_appliances'][appl_idx]['appliances'].pop(appl_idx_2)

                    with open("desain_appliances.json", "w") as write:
                        json.dump(data, write, indent=2)

                    return ("Updated Successfully")
    if not appl_found:
        return "Appliance Not Found"
    raise HTTPException(
			status_code=404, detail=f'Appliance Not Found'
		)

@router.put('/{desain_id}')
async def edit_appliances_usage(desain_id: int, appliance_id: int, appliance_usage: int, current_user: User = Depends(get_current_active_user)):
    # cek apakah desain_id valid dan terdapat di database layanan eksternal dan di file desain_appliances.json
    desain_found = False
    for d in data['desain_appliances']:
        if desain_id == d['id']:
            desain_found = True
            break
    if not desain_found:
        raise HTTPException(status_code=404, detail="Desain Not Found")
    
    # cek apakah appliance_id valid dan terdapat di file appliances.json
    appl_found = False
    for a in data_appliances['appliances']:
        if appliance_id == a['appliance_id']:
            appl_found = True
            break
    if not appl_found:
        raise HTTPException(status_code=404, detail="Appliance Not Found")
    
    # ubah waktu penggunaan appliance yang ada data di file desain_appliances.json
    for appl_idx, appl in enumerate(data['desain_appliances']):
        if appl['id'] == desain_id:
            for appl_idx_2, appl2 in enumerate(appl['appliances']):
                if appl2['id'] == appliance_id:
                    # appl2['appliance_usage_in_min'] = power
                    data['desain_appliances'][appl_idx]['appliances'][appl_idx_2]['appliance_usage_in_min'] = appliance_usage
            # data['desain_appliances'][appl_idx]['appliances'].append(inserted_appl.dict())

                    with open("desain_appliances.json", "w") as write:
                        json.dump(data, write, indent=2)

                    return "Appliance Usage Time Updated"