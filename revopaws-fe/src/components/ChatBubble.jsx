import React from 'react'

const ChatBubble = ({ messType = "chat", fileUrl = "", role = 'user', message = "", status = "unread", timestamp, doctorName = "Dr. Sri Haryani" }) => {
  return (
    <div className={`flex w-full ${role === "user" ? " flex-row-reverse" : "justify-start"} items-start gap-2.5`}>
        <img className="w-8 h-8 rounded-full" src={role === "user" ? "https://static.vecteezy.com/system/resources/previews/036/280/651/non_2x/default-avatar-profile-icon-social-media-user-image-gray-avatar-icon-blank-profile-silhouette-illustration-vector.jpg" : "https://imgcdn.stablediffusionweb.com/2024/3/30/68e909a4-34e6-403d-97fc-72cee0558af0.jpg"} alt="image" />
        <div className={`flex flex-col w-full ${role === "user" ? "text-end rounded-s-xl rounded-ee-xl" : "text-start rounded-e-xl rounded-es-xl"} max-w-[320px] leading-1.5 p-4 border-gray-200 bg-gray-700 dark:bg-gray-700`}>
            <span className="text-sm font-semibold text-white">{role === "user" ? "Kamu" : doctorName} <i className={`text-blue-400 ml-1 bi-patch-check-fill ${role === "user" ? "hidden" : "inline"}`}></i></span>
            {messType === "chat" ? (
                <p className="text-sm font-normal py-2.5 text-gray-300">{message}</p>
            ) : (   
                <>
                    <p className="text-sm font-normal py-2.5 text-gray-300">{message}</p>
                    <img className=" rounded-sm mt-2 mb-5" src={fileUrl ?? ""} alt="image" />
                </>
            )}
            <div className={`flex ${role === "user" ? "items-end gap-2 flex-row-reverse" : ""}`}>
                <span className={`text-sm font-normal text-gray-400 ${role === "doctor" ? "hidden" : ""}`}><i className={`bi-check-all ${status === "read" ? "text-blue-500" : "text-gray-500"}`}></i></span>
                <span className="text-sm font-normal text-gray-500">{timestamp}</span>
            </div>
        </div>
    </div>
  )
}

export default ChatBubble