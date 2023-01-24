from dotenv import load_dotenv
import asyncio
import openai_async
import os


def openai(list_text: str):
    load_dotenv()
    key = os.getenv("OPENAI_API_KEY")
    prompt_prepend = list_text
    prompt = """
####
Here is an ordered list of the companies from the text:
1."""
    temperature = 0
    temp_data = (prompt_prepend + prompt).strip()
    temp_list = temp_data.split('\n')
    n= 120 # word count
    # split prompt data
    split_data = [(temp_list[i:i+n]) for i in range(0, len(temp_list), n)]
    total_response_list = []
    prompt_response = {}

    async def task_coro(item):
        # report a message
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
        print(type(total_response_list))
        print ('task end')
 
    # coroutine used for the entry point
    async def main():
        # report a message
        print('main starting')
        # create many coroutines
        coros = [task_coro(item) for i, item in enumerate(split_data)]
        # run the tasks
        await asyncio.gather(*coros)
        print(total_response_list)
        print('main done') 
    asyncio.run(main())
    return {"return_data": total_response_list, "prompt_response": prompt_response}