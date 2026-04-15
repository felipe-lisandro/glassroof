import { Link } from "react-router-dom";

function Login() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <div className="w-full max-w-md bg-white p-8 rounded-xl shadow-md">
        <h1 className="text-3xl font-bold text-center mb-2">Login</h1>
        <p className="text-center text-gray-500 mb-6">
          Entre para acessar sua conta
        </p>

        <form className="flex flex-col gap-4">
          <input
            type="email"
            placeholder="E-mail"
            className="p-3 border border-gray-300 rounded-lg"
          />
          <input
            type="password"
            placeholder="Senha"
            className="p-3 border border-gray-300 rounded-lg"
          />
          <button
            type="submit"
            className="bg-black text-white p-3 rounded-lg hover:opacity-90 transition"
          >
            Entrar
          </button>
        </form>

        <p className="text-sm text-center mt-4">
          Ainda não tem conta?{" "}
          <Link to="/cadastro" className="text-blue-600 hover:underline">
            Cadastre-se
          </Link>
        </p>
      </div>
    </main>
  );
}

export default Login;