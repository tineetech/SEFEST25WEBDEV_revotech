import React, { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Swal from 'sweetalert2'
import Home from './pages/Home'
import N404 from './pages/N404'
import ChatDokter from './pages/ChatDokter'
import Consultation from './pages/Consultation'
import Room from './pages/Room'
import Chats from './pages/Chats'
import RoomDokter from './pages/RoomDokter'
import ChatsDokter from './pages/ChatsDokter'
import CheckoutTempo from './pages/CheckoutTempo'

const PrivateRoute = ({element}) => {
  const cekLogin = sessionStorage.getItem('isLogin')
  const cekAdmin = sessionStorage.getItem('role')
    if (!cekLogin) {
      return <Navigate to='/' replace />
    } else if (cekLogin && cekAdmin === 'pembeli') {
      return <Navigate to='/' replace />
    }
    return element;
}

const RouterApp = () => {
  return (
    <Router>
        <Routes>
            <Route path='/' element={<Home/>} />
            <Route path='/konsultasi' element={<Consultation/>} />
            <Route path='/room' element={<Room/>} />
            <Route path='/room-dokter' element={<RoomDokter/>} />
            <Route path='/room/chat/:id' element={<Chats/>} />
            <Route path='/room/chat-dokter/:id' element={<ChatsDokter/>} />
            <Route path='/chat-dokter' element={<ChatDokter/>} />
            <Route path='/checkout' element={<CheckoutTempo/>} />
            <Route path='*' element={<N404/>} />
        </Routes>
    </Router>
  )
}

export default RouterApp