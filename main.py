from fastapi import FastAPI
from appliances import router as appliances_router
from rooms import router as rooms_router

app = FastAPI()

app.include_router(appliances_router, prefix = "/appliances")
app.include_router(rooms_router, prefix = "/rooms")