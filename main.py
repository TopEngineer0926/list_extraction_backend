from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import openai
import os

load_dotenv()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"id": "1234abcd", "request": request})


@app.get("/api")
async def api():

    prompt_prepend = """I'm looking for a job candidate to fill an open position I have at my company. Only respond with one message, do not write an entire conversation. Ask me questions about what I'm looking for in a candidate, and when you have enough information to give me a satisfactory query, give me a natural language search query. Ask me the relevant questions needed to obtain all of the following: skills, education, and possibly job history I need from the candidate. When you're ready to give me a search query, say something like "I have found the following candidates".

Categories: Skills, Degree Type, Current Employer, University Name

Hiring Manager: Hi
Recruiter: What kind of position are you looking to fill? What qualifications and experience are you looking for in the ideal candidate?
Hiring Manager: I'm looking for someone experienced in Python
Recruiter:
Are you looking for someone with a specific educational background, or just experience with Python in general? Are you open to someone with no formal job history in programming?
Hiring Manager: Sure, I suppose that's okay. I'm thinking they'll need a bachelor's degree in CS.
Recruiter: Got it. Is there any other specific experience or skills you're looking for in the ideal candidate?
Hiring Manager: Yes, they should have at least two years of experience programming with Python.
Recruiter:
Based on the information you provided, I have found these candidates:
Skills: Python, Degree Type: Bachelor's

Hiring Manager: Hi
Recruiter: What kind of position are you looking for? What qualifications and experience are you looking for in the ideal candidate?
Hiring Manager: a devops engineer who works at google
Recruiter: Are you looking for someone with a specific educational background, skills, and experience working at Google, or just someone who currently works there?
Hiring Manager: Ideally they'll have worked with databases. also docker and kubernetes
Recruiter: Got it. Are there any other specific qualifications you're looking for in the ideal candidate?
Hiring Manager: No, that's all.
Recruiter: Based on the information you provided, I have found the following candidates: Skills: Docker, Kubernetes, Database, Current Employer: Google.
Hiring Manager: Hi
Recruiter: """

    prompt = ""
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