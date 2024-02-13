from fastapi import FastAPI,UploadFile,File
from fastapi.responses import StreamingResponse,FileResponse
from fastapi.middleware.cors import CORSMiddleware
import json
from dotenv import load_dotenv
import openai
import os
import requests

app = FastAPI()

load_dotenv()
open_api_key=os.getenv("OPENAI_API_KEY")
elevenlabs_key=os.getenv("ELEVENLABS_KEY")


#origins

origins=[
    "http://localhost:8000/",
    "http://localhost:8000/reset",
    "https://gyaani-2-0.onrender.com/",
    "https://gyaani-2-0.onrender.com/reset/",
    "http://localhost:3000/",
    "http://localhost:3000",
    "https://rohitskoujalagi.github.io/Gyaani/"
    "https://rohitskoujalagi.github.io/Gyaani",
    "https://rohitskoujalagi.github.io",
    "https://rohitskoujalagi.github.io/"
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

        user_msg=req_transcribe(audio_input)
        print("USER_MSG \n",user_msg)

    except Exception as e:
        print(e)

    try:
            chat_response=chat_completion(user_msg)
            print("CHAT_RESPONSE\n",chat_response)
    except Exception as e:
            print("Chat Res ERRor \n",e)


    try:
            audio_output=txtToSpeech(chat_response)
            
            with open('LOL.mp3', mode='wb') as f:
              f.write(audio_output)

            OutFyl="output.mp3"
            return FileResponse(OutFyl)

    except Exception as e:
            print(e)


#Transcribes audio to text using OpenAI Whisper API.
# def transcribe_audio(file):
#     try:
#       transcript = openai.audio.transcriptions.create(model="whisper-1", 
#           file=file)
#       return transcript.text
    
#     except Exception as e:
#         print(f"Could Not Transcribe Audio to Text \n Error: {e}")


# def createTranscribedAudioFile():
#     url=f"https://cloud.appwrite.io/v1//storage/buckets/{bucketId}/files"
            

def req_transcribe(file):
    try:

        url = "https://api.openai.com/v1/audio/transcriptions"

        payload = {
            "model": "whisper-1",
            "response_format":"text"
            }
        
        files={"file":file}

        headers = {
             'Authorization': f"Bearer {open_api_key}"
                    }
        

        response = requests.request("POST", url, headers=headers, data=payload,files=files)

        print("res=\n",response.text)
        return response.text


    except Exception as e:
        print("Error from req_transcribe \n",e)


#Queries the GPT-3.5-turbo model for a response to the user's message.
# def get_chat_response(user_msg):
#     messages=load_messages()
#     messages.append({"role":"user","content":user_msg})

#     gpt_response=openai.chat.completions.create(
#      model="gpt-3.5-turbo",
#      messages=messages
#             )
#     print("GPT RESPONSE = ",gpt_response.choices[0].message.content,"\n")
#     save_messages(user_msg,gpt_response)
#     return gpt_response.choices[0].message.content



def chat_completion(user_msg):

 try:
    messages=load_messages()
    print("MESSAGES=\n",messages)
    messages.append({"role":"user","content":user_msg})

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {open_api_key}"
        }

    data = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.5,
        }


    gpt_response=requests.post(url,headers=headers,json=data)

    json_response=gpt_response.json()
    
    print("\nJSON RESPONSE = ",json_response["choices"][0]["message"]["content"],"\n")
    save_messages(user_msg,json_response["choices"][0]["message"]["content"])


    return json_response["choices"][0]["message"]["content"]
 except Exception as e:
     print("Error from chat_completion=\n",e)


#Generates speech audio from text using ElevenLabs Text-to-Speech API.
def text_to_speech(chat_response):
  
    # voice_id="96oPcs6oI8iZWmOgaWMP"
    # voice_ID="tCdJgnmiVUt2DAMc1P0b"
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

    headers = {"xi-api-key":f"{elevenlabs_key}","Content-Type": "application/json",
               "accept":"audio/mpeg"
               }
    # print(elevenlabs_key)

    try:
      response = requests.request("POST",url, json=payload, headers=headers,stream=True)
      print(response.json())
      
      if response.status_code==200:
         return response.content
      else:
         print(f"Error Response Code iz : {response.status_code}")

    except Exception as e:
        print("Error from text_to_speech\n",e)


def txtToSpeech(chat_response):
    try:
        url = "https://api.openai.com/v1/audio/speech"

# Define the request payload
        payload = {
        "model": "tts-1-hd",
        "input": chat_response,
        "voice": "fable",
        "response_format": "mp3",
        "speed": 0.5
            }


# Set the request headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {open_api_key}"
                }

# Make the POST request
        response = requests.post(url, json=payload, headers=headers)

# Check if the request was successful
        if response.status_code == 200:
    # Save the audio file
            print("\nRESPECT\n")
            # with open("output.mp3", "wb") as f:
            #   f.write(response.content)
            # print("Audio file generated successfully.")
            return response.content

            

        else:
         print("Error:", response.text)



    except Exception as e:
        print("\nError in txttospeech is\n",e)
        

#Loads conversation history from database.json file.
def load_messages():
    messages=[]
    file="database.json"
    empty=os.stat(file).st_size==0

    if not empty:
        with open(file) as db_file:
            data=json.load(db_file)

            for item in data:
                messages.append(item)

    else:
        messages.append(
            {"role":"system","content":"You are an friendly and funny assistent who is a subject expert on India.Provide short answers that are relevant to Indians.Your name is Gyaani.Keep response under 30 words and be funny most of the times.Do not hallucinate"}
        )

    return messages


#Saves the user's message and GPT-3 response to the database.json file.
def save_messages(user_msg,gpt_response):
    file='database.json'
    messages=load_messages()

    print("Yupp")

    messages.append({"role":"user","content":user_msg})
    messages.append({"role":"system","content":gpt_response})

    with open(file,'w')  as f:
        json.dump(messages,f)

