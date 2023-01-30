from dotenv import load_dotenv
import asyncio
import openai as oa
import os


def openai(list_text: str):
    print("#openai start")
    load_dotenv()
    oa.api_key= os.getenv("OPENAI_API_KEY")
    key = os.getenv("OPENAI_API_KEY")
    prompt = """
####
Here is an ordered list of the companies from the text:
"""

    temperature = 0
    temp_data = (list_text + prompt).strip()
    temp_list = temp_data.split('\n')
    data_list = [x for x in temp_list if x != '']
    for item in data_list:
        print("**************************")
        print(item)
    n= 120 # sentence count
    # split prompt data
    split_data = [(data_list[i:i+n]) for i in range(0, len(data_list), n)]
    total_response_list = []
    prompt_response = {}
    prompt_prepend = ""
    for i, item in enumerate(split_data):
        temp_prompt = "".join(item) + prompt
        response = oa.Completion.create(
            model="code-davinci-002",
            prompt=prompt_prepend + temp_prompt,
            temperature=temperature,
            max_tokens=400,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop="####"
        )
        response_list = response["choices"][0]["text"].translate({ord('\t'):None}).split('\n')
        response_list = [x for x in response_list if x != '']
        prompt_prepend += str(response_list)
        print(response_list)
        prompt_response[temp_prompt] = response_list
    for i, item in enumerate(response_list):
        if(len(item.split(". ")) > 1):
            total_response_list.append(item.split(". ")[1])
    cleanup_response_list = []
    [cleanup_response_list.append(item) for item in total_response_list if item not in cleanup_response_list]
    print(cleanup_response_list)
    print("#openai end")
    return {"return_data": cleanup_response_list, "prompt_response": prompt_response}