from fastapi import Depends, FastAPI, HTTPException
from router import hello, auth, hotels
from db import models
from db.database import engine
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["x-apigateway-header", "Content-Type", "X-Amz-Date"],
)


app.include_router(hello.router)
app.include_router(auth.router)
app.include_router(hotels.router)

@app.get('/')
def home():
    return "This is the entry point"

handler = Mangum(app=app, spec_version=2)
