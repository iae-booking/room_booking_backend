from fastapi import Depends, FastAPI, HTTPException
from router import hello, auth, hotels
from db import models
from db.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(hello.router)
app.include_router(auth.router)
app.include_router(hotels.router)

@app.get('/')
def home():
    return "This is the entry point"