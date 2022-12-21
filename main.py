from fastapi import Depends, FastAPI, HTTPException
from router import hotels
from db import models
from db.database import engine
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "https://main.d2nlm8wd08s9mv.amplifyapp.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hotels.router)

@app.get('/')
def home():
    return "This is the entry point"

handler = Mangum(app=app)