from fastapi import FastAPI
from router import hello, auth

app = FastAPI()

app.include_router(hello.router)
app.include_router(auth.router)

@app.get('/')
def home():
    return "This is the entry point"