from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from databases import Database
import base64

app = FastAPI()

# Configuração da conexão com o banco de dados
DATABASE_URL = "postgresql://demoblaze_user:Q@cdias3242*&@db:5432/demoblaze"
database = Database(DATABASE_URL)

app.mount("/", StaticFiles(directory="static", html=True), name="static")

DATABASE_URL = "postgresql://demoblaze_user:Q@cdias3242*&@db:5432/demoblaze"
database = Database(DATABASE_URL)

class User(BaseModel):
    username: str
    password: str

@app.post("/signup")
async def signup(request: Request):
    body = await request.json()
    username = body.get("username")
    encoded_password = body.get("password")

    try:
        password = base64.b64decode(encoded_password).decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error decoding password: " + str(e))

    query = "SELECT * FROM users WHERE username = :username"
    existing_user = await database.fetch_one(query=query, values={"username": username})

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    query = "INSERT INTO users (username, password) VALUES (:username, :password)"
    values = {"username": username, "password": password}
    await database.execute(query=query, values=values)
    return {"status": "User created successfully"}

@app.get("/users")
async def get_users():
    query = "SELECT username, password FROM users"
    users = await database.fetch_all(query=query)
    return [{"username": user["username"], "password": base64.b64encode(user["password"].encode()).decode()} for user in users]

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
