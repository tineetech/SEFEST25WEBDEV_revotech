// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getDatabase } from "firebase/database";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAVUzZp75gPzA52Gyrhp6a9WW43rYKjI2E",
  authDomain: "revopaws-realtime.firebaseapp.com",
  databaseURL: "https://revopaws-realtime-default-rtdb.firebaseio.com",
  projectId: "revopaws-realtime",
  storageBucket: "revopaws-realtime.firebasestorage.app",
  messagingSenderId: "729783084020",
  appId: "1:729783084020:web:43b98bb7a1537da73d4fa1",
  measurementId: "G-EJDWHFXTDR"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const db = getDatabase(app);

export { analytics, db }