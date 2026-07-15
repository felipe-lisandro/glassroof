import { NavLink } from "react-router-dom";


export default function Hero() {
  return (
    <div className="text-center flex flex-col items-center justify-center h-screen w-full bg-linear-to-b from-background via-background to-blue-900/10 gap-5">
        <h1 className="text-5xl font-bold text-white px-50">Saiba onde você vai morar antes de assinar.</h1>
        <p className="text-lg font-extralight px-90 text-zinc-600">A primeira plataforma de avaliações reais e anônimas de repúblicas, kitnets e apartamentos feita por estudantes, para estudantes.</p>

    </div>
  );
}