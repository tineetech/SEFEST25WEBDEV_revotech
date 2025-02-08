import React, { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Swal from 'sweetalert2'
import Home from './pages/Home'
import N404 from './pages/N404'
import ChatDokter from './pages/ChatDokter'

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
            <Route path='/konsultasi' element={<ChatDokter/>} />
            <Route path='/chat-dokter' element={<ChatDokter/>} />
            <Route path='*' element={<N404/>} />
        </Routes>
    </Router>
  )
}

export default RouterApp