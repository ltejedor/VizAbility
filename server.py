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
    # Include fields for the data you expect, e.g., background, takeaways
    # For file uploads, you'll handle them separately with UploadFile
    background: str
    takeaways: str

@app.post("/")  # Change this line to match the fetch request
async def upload_csv():
    # Your processing logic here
    thread = client.beta.threads.create()
    print(thread)