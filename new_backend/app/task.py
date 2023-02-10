from dotenv import load_dotenv
import asyncio
import openai as oa
import openai_async
import backoff
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
    n= 1200 # word count
    # split prompt data
    split_data = [(data_list[i:i+n]) for i in range(0, len(data_list), n)]
    data_list_len = len(data_list)
    if(len(split_data[len(split_data) -1]) < n):
        split_data[len(split_data) -1]= data_list[data_list_len-n-1 : data_list_len-1]
    prompt_response = {}
    ranked_response = []
    total_response_list = []
    total_response = []


    for i in range(0, len(split_data)):
        total_response_list.append('')
    
    query = "company"
    # query = "software"

    async def task_coro(item, index):
        # report a message
        print("task start")
        company_list = []
        text = "".join(item)
        prompt = f"""Please extract name the of {query} from the text:
Just include only name of the {query}.
Desired format:
<comma_separated_list_of_{query}_names>
Text:{text}
####"""

        @backoff.on_exception(backoff.expo, oa.error.RateLimitError)
        def completions_with_backoff(key, timeout, payload):
                return openai_async.complete(key, timeout=timeout, payload=payload)
        # await delay_time()
        try:
            response = await completions_with_backoff(
                key,
                timeout=50,
                payload={
                    "model": "text-davinci-003",
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_tokens": 400,
                    "top_p":1,
                    "frequency_penalty":0,
                    "presence_penalty":0,
                    'stop':"####"
                },
            )
            response_list =response.json()["choices"][0]["text"].translate({ord('\t'):None}).split(', ')
        except Exception as e:
            response_list =[]
            print(e)
        for i, item in enumerate(response_list):
            company_list.append(item)
        total_response_list[index] = company_list
        print ('task end')
    # coroutine used for the entry point
    #main start
    async def main():
        # report a message
        print('main starting')
        # create many coroutines
        coros = [task_coro(item, i) for i, item in enumerate(split_data)]
        # run the tasks
        await asyncio.gather(*coros)
        print(total_response_list)
        for i, items in enumerate(total_response_list):
            for i, item in enumerate(items):
                total_response.append(item)
        cleanup_response_list = []
        [cleanup_response_list.append(item.strip()) for item in total_response if item not in cleanup_response_list]
        ranked_result = ""
        for i, item in enumerate(cleanup_response_list):
            ranked_result += str(item) + ', '
        prompt = f"""
Please rank the following {query} from best to worst:
Desired format:
<comma_separated_list_of_{query}_names>
{ranked_result}

####
"""
        try:
            response = await openai_async.complete(
                key,
                timeout=50,
                payload={
                    "model": "text-davinci-003",
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_tokens": 400,
                    "top_p":1,
                    "frequency_penalty":0,
                    "presence_penalty":0,
                    'stop':"####"
                },
            )
            ranked_cleanup_result = response.json()["choices"][0]["text"].translate({ord('\t'):None}).translate({ord('\n'):None}).split(', ')
        except Exception as e:
            print(e)
        for i, item in enumerate(ranked_cleanup_result):
            ranked_response.append(item)
        print('main done')
    #main end
    asyncio.run(main())
    return {"return_data": ranked_response, "prompt_response": prompt_response}