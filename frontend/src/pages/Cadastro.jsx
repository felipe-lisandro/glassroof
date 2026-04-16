import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerPerson } from "../services/api";

function Cadastro() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    cpf: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await registerPerson(form);
      navigate("/login", { state: { registered: true } });
    } catch (err) {
      if (err.errors) {
        const firstField = Object.keys(err.errors)[0];
        setError(err.errors[firstField][0]);
      } else if (err.error) {
        setError(err.error);
      } else {
        setError("Erro ao cadastrar. Tente novamente.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <div className="w-full max-w-md bg-white p-8 rounded-xl shadow-md">
        <h1 className="text-3xl font-bold text-center mb-2">Cadastro</h1>
        <p className="text-center text-gray-500 mb-6">
          Crie sua conta para avaliar imóveis
        </p>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="text"
            name="name"
            placeholder="Nome"
            value={form.name}
            onChange={handleChange}
            required
            className="p-3 border border-gray-300 rounded-lg"
          />
          <input
            type="text"
            name="cpf"
            placeholder="CPF (somente números)"
            value={form.cpf}
            onChange={handleChange}
            maxLength={11}
            required
            className="p-3 border border-gray-300 rounded-lg"
          />
          <input
            type="email"
            name="email"
            placeholder="E-mail"
            value={form.email}
            onChange={handleChange}
            required
            className="p-3 border border-gray-300 rounded-lg"
          />
          <input
            type="password"
            name="password"
            placeholder="Senha (mínimo 6 caracteres)"
            value={form.password}
            onChange={handleChange}
            minLength={6}
            required
            className="p-3 border border-gray-300 rounded-lg"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-black text-white p-3 rounded-lg hover:opacity-90 transition disabled:opacity-50"
          >
            {loading ? "Cadastrando..." : "Cadastrar"}
          </button>
        </form>

        <p className="text-sm text-center mt-4">
          Já possui conta?{" "}
          <Link to="/login" className="text-blue-600 hover:underline">
            Fazer login
          </Link>
        </p>
      </div>
    </main>
  );
}

export default Cadastro;
