#------------------------------------------------------------------------------------------------------------------------------------------#
#import azure.cognitiveservices.speech as speech_sdk: imports the Speech SDK module from the Azure Cognitive Services.                     #
#from dotenv import load_dotenv: imports the load_dotenv method from the dotenv library to load environment variables from a .env file.    #
#import os: imports the os module to access environment variables.                                                                         #
#import time: imports the time module to add a delay in the program.                                                                       #
#from datetime import datetime: imports the datetime module to work with timestamps.                                                       #
#from sounds import play_sound: imports the play_sound function from a separate sounds.py file.                                            #
#------------------------------------------------------------------------------------------------------------------------------------------#
import azure.cognitiveservices.speech as speech_sdk
from dotenv import load_dotenv
import os
import time
from datetime import datetime
from sounds import play_sound
import simpleaudio as sa
#---------------------------------------------------------------------------------------------------------------------------------------#
#   load_dotenv(override=True): loads environment variables from the .env file, overriding any existing values.                         #    
#   settings={...}: creates a dictionary object named settings with the values                                                          #
#   for the subscription key, service region, language, and OpenAI key. These values are retrieved from environment variables.          #
#---------------------------------------------------------------------------------------------------------------------------------------#
load_dotenv(override=True)
settings={
    'speechKey':os.environ.get('COG_SERVICE_KEY'),
    'region':os.environ.get('COG_SERVICE_REGION'),
    'language':os.environ.get('COG_SPEECH_LANGUAGE'),
    'openAIKey':os.environ.get('COG_OPENAI_KEY')
}

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#                                                                                                                                                                                                       
#   def start_recording():: defines a function named start_recording.                                                                                                                                   #
#   speech_config = speech_sdk.SpeechConfig(subscription = settings['speechKey'], region = settings['region']): creates a SpeechConfig object with the specified subscription key and service region.   #
#   speech_config.request_word_level_timestamps(): sets the SpeechConfig object to return word level timestamps in the response.                                                                        #
#   speech_config.set_property(...) : sets a property of the SpeechConfig object, which specifies the output format option for the speech service response.                                             #
#   audio_config = speech_sdk.audio.AudioConfig(use_default_microphone=True): creates an AudioConfig object that uses the default microphone for input.                                                 #
#   speech_recognizer = speech_sdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config): creates a SpeechRecognizer object with the SpeechConfig and AudioConfig objects.           #
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def start_recording():
    #creates an instance of a speech config with specified subscription key and service region.
    speech_config = speech_sdk.SpeechConfig(subscription = settings['speechKey'], region = settings['region'])
    
    speech_config.request_word_level_timestamps()
    speech_config.set_property(
        property_id= speech_sdk.PropertyId.SpeechServiceResponse_OutputFormatOption, value="detailed")
    
    
    #Creates a speech recognizer using the default microphone (built-in)
    audio_config = speech_sdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(
        speech_config= speech_config,audio_config=audio_config)
    
#----------------------------------------------------------------------------------------#
#                               EventHandler                                             #   
#----------------------------------------------------------------------------------------#
    results=[]
    done = False
    def speech_detected():
        nonlocal last_spoken
        last_spoken =last_spoken =int(datetime.now().timestamp()*1000)

    #for speech recognize we have to connect event
    def handle_results(evt):
        nonlocal results

        #now creating output Object with result text, how much it will take to speak, and finally the result
        res={'text':evt.result.text,'timestamp':evt.result.offset,
             'duration':evt.result.duration,'raw':evt.result}
        
        speech_detected()
        text = res["text"]
        print(f"text: {text}")
        if (res["text"]!=""):
            results.append(res)

    def speech_canceled(evt):
       nonlocal done
       done = True
    
    
    #we have different stages of event if it's recognize the text the session will start
    speech_recognizer.session_started.connect(lambda evt: print(f"Session Started {evt}"))
    speech_recognizer.session_stopped.connect(speech_canceled)
    speech_recognizer.recognizing.connect(lambda evt: speech_detected())
    speech_recognizer.canceled.connect(speech_canceled)
    speech_recognizer.recognized.connect(handle_results)
    result_future = speech_recognizer.start_continuous_recognition_async()
    result_future.get()

    last_spoken =int(datetime.now().timestamp()*1000)
    play_sound()
    while(not done):
       time.sleep(1)
       now =int(datetime.now().timestamp()*1000)
       inactivity = now-last_spoken
       if(inactivity > 1000):
          play_sound()
       if (inactivity>3000):
          print('Stopping async recognition.')
          speech_recognizer.stop_continuous_recognition_async()
          while not done:
             time.sleep(1)

    output=""
    for item in results:
        output+=item["text"]

    return output    


def speak(text,output_folder):
        speech_config = speech_sdk.SpeechConfig(
            subscription=settings['speechKey'], region=settings['region'])
        
        file_name = f'{output_folder}/{datetime.now().strftime("%Y%m%d_%H%M%S")}.wav'
        
        audio_config = speech_sdk.audio.AudioOutputConfig(
            use_default_speaker=True,filename=file_name) 
        
        speech_config.speech_synthesis_voice_name =  'en-IN-NeerjaNeural'
        speech_synthesizer = speech_sdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=audio_config
        )
        speech_synthesis_result= speech_synthesizer.speak_text(text)

        if speech_synthesis_result.reason == speech_sdk.ResultReason.SynthesizingAudioCompleted:
            play_obj = sa.WaveObject.from_wave_file(file_name).play()
            play_obj.wait_done()
        elif speech_synthesis_result.reason == speech_sdk.ResultReason.Canceled:
            cancellation_details= speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(
            cancellation_details.reason))
            if cancellation_details.reason == speech_sdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(
                    cancellation_details.error_details))
                    print("Did you set the speech resources key, OPENAPI Key and region values?")
                    