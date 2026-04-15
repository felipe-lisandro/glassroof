import { NavLink } from "react-router-dom";


export default function Hero() {
  return (
    <div className="text-center flex flex-col items-center justify-center h-screen w-full bg-linear-to-b from-background via-background to-blue-900/10 gap-5">
        <h1 className="text-5xl font-bold text-white px-50">Saiba onde você vai morar antes de assinar.</h1>
        <p className="text-lg font-extralight px-90 text-zinc-600">A primeira plataforma de avaliações reais e anônimas de repúblicas, kitnets e apartamentos feita por estudantes, para estudantes.</p>
        <NavLink to="/avaliacoes" className="px-6 py-3 bg-blue-300 text-gray-900 font-bold text-sm rounded-md tracking-tight hover:bg-blue-900 hover:text-black transition-all duration-300 ease-in-out">
          Ver avaliações
        </NavLink>
    </div>
  );
}