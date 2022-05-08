from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model import Todo
import database

app = FastAPI()
origins = ['http://127.0.0.1:3000', 'http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/")
def read_root():
    return { "ping": "pong"}

@app.get("/api/todo")
async def get_todo():
    response = await database.fetch_all_todos()
    return response

@app.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_id(title):
    response = await database.fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"there is no todo with that title {title}")

@app.post("/api/todo", response_model=Todo)
async def post_todo(todo:Todo): #input todo would be json, convert it to dict
    response = await database.create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "something went wrong")

@app.put("/api/todo/{title}", response_model=Todo)
async def put_todo(title:str, desc:str):
    response = await database.update_todo(title, desc)
    if response:
        return response
    raise HTTPException(404, f"no todo with title {title}")

@app.delete("/api/todo/{title}")
async def delete_todo(title):
    response = await database.delete_todo(title)
    if response:
        return  (f"successfully deleted item {title}", response, title)
    raise HTTPException(404, f"no todo witht title {title}")