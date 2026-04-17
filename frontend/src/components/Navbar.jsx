import { useState, useRef, useEffect } from "react";
import { NavLink, useNavigate, Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();
  const dropdownRef = useRef(null);

  // Fecha o dropdown se clicar fora dele
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  function handleLogout() {
    setIsOpen(false);
    logout();
    navigate("/");
  }

  return (
    <nav className="fixed z-50 w-full">
      <div className="flex items-center justify-between px-6 bg-surface border-b border-black h-16">
        <NavLink to="/" className="font-black text-3xl font-display uppercase ml-6 mt-2">
          <span className="text-white">Glass</span>
          <span className="text-blue-300">Roof</span>
        </NavLink>

        <div className="flex gap-15 h-full">
          <NavLink to="/imoveis" className={({ isActive }) => `nav-link ${isActive ? "nav-link-active" : ""}`}>
            Imóveis
          </NavLink>
          <NavLink to="/imobiliarias" className={({ isActive }) => `nav-link ${isActive ? "nav-link-active" : ""}`}>
            Imobiliárias
          </NavLink>
          <NavLink to="/sobre" className={({ isActive }) => `nav-link ${isActive ? "nav-link-active" : ""}`}>
            Sobre nós
          </NavLink>
        </div>

        {isAuthenticated ? (
          <div className="relative" ref={dropdownRef}>
            {/* Botão do Usuário */}
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="flex items-center gap-2 px-4 py-2 bg-zinc-800 text-white rounded-md hover:bg-zinc-700 transition-all border border-zinc-600"
            >
              <span className="text-xs font-bold uppercase tracking-wider">{user?.name}</span>
              <svg 
                className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} 
                fill="none" stroke="currentColor" viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            {/* Menu Dropdown */}
            {isOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-zinc-900 border border-zinc-700 rounded-lg shadow-xl py-2 overflow-hidden animate-in fade-in zoom-in duration-200">
                
                <div className="px-4 py-2 border-b border-zinc-800">
                  <p className="text-[10px] text-zinc-500 font-bold uppercase">Logado como</p>
                  <p className="text-xs text-white truncate font-medium">{user?.email}</p>
                </div>

                {/* Opção exclusiva para Imobiliária */}
                {user?.type === "enterprise" && (
                  <Link
                    to="/meus-imoveis"
                    onClick={() => setIsOpen(false)}
                    className="block px-4 py-2 text-sm text-blue-300 hover:bg-zinc-800 transition-colors"
                  >
                    Meus Imóveis
                  </Link>
                )}

                <button
                  onClick={handleLogout}
                  className="w-full text-left px-4 py-2 text-sm text-red-400 hover:bg-zinc-800 transition-colors"
                >
                  Sair
                </button>
              </div>
            )}
          </div>
        ) : (
          <NavLink
            to="/login"
            className="w-fit px-4 py-2 bg-blue-300 text-gray-900 font-bold text-xs rounded-md tracking-tight
                       hover:bg-blue-400 transition-all duration-300 ease-in-out"
          >
            Entrar
          </NavLink>
        )}
      </div>
    </nav>
  );
}