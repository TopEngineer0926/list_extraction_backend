from fastapi import FastAPI, Request
from dotenv import load_dotenv
import openai
import os

load_dotenv()
app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
async def root(request: Request):
    return "works"


@app.get("/api")
async def api():

    prompt_prepend = "Hello, "

    prompt = "how are you?"
    temperature = 0.7

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_prepend + prompt,
        temperature=temperature,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop="Hiring Manager:"
    )

    return {"response_text": response['choices'][0]['text']}