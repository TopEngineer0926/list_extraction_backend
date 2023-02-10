from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Union, Optional
import logging
import openai
import os

load_dotenv()
app = FastAPI()
logger = logging.getLogger()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
async def root(request: Request):
    return "works"


@app.post("/api")
async def api(list_text: str):

    prompt_prepend = list_text


    #with open('test_text.txt','r') as file:
        #prompt_prepend = file.read()

    #logger.error("prompt_prepend is " + prompt_prepend)

    prompt = """
####

Here is an ordered list of the companies from the text:

1."""
    temperature = 0

    temp_data = (prompt_prepend + prompt).strip()
    temp_list = temp_data.split('\n')
    n= 1200 # word count
    # split prompt data
    split_data = [(temp_list[i:i+n]) for i in range(0, len(temp_list), n)]
    print(split_data)

    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt_prepend + prompt,
        temperature=temperature,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop="####"
    )

    response_list = response['choices'][0]['text'].strip().split("\n")
    parsed_list = [response_list[0]]

    for i, item in enumerate(response_list):
        if i == 0:
            continue
        if(len(item.split(". ")) > 1):
            parsed_list.append(item.split(". ")[1])

    return {"list": parsed_list}