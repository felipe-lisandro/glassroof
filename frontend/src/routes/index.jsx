import { Routes, Route } from "react-router-dom"
import Home from "../pages/Home"
import Login from "../pages/Login"
import Cadastro from "../pages/Cadastro"
import CreateProperty from "../pages/CreateProperty"

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/cadastro" element={<Cadastro />} />
      <Route path="/criar-imovel" element={<CreateProperty />} />
    </Routes>
  )
}