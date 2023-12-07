from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from appliances import router as appliances_router
from rooms import router as rooms_router
from calculate_energy import router as energy_meter_router
from estimate_design_energy import router as estimate_design_energy_router
from auth import router as auth_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(appliances_router, prefix = "/appliances")
app.include_router(rooms_router, prefix = "/rooms")
app.include_router(energy_meter_router, prefix = "/calculate-energy")
app.include_router(estimate_design_energy_router, prefix="/estimate-energy-cost")
app.include_router(auth_router)

#Landing Page
@app.get('/')
async def homepage():
    return {"message": "Welcome to EnergyMeter!"}