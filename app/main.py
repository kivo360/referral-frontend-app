import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.requests import Request

from app.blueprints.users import userapi


version = f"{sys.version_info.major}.{sys.version_info.minor}"

origins = [
    "http:localhost",
    "http:localhost:8080",
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
