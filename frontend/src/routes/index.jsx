import { Routes, Route } from 'react-router-dom'
import Home from '../pages/Home' 
import Login from '../pages/Login'
import Cadastro from '../pages/Cadastro'

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/cadastro" element={<Cadastro />} />
    </Routes>
  )
}