from dotenv import load_dotenv
import asyncio
import openai as oa
import os


def openai(list_text: str):
    load_dotenv()
    oa.api_key= os.getenv("OPENAI_API_KEY")
    key = os.getenv("OPENAI_API_KEY")
    prompt = """
####
Here is an ordered list of the companies from the text:
1."""

    temperature = 0
    temp_data = (list_text + prompt).strip()
    temp_list = temp_data.split('\n')
    data_list = [x for x in temp_list if x != '']
    n= 120 # word count
    # split prompt data
    split_data = [(data_list[i:i+n]) for i in range(0, len(data_list), n)]
    total_response_list = []
    prompt_response = {}

    async def main():
        # report a message
        print('main starting')
        # run the tasks
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
        total_response_list.append(response_list[0].strip(''))
        for i, item in enumerate(response_list):
            if i == 0:
                continue
            if(len(item.split(". ")) > 1):
                total_response_list.append(item.split(". ")[1])
        print('main done')
    asyncio.run(main())
    return {"return_data": total_response_list, "prompt_response": prompt_response}