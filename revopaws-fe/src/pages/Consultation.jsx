import { push, ref, set } from "firebase/database";
import React from "react";
import { db } from "../utils/firebaseConfig";
import Swal from "sweetalert2";
import { useNavigate } from "react-router-dom";

const Consultation = () => {
  const navigate = useNavigate();
  const getRandomInt = (min, max) => {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  };
  const handleKonsul = async () => {
    Swal.fire({
      title: "Memproses...",
      allowOutsideClick: false,
      didOpen: () => {
        Swal.showLoading();
      },
    });
    const room_id = getRandomInt(1, 900);
    const data = {
      chats: {
      },
      configuration: {
        room_id,
        room_password: "eiwfhsdfiqyweuewfds2918321hidsh",
        user_id: 2,
        user_sessions : "",
        doctor_sessions: "",
        pet_id: 8,
        doctor_id: 12,
        consultation_id: 12,
        consultation_type: "chat",
        consultation_payment: "paid",
        room_status: "open",
        created_at: "now",
        updated_at: "now",
      },
    };
    try {
      await set(ref(db, `room_konsul/room${room_id}`), data);
      Swal.fire({
        title: "Berhasil",
        text: `Room id: ${room_id}, Room Password: ${data.configuration.room_password}. Simpan data tersebut untuk login ke room konsultasi !`,
        icon: "success",
      }).then((result) => (result.isConfirmed ? navigate("/room") : ""));
    } catch (error) {
      console.error("Error saat menulis data:", error);
    }
  };
  return (
    <div className="bg-gray-900 w-full h-screen text-white flex justify-center items-center">
      <div className="p-5 bg-gray-800 rounded-md">
        <h1 className="text-center">Konsultasi</h1>
        <div className="flex gap-10 mt-2 justify-between">
          <span>Nama dokter</span>
          <span>Dr. Sri Haryani</span>
        </div>
        <div className="flex gap-10 mt-2 justify-between">
          <span>Jenis Konsultasi</span>
          <span>Chat</span>
        </div>
        <div className="flex gap-10 mt-2 justify-between">
          <span>Harga</span>
          <span>Rp 200.000</span>
        </div>
        <button
          className="btn bg-blue-600 py-3 mt-5 w-full"
          onClick={handleKonsul}
        >
          Konsultasi Sekarang
        </button>
      </div>
    </div>
  );
};

export default Consultation;
