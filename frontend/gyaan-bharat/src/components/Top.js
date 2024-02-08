import { useState } from "react";
import axios from "axios";



  function Top(props) {

    const [isResetting,setIsResetting]=useState(false)

    const resetConversation=async ()=>{
      setIsResetting(true);
      await axios.get("http://localhost:8000/reset").then((res)=>{
        if(res.status===200){
          props.setMessages([])
        }
        else{
          console.error("There was an error resetting messages")
        }
      }).catch((err)=>{
        console.error(err)
      })
      setIsResetting(false);
    }

  return (

    <div>
          <button onClick={resetConversation} className='btn btn-warning reset-btn'>Reset</button>

    </div>

  )
}

export default Top;