import React,{useState} from 'react'



function MicButton() {
const [isClicked, setIsClicked] = useState(false);


  const handleClick = () => {
    setIsClicked(!isClicked);
  };


  return (
    <>
          <span onMouseDown={handleClick} onClick={handleClick} className={isClicked ? 'material-symbols-outlined btn-clkd wffwct-shadow ' : 'material-symbols-outlined'} >mic</span>

    </>
  )
}

export default MicButton;