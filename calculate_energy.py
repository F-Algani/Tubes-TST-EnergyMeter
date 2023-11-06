from fastapi import APIRouter, HTTPException
import json
from pydantic import BaseModel
from typing import List

########################################
################# CRUD #################
########################################

def calculate_energy()