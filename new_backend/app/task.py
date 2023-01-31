from dotenv import load_dotenv
import asyncio
import openai as oa
import os
import re


def openai(list_text: str):
    print("#openai start")
    load_dotenv()
    oa.api_key= os.getenv("OPENAI_API_KEY")
    key = os.getenv("OPENAI_API_KEY")

    temperature = 0
    temp_data = list_text.strip('\n').translate({ord('\t'):' '}).translate({ord('\n'):' '})
    temp_list = re.split(r'\b', temp_data)
    data_list = [x for x in temp_list if x != '']
    # for item in data_list:
    #     print("************start**************")
    #     print(item)
    #     print("***********end***************")
    n= 960 # word count
    # split prompt data
    split_data = [(data_list[i:i+n]) for i in range(0, len(data_list), n)]
    prompt_response = {}
    prompt_prepend = ""
    for i, item in enumerate(split_data):
        temp_prompt = "".join(item)
        prompt = f"""Extract rank company names from the text below.

        Desired format:
        <comma_separated_list_of_company_names>
        Text: {prompt_prepend + temp_prompt} 
        ####
        """
        print(prompt)
        response = oa.Completion.create(
            model="text-davinci-002",
            prompt= prompt,
            temperature=temperature,
            max_tokens=400,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop= "####"
        )
        response_list = response["choices"][0]["text"].translate({ord('\t'):None}).translate({ord('\n'):None}).split(', ')
        response_list = [x for x in response_list if x != '']
        print(response_list)
        temp_prepend = ""
        for i, item in enumerate(response_list):
            temp_prepend += str(item) + ' '
        prompt_prepend =temp_prepend
        prompt_response[temp_prompt] = response_list
    # for i, item in enumerate(response_list):
    #     if(len(item.split(". ")) > 1):
    #         total_response_list.append(item.split(". ")[1])
    cleanup_response_list = []
    [cleanup_response_list.append(item.strip()) for item in response_list if item not in cleanup_response_list]
    print(cleanup_response_list)
    print("#openai end")
    return {"return_data": cleanup_response_list, "prompt_response": prompt_response}