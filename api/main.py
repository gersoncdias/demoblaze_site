from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware  # Importando o CORSMiddleware
from pydantic import BaseModel
from databases import Database
from typing import List
import base64

app = FastAPI()

# Configuração da conexão com o banco de dados
DATABASE_URL = "postgresql://demoblaze_user:Q@cdias3242*&@db:5432/demoblaze"
database = Database(DATABASE_URL)

# Montando o diretório estático
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitindo todas as origens, ajuste conforme necessário
    allow_credentials=True,
    allow_methods=["*"],  # Permitindo todos os métodos
    allow_headers=["*"],  # Permitindo todos os headers
)

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
    password = body.get("password")  # Senha recebida diretamente sem codificação

    query = "SELECT * FROM users WHERE username = :username"
    existing_user = await database.fetch_one(query=query, values={"username": username})

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Armazene a senha diretamente
    query = "INSERT INTO users (username, password) VALUES (:username, :password)"
    values = {"username": username, "password": password}
    await database.execute(query=query, values=values)
    return {"status": "User created successfully"}


@app.post("/login")
async def login(user: User, response: Response):
    query = "SELECT * FROM users WHERE username = :username AND password = :password"
    values = {"username": user.username, "password": user.password}  # Comparação direta
    existing_user = await database.fetch_one(query=query, values=values)

    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Gerar o token de autenticação
    auth_token = base64.b64encode(f"{user.username} {user.password}".encode("utf-8")).decode("utf-8")

    # Setar o token nos cookies
    response.set_cookie(key="tokenp_", value=auth_token)

    return {"Auth_token": auth_token}


@app.get("/users")
async def get_users():
    query = "SELECT id, username, password FROM users"
    users = await database.fetch_all(query=query)
    return [{"id": user["id"], "username": user["username"], "password": base64.b64encode(user["password"].encode()).decode()} for user in users]

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = "DELETE FROM users WHERE id = :id"
    values = {"id": user_id}
    await database.execute(query=query, values=values)
    return {"status": f"User with id {user_id} deleted successfully"}

# Modelo para receber a lista de IDs
class DeleteUsersRequest(BaseModel):
    ids: List[int]

@app.delete("/delete_users")
async def delete_users(request: DeleteUsersRequest):
    query = "DELETE FROM users WHERE id = ANY(:ids)"
    values = {"ids": request.ids}
    result = await database.execute(query=query, values=values)
    
    return {"status": f"{len(request.ids)} users deleted successfully"}

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
