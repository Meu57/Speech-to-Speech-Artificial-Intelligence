import openai
from dotenv import load_dotenv
import os
load_dotenv(override=True)

setting ={
    'openAIkey': os.environ.get('COG_OPENAI_KEY')
}

openai.api_key=setting['openAIkey']

def complete_openai(prompt,token=50):
    try:
        response = openai.Completion.create(
            model = "text-davinci-003",
            prompt = prompt,
            temperature=0.5,
            max_tokens=token,
            top_p=1,
            presence_penalty=1.5,
            frequency_penalty=1.5
        )
            
        
        lines= response.to_dict_recursive()['choices'][0]['text'].split("\n")
        response = '\n'.join(list(filter(lambda x: x != '',lines)))
        return response
    except Exception as e:
        print("An exception of type", type(e),"occurred with the message:",e)



