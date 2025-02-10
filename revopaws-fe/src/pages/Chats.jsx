import { get, onValue, push, ref, set, update } from "firebase/database";
import React, { useEffect, useRef, useState } from "react";
import { db } from "../utils/firebaseConfig";
import Swal from "sweetalert2";
import { useNavigate, useParams } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import ChatBubble from "../components/ChatBubble";
import axios from "axios";
import DataSentChat from "../utils/DataSentChat";

const validationSchema = Yup.object({
  message: Yup.string().required("Pesan tidak boleh kosong"),
});

const Chats = () => {
  const navigate = useNavigate();
  const chatContainerRef = useRef(null);
  const fileInputRef = useRef(null);
  const { id } = useParams();
  const [messages, setMessages] = useState([]);
  const [file, setFile] = useState({
    file: null,
    url: "",
  });

  useEffect(() => {
    const messagesRef = ref(db, `room_konsul/room${id}/chats`);
    onValue(messagesRef, (snapshot) => {
      const data = snapshot.val();
      if (data) {
        setMessages(Object.entries(data).map(([key, value]) => ({ key, ...value })))
        // setMessages(Object.values(data));
      }
    });
  }, []);
  
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.visibilityState === "visible" && document.hasFocus()) {
        if (messages.some((msg) => msg.role === "doctor" && msg.status !== "read")) {
          markAsRead();
        }
      }
    };
  
    // Tambahkan event listener untuk visibility dan focus
    document.addEventListener("visibilitychange", handleVisibilityChange);
    window.addEventListener("focus", handleVisibilityChange);
  
    // Panggil sekali saat komponen pertama kali dipasang
    handleVisibilityChange();
  
    return () => {
      document.removeEventListener("visibilitychange", handleVisibilityChange);
      window.removeEventListener("focus", handleVisibilityChange);
    };
  }, [messages]); // Efek hanya berjalan jika `messages` berubah  

  useEffect(() => {
    if (chatContainerRef.current) {
      setTimeout(() => {
        chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
      }, 100); // Delay 100ms agar pesan benar-benar dirender sebelum scroll
    }
  }, [messages]); // Efek hanya berjalan jika `messages` berubah
  

  useEffect(() => {
    checkRoomAndSessions();
  }, []);

  const checkRoomAndSessions = async () => {
    Swal.fire({
      title: "Tunggu sebentar...",
      allowOutsideClick: false,
      didOpen: () => {
        Swal.showLoading();
      },
    });
    try {
      const findRoom = await get(ref(db, `room_konsul/room${id}`));
      if (!findRoom.exists()) {
        Swal.fire({
          title: "Error",
          text: `Room ${id} tidak ditemukan.`,
          icon: "error",
        }).then((result) => (result.isConfirmed ? navigate("/room") : ""));
        return null;
      }

      const roomData = findRoom.val();
      if (roomData.configuration.user_sessions !== localStorage.getItem('user_sessions_' + id)) {
        Swal.fire({
          title: "Error",
          text: `Kamu tidak memiliki akses untuk room ini.`,
          icon: "error",
        }).then((result) => (result.isConfirmed ? navigate("/room") : ""));
        return null;
      }

      Swal.close();
    } catch (error) {
      console.error("Error saat verifikasi room:", error);
    }
  };
  
  const markAsRead = async () => {
    const findUserRole = messages.filter(item => item.role === "doctor")
    console.log(findUserRole)
    findUserRole.map((item) => {
      update(ref(db, `room_konsul/room${id}/chats/${item.key}`), {
        status: "read",
      });
    })
  };

  const sendMessage = async (values, { resetForm }) => {
    if (file.file !== null) {
      const formData = new FormData();
      formData.append("file", file.file);
      formData.append("room_id", id); // Kirim room_id
      formData.append("chat_id", "828"); // Kirim chat_id

      try {
        const response = await axios.post(`${import.meta.env.VITE_URL_BE}/api/consultations/upload-file/`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
  
        alert(`File uploaded: ${response.data.file_url}`);
        const messageRef = ref(db, `room_konsul/room${id}/chats`);
        const data = DataSentChat({
          user_id: id,
          doctor_id: "",
          sessions: localStorage.getItem('user_sessions_' + id),
          doctor_name: "",
          role: "user",
          message_type: "file",
          file_url: response.data.file_url,
          message: values.message,
          status: "unread",
        })
        await push(messageRef, data);
        setFile({...file, file: null, url: "" })
        return resetForm(); 
      } catch (error) {
        console.error("Upload error:", error);
        alert("Upload failed");
      }
    }
    try {
      const messageRef = ref(db, `room_konsul/room${id}/chats`);
      const data = DataSentChat({
        user_id: id,
        doctor_id: "",
        sessions: localStorage.getItem('user_sessions_' + id),
        doctor_name: "",
        role: "user",
        message_type: "chat",
        file_url: "",
        message: values.message,
        status: "unread",
      })
      await push(messageRef, data);
      resetForm();
    } catch (error) {
      console.error("Error saat mengirim pesan:", error);
      Swal.fire({
        icon: "error",
        title: "Gagal mengirim pesan.",
      });
    }
  };

  const handleChangeFiles = (e) => {
    const files = e.target.files[0]; // Mengambil file pertama yang dipilih
    
    if (!files) return; // Jika tidak ada file, hentikan fungsi
  
    const fileUrl = URL.createObjectURL(files); // Membuat URL blob untuk pratinjau
    
    setFile({ ...file, file: files, url: fileUrl }); // Menyimpan file & URL ke state
  };
  

  return (
    <div className="bg-gray-900 w-full h-screen text-white flex justify-center items-center">
      <div className="bg-gray-800 overflow-hidden w-full h-full rounded-md">
        <div className="p-3">
          <h1 className="text-center">Room Konsultasi #{id}</h1>
        </div>
        <div className="flex">
          <aside className="w-[30%] container bg-gray-900 border-r-2 border-gray-600">
            <div className="container w-full mx-5 my-10">
              <ul className="w-full gap-3 flex flex-col">
                <li className="flex w-[90%] py-3 px-4 rounded-md gap-4 bg-opacity-10 hover:bg-opacity-100 bg-blue-500">
                  <i className="bi-house"></i>
                  <span>Home</span>
                </li>
                <li className="flex w-[90%] py-3 px-4 rounded-md gap-4 bg-opacity-0 hover:bg-opacity-100 bg-blue-500">
                  <i className="bi-house"></i>
                  <span>Home</span>
                </li>
                <li className="flex w-[90%] py-3 px-4 rounded-md gap-4 bg-opacity-0 hover:bg-opacity-100 bg-blue-500">
                  <i className="bi-house"></i>
                  <span>Home</span>
                </li>
              </ul>
            </div>
          </aside>
          <div ref={chatContainerRef} className="w-[70%] gap-5 overflow-y-auto hide-scrollbar relative flex flex-col h-[100vh] bg-gray-900">
            <div className="flex flex-col gap-5 px-4 pt-5 h-auto pb-32 w-full">
              {messages.map((msg, index) => (
                <ChatBubble key={index} message={msg.message} messType={msg.message_type} fileUrl={msg.file_url} doctorName={msg.doctor_name} status={msg.status} timestamp={msg.timestamp.slice(0, 21)} role={msg.role} />
              ))}
            </div>
            <Formik
              initialValues={{ message: "" }}
              validationSchema={validationSchema}
              onSubmit={sendMessage}
            >
              {({ isSubmitting }) => (
                <Form className="flex items-center fixed bottom-0 w-[70%] px-3 py-4 bg-gray-700 dark:bg-gray-700">
                  <div className="relative">
                    <div className={`bg-gray-500 absolute p-3 bottom-12 w-auto flex gap-2 rounded-md ${file.file ? "" : "hidden"}`}>
                      <img src={file.url ?? ""} className="object-cover" style={{width: "20px", height: "20px"}} alt="" />
                    </div>
                    <button type="button" className="inline-flex justify-center relative w-12 h-10 items-center text-lg text-white-500 bg-blue-500 rounded-full cursor-pointer hover:bg-blue-600 dark:hover:bg-gray-600" onClick={() => fileInputRef.current.click()}>
                      <i className="bi-file-earmark-arrow-up-fill"></i>
                      <input type="file" className="hidden" accept="image/*" onChange={(e) => handleChangeFiles(e)} ref={fileInputRef}/>
                    </button>
                  </div>
                  <div className="flex flex-col gap-1 w-full justify-start px-4 items-start">
                    <Field
                      name="message"
                      as="textarea"
                      rows={1}
                      className="block p-2.5 w-full text-sm text-white rounded-lg border border-gray-600 bg-gray-600 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                      placeholder="Your message..."
                      onKeyDown={(e) => {
                        if (e.key === "Enter" && !e.shiftKey) {
                          e.preventDefault(); // Mencegah baris baru di textarea
                          e.target.form.requestSubmit(); // Submit Formik form
                        }
                      }}                    
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="inline-flex justify-center disabled:bg-blue-600 p-2 text-white-500 bg-blue-500 rounded-full cursor-pointer hover:bg-blue-600 dark:hover:bg-gray-600"
                  >
                    <svg
                      className="w-5 h-5 rotate-90 rtl:-rotate-90"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="currentColor"
                      viewBox="0 0 18 20"
                    >
                      <path d="m17.914 18.594-8-18a1 1 0 0 0-1.828 0l-8 18a1 1 0 0 0 1.157 1.376L8 18.281V9a1 1 0 0 1 2 0v9.281l6.758 1.689a1 1 0 0 0 1.156-1.376Z" />
                    </svg>
                    <span className="sr-only">Send message</span>
                  </button>
                </Form>
              )}
            </Formik>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chats;