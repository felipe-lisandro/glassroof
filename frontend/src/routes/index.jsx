import { Routes, Route } from "react-router-dom"
import Home from "../pages/Home"
import Login from "../pages/Login"
import Cadastro from "../pages/Cadastro"
import CreateProperty from "../pages/CreateProperty"
import MyProperties from "../pages/MyProperties"
import Properties from "../pages/Properties"
import PropertyDetails from "../pages/PropertyDetails";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/cadastro" element={<Cadastro />} />
      <Route path="/criar-imovel" element={<CreateProperty />} />
      <Route path="/meus-imoveis" element={<MyProperties />} />
      <Route path="/imoveis" element={<Properties />} />
      <Route path="/imovel/:id" element={<PropertyDetails />} />
    </Routes>
  )
}