// Capture audio and send it to the server

import React, { useState, useRef } from 'react';
import axios from 'axios';
import Top from './components/Top';



function Gyan()
{

  const [isRecording, setIsRecording] = useState(false);
  const [recordedAudio, setRecordedAudio] = useState(null);

  const [isLoading,setIsLoading]=useState(false);
  const [messages,setMessages]=useState([])

  const getBlob=async()=>{
// document.getElementById('recordButton').addEventListener('click', async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    const chunks = [];

    mediaRecorder.ondataavailable = (e) => {
        chunks.push(e.data);
    };

    mediaRecorder.onstop = async () => {
        const blob = new Blob(chunks, { type: 'audio/wav' }); // Adjust type according to your audio format
        const formData = new FormData();
        formData.append('file', blob,"audioBlob.mp3");

        // const response = await fetch('/transcribe', {
        //     method: 'POST',
        //     body: formData
        // });
        console.log("HEllo")
        await axios.post("http://localhost:8000/talk/" ,formData,
        {headers:{
          // Accept:"audio/mpeg",
          "Content-Type":"multipart/form-data"}
          // body:blob
        // responseType:"arraybuffer"
        }
        // }
        ).then((res)=>{
    
          // setIsLoading(false);
        }).catch(error=>{
          console.log();
          console.log(error)
        })
          
        
        
    
        fetch()
        .then(response => {
            console.log('Audio data sent successfully:', response);
            //  audioUrl = URL.createObjectURL(new Blob([response.data]));
        })
        .catch(error => {
            console.error('Error sending audio data:', error);
        });
        
        // const transcription = await response.json();
        // console.log('Transcription:', transcription);
    };

    mediaRecorder.start();
    setTimeout(() => {
        mediaRecorder.stop();
    }, 8000); // Record for 15 seconds, adjust as needed
};

  




return(
<div className="App">
    
 <button  id='recordButton' onClick={getBlob()}>Click Me</button>
 {/* {getBlob()  } */}


</div>
);

}

export default Gyan;