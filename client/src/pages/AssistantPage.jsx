import React from 'react'
import Chatbot from '../components/ChatBot'
import VoiceAssistant from '../components/VoiceAssistant'

const AssistantPage = () => {
  return (
    <>
    <h1 className='text-2xl text-bold text-center text-archivo-black pt-6 font-gaegu'>Claremont Intelligent Assistant</h1>
    <h2 className='text-2xl text-bold text-center text-archivo-black font-gaegu'>AMA about transporation, restaurants, social events!</h2>
    <VoiceAssistant />
    <div className="h-64"></div> 
    </>
  )
}

export default AssistantPage