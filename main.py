from fastapi import FastAPI
from router import hello

app = FastAPI()

app.include_router(hello.router)

@app.get('/')
def home():
    return "This is the entry point"