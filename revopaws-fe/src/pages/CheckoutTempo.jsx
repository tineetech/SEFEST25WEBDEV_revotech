import { get, push, ref, set, update } from "firebase/database";
import React from "react";
import { db } from "../utils/firebaseConfig";
import Swal from "sweetalert2";
import { useNavigate } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import axios from "axios";
import LoadSnapScript from "../utils/LoadMidtrans";

const validationSchema = Yup.object({
  gross_amount: Yup.string().required("Total harga wajib diisi"),
});

const CheckoutTempo = () => {
  const navigate = useNavigate();
  
  const getRandomInt = (min, max) => {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  };

  const bayar = async (values) => {
    Swal.fire({
      title: "Memproses...",
      allowOutsideClick: false,
      didOpen: () => {
        Swal.showLoading();
      },
    });
    try {
      const createSnap = await axios.post(`${import.meta.env.VITE_URL_BE}/api/payment/create/`, {
        order_id: getRandomInt(1, 100),
        gross_amount: values.gross_amount
      }, {
        headers: { "Content-Type": "multipart/form-data" },
      });;
      
      if (!createSnap) {
        Swal.fire({
          title: "Error",
          text: `Gagal membuat snap.`,
          icon: "error",
        }).then((result) => (result.isConfirmed ? navigate("/checkout") : ""));
        return null
      }

      console.log(createSnap)

      Swal.fire({
        title: "Berhasil",
        text: `Berhasil Membuat snap payment midtrans, silakan coba dan bayar dengan simulator https://simulator.sandbox.midtrans.com/openapi/va/index?bank=bri`,
        icon: "success",
      }).then(async (result) => {
        if (result.isConfirmed) {
          try {
            const snap = await LoadSnapScript();
            snap.pay(createSnap.data.token, {
                onSuccess: (result) => {
                    console.log("Payment Success:", result);
                    alert("Pembayaran berhasil!");
                },
                onPending: (result) => {
                    console.log("Payment Pending:", result);
                    alert("Pembayaran tertunda. Silakan selesaikan di halaman pembayaran.");
                },
                onError: (result) => {
                    console.error("Payment Error:", result);
                    alert("Terjadi kesalahan saat pembayaran.");
                },
                onClose: () => {
                    console.log("User closed the payment popup.");
                    alert("Anda menutup halaman pembayaran.");
                },
            });
        } catch (error) {
            console.error("Error loading Midtrans Snap:", error);
        }
        }
      });
    } catch (error) {
      console.error("Error saat menulis data:", error);
    }
  };
  return (
    <div className="bg-gray-900 w-full h-screen text-white flex justify-center items-center">
      <div className="p-5 bg-gray-800 rounded-md">
        <h1 className="text-center mb-3">Checkout</h1>
        <Formik
          initialValues={{ gross_amount: "" }}
          validationSchema={validationSchema}
          onSubmit={(values) => {
            bayar(values)
          }}
        >
          {() => (
            <Form className="flex flex-col gap-1">
              <label>Total harga belanja</label>
              <Field name="gross_amount" type="number" className="bg-gray-700 text-white px-3 rounded-sm py-2" placeholder="Enter groos amount" />
              <ErrorMessage
                name="gross_amount"
                component="div"
                style={{ color: "red" }}
              />

              <button
                type="submit"
                className="btn bg-blue-600 py-3 mt-5 w-full"
              >
                Bayar
              </button>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
};

export default CheckoutTempo;
