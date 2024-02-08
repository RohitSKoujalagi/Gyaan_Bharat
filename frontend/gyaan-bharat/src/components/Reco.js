import React from 'react'
import { ReactMediaRecorder } from "react-media-recorder";
import MicButton from './MicButton'



const Reco=(props)=> (
    <div>


        <ReactMediaRecorder
        audio
        onStop={props.handleStop}
        render={({  status,startRecording, stopRecording  }) => 
            <div>
              <p>{status}</p>
              <button className='rec-btn'  onMouseUp={stopRecording} onMouseDown={startRecording} >
                <MicButton/>
              </button>
            </div>
          }
        
        
        />


    </div>
);

export default Reco;