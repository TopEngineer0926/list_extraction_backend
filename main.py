from fastapi import FastAPI, HTTPException, Depends, Body
from pydantic import BaseModel
from database import SessionLocal, engine
from dotenv import load_dotenv
import openai_async
import asyncio
import logging
import openai
import os
from schema import DataList
import crud, models

class Item(BaseModel):
    title: str
    list_text: str

models.Base.metadata.create_all(bind=engine)

load_dotenv()
app = FastAPI()
logger = logging.getLogger()

openai.api_key = os.getenv("OPENAI_API_KEY")
key = os.getenv("OPENAI_API_KEY")

def db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.post('/api/list_text')
def api(item: Item = Body(), db=Depends(db)):

    title = item.title
    list_text = item.list_text
    prompt_prepend = list_text
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
    prompt_response = {}
    
    async def task_coro(item):
        # report a message
        # print(f'>task {item} executing \n')
        print("".join(item) + prompt)
        temp_prompt = "".join(item) + prompt
        response = await openai_async.complete(
            key,
            timeout=50,
            payload={
                "model": "code-davinci-002",
                "prompt": temp_prompt,
                "temperature": temperature,
                "top_p":1,
                "frequency_penalty":0,
                "presence_penalty":0,
                'stop':"####"
            },
        )
        if("error" in response.json()):
            print(response.json()["error"])
        else:
            response_list =  response.json()["choices"][0]["text"].translate({ord('\t'):None}).split('\n')
            prompt_response[temp_prompt] = response_list
            total_response_list.append(response_list[0])
            print(response_list)
            for i, item in enumerate(response_list):
                print(item)
                if i == 0:
                    continue
                if(len(item.split(". ")) > 1):
                    total_response_list.append(item.split(". ")[1])
        print ('task end')
 
    # coroutine used for the entry point
    async def main():
        # report a message
        print('main starting')
        # create many coroutines
        coros = [task_coro(item) for i, item in enumerate(split_data)]
        # run the tasks
        await asyncio.gather(*coros)
        info = DataList(
                title= title,
                request= list_text,
                prompt_response= str(prompt_response),
                return_data= str(total_response_list)
        )
        await crud.save_datalist_info(db,info)
        # report a message
        print('main done') 
    asyncio.run(main())
    return {"list": total_response_list}

@app.post('/datalist/info')
def save_datalist_info(info :DataList, db=Depends(db)):
    print(type(info))
    print(info)
    object_in_db = crud.get_datalist_info(db, info.id)
    if object_in_db:
        raise HTTPException(400, detail= crud.error_message('This data info already exists'))
    return crud.save_datalist_info(db,info)

@app.get('/datalist/info/{id}')
def get_datalist_info(token: str, db=Depends(db)):
    info = crud.get_datalist_info(db,id)
    if info:
        return info
    else:
        raise HTTPException(404, crud.error_message('No device found for token {}'.format(token)))

@app.get('/device/info')
def get_all_datalist_info(db=Depends(db)):
    return crud.get_datalist_info(db)