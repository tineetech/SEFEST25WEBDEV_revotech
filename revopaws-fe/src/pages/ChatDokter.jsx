import React from 'react'
import ChatDokterCompomemt from '../components/ChatDokterComponent'

const ChatDokter = () => {
  return (
    <div className='w-full bg-red-50 h-full flex-col flex justify-center items-center'>
        <h1>Chat dokter</h1>
        <ChatDokterCompomemt />
    </div>
  )
}

export default ChatDokter