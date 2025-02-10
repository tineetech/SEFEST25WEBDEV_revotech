const DataSentChat = ({
    user_id = "",
    doctor_id = "",
    sessions = "",
    doctor_name = "",
    role = "",
    message_type = "chat",
    file_url = "",
    message = "",
    status = ""
  }) => {
    return {
      user_id,
      doctor_id,
      sessions,
      doctor_name,
      role,
      message_type,
      file_url,
      message,
      status,
      timestamp: String(new Date()),
    };
  };
  
  export default DataSentChat;
  