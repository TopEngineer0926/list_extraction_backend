from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Union, Optional
from asgiref.sync import sync_to_async
import openai_async
import asyncio
import logging
import openai
import os

load_dotenv()
app = FastAPI()
logger = logging.getLogger()

openai.api_key = os.getenv("OPENAI_API_KEY")
key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def root(request: Request):
    return "works"


@app.post("/api")
def api(list_text: str):

    prompt_prepend = list_text


    #with open('test_text.txt','r') as file:
        #prompt_prepend = file.read()

    #logger.error("prompt_prepend is " + prompt_prepend)

    prompt = """
####

Here is an ordered list of the companies from the text:

1."""
    temperature = 0

    temp_data = prompt_prepend.strip()
    temp_list = temp_data.split('\n')
    n= 150 # word count
    # split prompt data
    split_data = [(temp_list[i:i+n]) for i in range(0, len(temp_list), n)]

    total_response_list = []
    
    async def task_coro(item):
        # report a message
        print(f'>task {item} executing \n')
        response = await openai_async.complete(
            key,
            timeout=10,
            payload={
                "model": "code-davinci-002",
                "prompt": "".join(item) + prompt,
                "temperature": temperature,
                'stop':"####"
            },
        )
        b_in_dict =  "error" in response.json()
        if("error" in response.json()):
            print(response.json()["error"])
        else:
            response_list = response.json()["choices"][0]["text"].strip().split("\n")
            print(response_list)
            for i, item in enumerate(response_list):
                if(len(item.split(". ")) > 1):
                    total_response_list.append(item.split(". ")[1])
                else:
                    total_response_list.append(item)
        print ('task end')
 
    # coroutine used for the entry point
    async def main():
        # report a message
        print('main starting')
        # create many coroutines
        coros = [task_coro(item) for i, item in enumerate(split_data)]
        # run the tasks
        await asyncio.gather(*coros)
        # report a message
        print('main done') 
    asyncio.run(main())

    # response_list = response['choices'][0]['text'].strip().split("\n")
    # parsed_list = [response_list[0]]

    # for i, item in enumerate(response_list):
    #     if i == 0:
    #         continue
    #     if(len(item.split(". ")) > 1):
    #         parsed_list.append(item.split(". ")[1])

    return {"list": total_response_list}