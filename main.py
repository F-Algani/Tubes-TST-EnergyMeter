from fastapi import FastAPI
from appliances import router as appliances_router
from rooms import router as rooms_router
from calculate_energy import router as energy_meter_router
from auth import router as auth_router

app = FastAPI()

app.include_router(appliances_router, prefix = "/appliances")
app.include_router(rooms_router, prefix = "/rooms")
app.include_router(energy_meter_router, prefix = "/calculate-energy")
app.include_router(auth_router)

#Landing Page
@app.get('/')
async def homepage():
    return {"message": "Welcome to EnergyMeter!"}