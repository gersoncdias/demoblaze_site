from fastapi import FastAPI
from databases import Database

app = FastAPI()

DATABASE_URL = "postgresql://demoblaze_user:Q@cdias3242*&@db:5432/demoblaze"
database = Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}
