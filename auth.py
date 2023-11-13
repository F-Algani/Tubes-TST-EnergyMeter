from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import json

### AUTHENTICATION ###
SECRET_KEY = "a480d00caa342eda9658e7d8c06af8e7dbff94944c34c640f4a08bca26f48088"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

# pass untuk username dibawah: gani1234
# db = {
#     "algani": {
#         "user_id": 1,
#         "username": "algani",
#         "full_name": "farhan algani",
#         "email": "algani@test.com",
#         "hashed_password": "$2b$12$HB0kudOyf.dP3c5pvYXOp.XMselAEEFQNFp1rA/S2GMEZ.PHklJO.",
#         "disabled": False
#     }
# }

json_filename="users.json"

with open(json_filename,"r") as read_file:
	data = json.load(read_file)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str or None = None

class User(BaseModel):
    user_id: int
    username: str
    email: str or None = None
    full_name: str or None = None
    disabled: bool or None = None

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(dict: dict, username: str):
    for usernames in dict:
        if username == usernames['username']:
            user_data = usernames
            return UserInDB(**user_data)
    
def authenticate_user(dict: dict, username: str, password: str):
    user = get_user(dict, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=10)
    
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    
    user = get_user(data['users'], username=token_data.username)
    if user is None:
        raise credential_exception
    
    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(data['users'], form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register(user: User, password: str):
    user_dict = user.dict()
    user_found = False
    for users in data['users']:
        if users['username'] == user_dict['username']:
            user_found = True
            return "Username "+str(user_dict['username'])+" sudah tersedia."
        if users['user_id'] == user_dict['user_id']:
            user_found = True
            return "User ID "+str(user_dict['user_id'])+" sudah tersedia."
	
    if not user_found:
        new_input = {
            "user_id": user.user_id,
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "hashed_password": get_password_hash(password),
            "disabled": user.disabled
        }
        
        data['users'].append(new_input)
        with open(json_filename,"w") as write_file:
            json.dump(data, write_file, indent=3)
        return user_dict