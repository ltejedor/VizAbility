from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
# from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse

import requests
import replicate
from openai import OpenAI
import random
from dotenv import load_dotenv
import os
import random
import json
import logging
import time

load_dotenv()

client = OpenAI(
  organization=os.environ.get("OPENAI_API"),
)

app = FastAPI()
templates = Jinja2Templates(directory = 'templates')

# ###################
file_path = "budgets.json"

def upload_file(file_path):
     # Upload a file with an "assistants" purpose
        file_to_upload = client.files.create(
             file=open(file_path, "rb"),
             purpose='assistants'
             )
        return file_to_upload

assist_id = "asst_N9nNHYnL43daWRkhoGXIwfJw"

##############################################
@app.get("/")
def home(request: Request):
    ''' Returns html jinja2 template render for home page form
    '''

    return templates.TemplateResponse('home.html', {
            "request": request,
        })

# class Item(BaseModel):
#     # Include fields for the data you expect, e.g., background, takeaways
#     # For file uploads, you'll handle them separately with UploadFile
#     background: str
#     takeaways: str

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """

    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    i=0
    while True and i < 100:
        i+=1
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                return response
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)


@app.post("/")  # Change this line to match the fetch request
# async def upload_csv():
#     thread = client.beta.threads.create()
#     print(thread)

async def upload_csv(request: Request, project_background: str = Form(...), project_takeaways: str = Form(...), csv_file: UploadFile = File(...)):  

    ''' Handles the form submission and processes the data
    '''

    form_data = await request.form()
    project_background = form_data['project_background']
    project_takeaways = form_data['project_takeaways']
    # csv_file = form_data['csv_file']

    uploaded_file = upload_file(file_path)

    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id, 
        content=project_background,
        role="user",
        file_ids=[uploaded_file.id]
    )

    # === Run our Assistant ===
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assist_id,
        instructions="code 3 visualizations based on the data and return the SVG code to render them",
    )

    # === Run ===
    response = wait_for_run_completion(client=client, thread_id=thread.id, run_id=run.id)
    # return None
    return JSONResponse(content={"message": response})

