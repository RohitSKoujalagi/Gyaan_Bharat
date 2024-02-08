from fastapi import FastAPI,UploadFile,File
from fastapi.responses import StreamingResponse,FileResponse
from fastapi.middleware.cors import CORSMiddleware
import json
from dotenv import load_dotenv
import openai
import os
import requests
from elevenlabs import generate,stream

# openai.organization=os.getenv("OPENAI_ORG")
app = FastAPI()

load_dotenv()
openai.api_key=os.getenv("OPENAI_API_KEY")
elevenlabs_key=os.getenv("ELEVENLABS_KEY")


#origins

origins=[
    "http://localhost:8000/",
    "http://localhost:8000/reset"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Endpoints

#To reset the message history in database.json file
@app.get("/reset/")
async def reset_msgs():
     open("database.json","w")
     return {"message": "Messages were RESET"}


#To Chat with GYAANI 
@app.post("/")
async def root(file: UploadFile=File(...)):

    try:
        
        with open(file.filename, "wb") as buffer:
         buffer.write(file.file.read())
        audio_input = open(file.filename, "rb")

        user_msg=transcribe_audio(audio_input)
        print("USER_MSG \n",user_msg)

    except Exception as e:
        print(e)

    try:
            chat_response=get_chat_response(user_msg)
            print("CHAT_RESPONSE\n",chat_response)

    
            audio_output=text_to_speech(chat_response)
            
            with open('LOL.mp3', mode='wb') as f:
              f.write(audio_output)
            OutFyl="LOL.mp3"

            return FileResponse(OutFyl)

    except Exception as e:
            print(e)


#Transcribes audio to text using OpenAI Whisper API.
def transcribe_audio(file):
    try:
      transcript = openai.audio.transcriptions.create(model="whisper-1", 
          file=file)
      return transcript.text
    
    except Exception as e:
        print(f"Could Not Transcribe Audio to Text \n Error: {e}")



#Queries the GPT-3.5-turbo model for a response to the user's message.
def get_chat_response(user_msg):
    messages=load_messages()
    messages.append({"role":"user","content":user_msg})
    print("Hurray!!!")

    gpt_response=openai.chat.completions.create(
     model="gpt-3.5-turbo",
     messages=messages
            )
    print("GPT RESPONSE = ",gpt_response.choices[0].message.content,"\n")
    save_messages(user_msg,gpt_response)
    return gpt_response.choices[0].message.content


#Generates speech audio from text using ElevenLabs Text-to-Speech API.
def text_to_speech(chat_response):

    voice_id="1qZOLVpd1TVic43MSkFY"
    voice_ID="tCdJgnmiVUt2DAMc1P0b"
    voice_idIndia="RkW4SvYcPQPWTpc0u2mu"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_idIndia}/stream"
    payload = {
    "model_id": "eleven_monolingual_v1",
    "text": f"{chat_response}",
    "voice_settings": {
        "similarity_boost": 0.40,
        "stability": 0.40,
        "style": 0.6,
        "use_speaker_boost": True
    },
    "optimize_streaming_latency":"2",
    "output_format":"mp3_44100_128"
            }

    headers = {"xi-api-key":elevenlabs_key,"Content-Type": "application/json",
               "accept":"audio/mpeg"
               }

    try:
      response = requests.request("POST",url, json=payload, headers=headers,stream=True)
      
      if response.status_code==200:
         return response.content
      else:
         print(f"Error Response Code : {response.status_code}")
    except Exception as e:
        print(e)
        

#Loads conversation history from database.json file.
def load_messages():
    messages=[]
    print("Yohooo")
    file="database.json"
    empty=os.stat(file).st_size==0

    if not empty:
        with open(file) as db_file:
            data=json.load(db_file)

            for item in data:
                messages.append(item)

    else:
        messages.append(
            {"role":"system","content":"You are an friendly and funny assistent who is a subject expert on India.Provide short answers that are relevant to Indians. Your name is Gyaani.Gyaani was made by Ro-hit Kau-ja-la-gi.You were created using whisper 1 model of open ai that transcribes voice to text then the text was passed to open ai gpt-3.5-turbo  API model to get a chat response from Chat GPT and then the response text was sent to elevenlabs API to convert text to speech.Keep response under 40 words and be funny most of the times.Do not hallucinate"}
        )

    return messages


#Saves the user's message and GPT-3 response to the database.json file.
def save_messages(user_msg,gpt_response):
    file='database.json'
    messages=load_messages()

    print("Yupp")

    messages.append({"role":"user","content":user_msg})
    messages.append({"role":"system","content":gpt_response.choices[0].message.content})

    with open(file,'w')  as f:
        json.dump(messages,f)

