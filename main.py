from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# 仮データベース（インメモリ辞書）
fake_db: Dict[int, dict] = {}
current_id = 1

class User(BaseModel):
    name: str
    age: int
    email: str

# Create
@app.post("/users")
def create_user(user: User):
    global current_id
    fake_db[current_id] = user.dict()
    response = {"id": current_id, **user.dict()}
    current_id += 1
    return response

# Read
@app.get("/users/{user_id}")
def read_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, **fake_db[user_id]}

# Update
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    fake_db[user_id] = user.dict()
    return {"id": user_id, **user.dict()}

# Delete
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    # del fake_db[user_id]
    return {"message": "User deleted"}
