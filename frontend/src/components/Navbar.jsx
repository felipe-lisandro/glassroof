import { NavLink } from "react-router-dom"

export default function Navbar() {

  return (
    <nav className="fixed z-50 w-full">
      <div className="flex items-center justify-between px-6 bg-surface border-b border-black h-16">
        <NavLink to='/' className="font-black text-3xl font-display uppercase ml-6 mt-2">
          <span className="text-white">Glass</span>
          <span className="text-blue-300">Roof</span>
        </NavLink>
        <div className="flex gap-15 h-full">
          <NavLink to='/imoveis' className={({ isActive }) =>
            `nav-link ${isActive ? "nav-link-active" : ""}`
          }>Imóveis</NavLink>
          <NavLink to='/imobiliarias' className={({ isActive }) =>
            `nav-link ${isActive ? "nav-link-active" : ""}`
          }>Imobiliárias</NavLink>
          <NavLink to='/sobre' className={({ isActive }) =>
            `nav-link ${isActive ? "nav-link-active" : ""}`
          }>Sobre nós</NavLink>
        </div>
        <NavLink to="/login" className="w-fit px-4 py-2 bg-blue-300 text-gray-900 font-bold text-xs rounded-md tracking-tight 
                                      hover:bg-blue-900 hover:text-black
                                        transition-all duration-300 ease-in-out">
          Entrar
        </NavLink>

      </div>
    </ nav>
  )
}