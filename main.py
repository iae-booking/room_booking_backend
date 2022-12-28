from fastapi import Depends, FastAPI, HTTPException
from router import hello, auth, hotels, member, room
from db import models
from db.database import engine
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI() #root_path="/test/")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(hello.router)
app.include_router(auth.router)
app.include_router(hotels.router)
app.include_router(member.router)
app.include_router(room.router)

@app.get('/')
def home():
    return "This is the entry point"

handler = Mangum(app=app)
