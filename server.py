from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import HTMLResponse
import requests
import replicate

import matplotlib.pyplot as plt
import numpy as np
import random

import random
import json

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
