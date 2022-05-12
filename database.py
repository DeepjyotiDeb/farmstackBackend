from typing import Collection
from model import Todo

# mongo db driver
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
database = client.Todolist
collection = database.todo


async def fetch_one_todo(title):
    document = await collection.find_one({"title": title})
    return document


async def fetch_all_todos():
    todos = []
    cursor = collection.find({})  # finds and loads all docs in cursor
    async for document in cursor:
        # title, description can be of any number so **
        todos.append(Todo(**document))
    return todos


async def create_todo(todo):
    document = todo
    result = await collection.insert_one(document)
    return document


async def update_todo(title, desc):
    await collection.update_one({"title": title}, {"$set": {
        "description": desc}})  # choose by title and then followed by the update content
    document = await collection.find_one({"title": title})
    return document


async def delete_todo(title):
    await collection.delete_one({"title": title})
    return True
