from dotenv import load_dotenv
import openai as oa
import os
import re


def openai(list_text: str):
    print("#openai start")
    load_dotenv()
    oa.api_key= os.getenv("OPENAI_API_KEY")
    key = os.getenv("OPENAI_API_KEY")

    temperature = 0.7
    temp_data = list_text.strip('\n').translate({ord('\t'):' '}).translate({ord('\n'):' '})
    temp_list = re.split(r'\b', temp_data)
    data_list = [x for x in temp_list if x != '']
    n= 2400 # word count 
    # split prompt data
    split_data = [(data_list[i:i+n]) for i in range(0, len(data_list), n)]
    print("*******************split data***************************")
    print(len(split_data[len(split_data) -1]))
    data_list_len = len(data_list)
    print(len(data_list))
    if(len(split_data[len(split_data) -1]) < n):
        split_data[len(split_data) -1]= data_list[data_list_len-n-1 : data_list_len-1]
    prompt_response = {}
    prompt_prepend = ""
    query = "companies"

    for i, item in enumerate(split_data):
        temp_prompt = "".join(item)
        prompt = f"""
        Extract the top company names from the text:
        Just include only names of the company.

        Desired format:
        <comma_separated_list_of_company_names>
        Text: {prompt_prepend + temp_prompt} 
        ####
        """
        print('***************************star of this is prompt**************************')
        print(prompt)
        print("***************************end of prompt**********************************")
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
    cleanup_response_list = []
    [cleanup_response_list.append(item.strip()) for item in response_list if item not in cleanup_response_list]
    print(cleanup_response_list)
    print("#openai end")
    return {"return_data": cleanup_response_list, "prompt_response": prompt_response}