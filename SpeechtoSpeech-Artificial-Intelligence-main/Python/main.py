from dotenv import load_dotenv
import os
from datetime import datetime
from speech_processing import start_recording, speak
from openai_processing import complete_openai

load_dotenv(override=True)
settings={
    'speechKey':os.environ.get('COG_SERVICE_KEY'),
    'region':os.environ.get('COG_SERVICE_REGION'),
    'language':os.environ.get('COG_SPEECH_LANGUAGE'),
    'openAIKey':os.environ.get('COG_OPENAI_KEY')
}

output_folder=f'.Output/{datetime.now().strftime("%Y%m%d_%H%M%S")}/'
os.makedirs(output_folder)

conversation=[]
for i in range(0,5):
    speech=start_recording()
    conversation.append(speech)
    prompt =""
    for i in range(len(conversation)-4, len(conversation)):
        if(i>=0):
            if(i%2==0):
                prompt +=f"Q: {conversation[i]}\n"
            else:
                prompt += f"A: {conversation[i]}\n"
    prompt+="A: "
    result = complete_openai(prompt=prompt, token=3000)
    print(result)
    speak(result, output_folder=output_folder)
    conversation.append(result)
   #let's run this