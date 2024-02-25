from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import HTMLResponse
import requests
import replicate
from openai import OpenAI
import matplotlib.pyplot as plt
import numpy as np
import random
from dotenv import load_dotenv
import os
import random
import json

load_dotenv()

client = OpenAI(
  organization=os.getenv("OPENAI_API"),
)

my_assistant = client.beta.assistants.retrieve("asst_N9nNHYnL43daWRkhoGXIwfJw")

app = FastAPI()
templates = Jinja2Templates(directory = 'templates')

##############################################
@app.get("/")
def home(request: Request):
    ''' Returns html jinja2 template render for home page form
    '''

    return templates.TemplateResponse('home.html', {
            "request": request,
        })

class Item(BaseModel):
    search: str

@app.post("/")
async def root(item: Item):
    thread = client.beta.threads.create()
    print(thread)