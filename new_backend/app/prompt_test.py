from dotenv import load_dotenv
import asyncio
import openai as oa
import os


def openai(data_list):
    print("#openai start")
    load_dotenv()
    oa.api_key= os.getenv("OPENAI_API_KEY")
    key = os.getenv("OPENAI_API_KEY")
    temp_list = data_list.split('\n')
    data_list = [x for x in temp_list if x != '']
    temp_prompt = "".join(data_list)
    prompt_prepend = f"""Extract ranking companies name from the text below.
    Text: {temp_prompt}
    """
    prompt =  prompt_prepend
    temperature = 0
    response = oa.Completion.create(
        model="text-davinci-002",
        prompt= prompt,
        temperature=temperature,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print(response)