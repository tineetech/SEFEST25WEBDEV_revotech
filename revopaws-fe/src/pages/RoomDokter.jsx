import { get, push, ref, set, update } from "firebase/database";
import React from "react";
import { db } from "../utils/firebaseConfig";
import Swal from "sweetalert2";
import { useNavigate } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

const validationSchema = Yup.object({
  room_id: Yup.string().required("Room Id wajib diisi"),
  room_password: Yup.string().required("Password wajib diisi"),
});

const RoomDokter = () => {
  const navigate = useNavigate();
  const getRandomInt = (min, max) => {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  };
  const joinRoom = async (values) => {
    Swal.fire({
      title: "Memproses...",
      allowOutsideClick: false,
      didOpen: () => {
        Swal.showLoading();
      },
    });
    try {
      const findRoom = await get(ref(db, `room_konsul/room${values.room_id}`));
      
      if (!findRoom.exists()) {
        Swal.fire({
          title: "Error",
          text: `Room ${values.room_id} dengan password ${values.room_password} Tidak tersedia.`,
          icon: "error",
        }).then((result) => (result.isConfirmed ? navigate("/room") : ""));
        return null
      }

      const roomData = findRoom.val();

      // Validasi password setelah data diambil
      if (roomData.configuration.room_password !== values.room_password) {
        Swal.fire({
          title: "Error",
          text: `Room Password salah.`,
          icon: "error",
        }).then((result) => (result.isConfirmed ? navigate("/room") : ""));
        return null;
      }

      console.log(findRoom)

      const uuid = crypto.randomUUID();
      console.log(uuid);

      Swal.fire({
        title: "Berhasil",
        text: `Berhasil masuk ke room ${values.room_id}`,
        icon: "success",
      }).then((result) => {
        if (result.isConfirmed) {
          update(ref(db, `room_konsul/room${values.room_id}/configuration`), {
            doctor_sessions: uuid
          })
          localStorage.setItem('doctor_sessions_' + values.room_id, uuid)
          navigate("/room/chat-dokter/" + values.room_id)
        }
      });
    } catch (error) {
      console.error("Error saat menulis data:", error);
    }
  };
  return (
    <div className="bg-gray-900 w-full h-screen text-white flex justify-center items-center">
      <div className="p-5 bg-gray-800 rounded-md">
        <h1 className="text-center mb-3">Join Room (sebagai dokter)</h1>
        <Formik
          initialValues={{ room_id: "", room_password: "" }}
          validationSchema={validationSchema}
          onSubmit={(values) => {
            joinRoom(values)
          }}
        >
          {() => (
            <Form className="flex flex-col gap-1">
              <label>ID Room</label>
              <Field name="room_id" type="text" className="bg-gray-700 text-white px-3 rounded-sm py-2" placeholder="Enter room id" />
              <ErrorMessage
                name="room_id"
                component="div"
                style={{ color: "red" }}
              />

              <label className="mt-3">Password Room</label>
              <Field name="room_password" type="password" className="bg-gray-700 text-white px-3 rounded-sm py-2" placeholder="Enter room password"  />
              <ErrorMessage
                name="room_password"
                component="div"
                style={{ color: "red" }}
              />

              <button
                type="submit"
                className="btn bg-blue-600 py-3 mt-5 w-full"
              >
                Masuk
              </button>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
};

export default RoomDokter;
