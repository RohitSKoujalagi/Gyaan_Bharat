import React, { useState } from 'react';
import axios from 'axios';
import Top from './components/Top';
import Reco from './components/Reco';

function Main() {

  const [btnClkd,setBtnClkd]=useState(false)

  const [isLoading,setIsLoading]=useState(false);
  const [messages,setMessages]=useState([])

  const createBlobUrl=(data)=>{

    const blob=new Blob([data],{type:"audio/mpeg"});
    const url=window.URL.createObjectURL(blob);
    return url;

  };

  const handleStop= async (blobUrl)=>{
    setIsLoading(true);


    fetch(blobUrl)
    .then((res)=>res.blob()
    .then(async (blob)=>{  

      const formData=new FormData();
      formData.append("file",blob,"audio_file.wav");

      let url="https://gyaani-2-0.onrender.com/"
      
      // let url="http://localhost:8000"

      const fyl=await axios.post(url,formData,
      {
        headers:{"Content-Type":"audio/mpeg"},responseType:"arraybuffer",
      })
      .then((res)=>{
        const blob=res.data;
        console.log(res);
        const audio=new Audio();
        audio.src=createBlobUrl(blob);

        setIsLoading(false);
        audio.play();


      })
      .catch((err)=>{
        console.error(err.message);
        setIsLoading(false);
      })

    })
    .catch((err)=>{console.err(err)}))
    .catch((err)=>{console.err(err)})

  };



  return (
    <div className="App Main">
      
      <Top setMessages={setMessages}/>
      <Reco handleStop={handleStop}  />

    </div>
  );
}

export default Main;




