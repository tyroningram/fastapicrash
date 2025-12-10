# Import necessary modules
from enum import IntEnum
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from routers import inventory

# Create a FastAPI application instance
app = FastAPI()

# Define an enumeration for health points
class HealthPoints(IntEnum):
    LOW = 150
    MEDIUM = 250
    HIGH = 400

# Define base model for user data
class UserBase(BaseModel):
    first_name: str = Field(..., min_length=3, description="First name of user")
    last_name: str = Field(..., min_length=3, description="Last name of user")
    role: str = Field(..., min_length=3, description="Game role of user")
    healthpoints: Optional[HealthPoints] = Field(default=HealthPoints.MEDIUM, description="Set health points of role")

# Define model for creating a new user
class UserCreate(UserBase):
    pass

# Define model for user with ID
class User(UserBase):
    user_id: int = Field(..., description="Unique identifier of user")

# Define model for updating user information
class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=3, description="First name of user")
    last_name: Optional[str] = Field(None, min_length=3, description="Last name of user")
    role: Optional[str] = Field(None, min_length=3, description="Game role of user")
    healthpoints: Optional[HealthPoints] = Field(None, description="Set health points of role")

# Create a list of test users
test_user = [
    User(user_id=1, first_name="Sammy", last_name="Freeman", role="bard", healthpoints=HealthPoints.MEDIUM),
    User(user_id=2, first_name="Thomas", last_name="Singh", role="warrior", healthpoints=HealthPoints.HIGH),
    User(user_id=3, first_name="Kevin", last_name="Muhammed", role="fighter", healthpoints=HealthPoints.HIGH),
    User(user_id=4, first_name="Tessa", last_name="Williams", role="monk", healthpoints=HealthPoints.MEDIUM),
    User(user_id=5, first_name="Sarah", last_name="Ming", role="paladin", healthpoints=HealthPoints.HIGH),
    User(user_id=6, first_name="Dean", last_name="The Great", role="nurse", healthpoints=HealthPoints.LOW),
    User(user_id=7, first_name="Chester", last_name="Nutt", role="fighter", healthpoints=HealthPoints.HIGH),
]

app.include_router(inventory.router)

# Define route to get a user by ID
@app.get('/user/{user_id}', response_model=User)
async def get_user(user_id: int):
    for user in test_user:
        if user.user_id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found.")

# Define route to get all users or filter by role
@app.get('/user', response_model=List[User])
async def get_user(role: str = None):
    if role is None:
        return test_user
    
    users = [user for user in test_user if user.role == role]
    return users

# Define route to create a new user
@app.post('/user', response_model=User)
async def create_user(user: UserCreate):
    new_user_id = max(user.user_id for user in test_user) + 1
    new_user = User(user_id = new_user_id, **user.model_dump())
    test_user.append(new_user)
    return new_user

# Define route to update a user
@app.put('/user/{user_id}', response_model=User)
async def update_user(user_id: int, updated_user: UserUpdate):
    for user in test_user:
        if user.user_id == user_id:
            user.first_name = updated_user.first_name or user.first_name
            user.last_name = updated_user.last_name or user.last_name
            user.role = updated_user.role or user.role
            user.healthpoints = updated_user.healthpoints or user.healthpoints
            return user
    raise HTTPException(status_code=404, detail="User not found.")

# Define route to delete a user
@app.delete('/user/{user_id}', response_model=User)
async def delete_user(user_id: int):
    for index, user in enumerate(test_user):
        if user.user_id == user_id:
            deleted_user = test_user.pop(index)
            return deleted_user
    raise HTTPException(status_code=404, detail="User not found.")
