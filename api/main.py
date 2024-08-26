from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from databases import Database
import base64

app = FastAPI()

# Configuração da conexão com o banco de dados
DATABASE_URL = "postgresql://demoblaze_user:Q@cdias3242*&@db:5432/demoblaze"
database = Database(DATABASE_URL)

# Montando o diretório estático
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

class User(BaseModel):
    username: str
    password: str
# Defina outras rotas e lógica aqui

@app.get("/")
async def read_index():
    return FileResponse('frontend/static/index.html')

@app.post("/signup")
async def signup(request: Request):
    body = await request.json()
    username = body.get("username")
    password = body.get("password")  # Não faça a decodificação de Base64

    query = "SELECT * FROM users WHERE username = :username"
    existing_user = await database.fetch_one(query=query, values={"username": username})

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Armazene a senha diretamente (considere aplicar hash antes de armazenar)
    query = "INSERT INTO users (username, password) VALUES (:username, :password)"
    values = {"username": username, "password": password}
    await database.execute(query=query, values=values)
    return {"status": "User created successfully"}

@app.get("/users")
async def get_users():
    query = "SELECT id, username, password FROM users"
    users = await database.fetch_all(query=query)
    return [{"id": user["id"], "username": user["username"], "password": base64.b64encode(user["password"].encode()).decode()} for user in users]

@app.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    query = "DELETE FROM users WHERE id = :id"
    values = {"id": user_id}
    await database.execute(query=query, values=values)
    return {"status": f"User with id {user_id} deleted successfully"}

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/prod.html")
async def get_product_page(idp_: int):
    file_path = f"frontend/static/produtos/prod_{idp_}.html"
    return FileResponse(file_path)