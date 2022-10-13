from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/hello",
    tags=["hello"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get('/')
def say_hello():
    return "hello world :D"