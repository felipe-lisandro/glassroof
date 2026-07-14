import { useState } from "react";
import { useAuth } from "../contexts/AuthContext"; // Para pegar o enterprise_id automaticamente
import { createProperty } from "../services/propertyService";

function CreateProperty() {
  const { token, user } = useAuth(); // Puxa os dados do usuário logado
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  // Estado inicial seguindo a estrutura do seu Backend (Flask)
  const [form, setForm] = useState({
    name: "",
    description: "",
    price: "",
    location: {
      street: "",
      number: "",
      CEP: "",
      city: "",
      state: "",
      country: "Brasil",
      complement: ""
    },
    images: [
      {
        URL: "",
        order: 1,
        size_mb: 2,
        description: "Foto principal"
      }
    ]
  });

  // Função para atualizar campos aninhados (Location e Images)
  const handleChange = (e, section, field) => {
    const value = e.target.value;
    if (section) {
      setForm((prev) => ({
        ...prev,
        [section]: section === "images" 
          ? [{ ...prev.images[0], [field]: value }] // Atualiza a primeira imagem
          : { ...prev[section], [field]: value }    // Atualiza localização
      }));
    } else {
      setForm((prev) => ({ ...prev, [e.target.name]: value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // Montamos o objeto final injetando o enterprise_id do contexto
      const payload = {
        ...form,
        price: parseFloat(form.price), // Garante que é número para o Flask
        enterprise_id: user.id,
        location: {
          ...form.location,
          number: parseInt(form.location.number) // Garante que é inteiro
        }
      };

      await createProperty(payload, token);
      setMessage("Imóvel cadastrado com sucesso!");
      // Opcional: redirecionar para /properties
    } catch (err) {
      setMessage("Erro ao cadastrar. Verifique os dados.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-100 px-4 py-20">
      <div className="w-full max-w-2xl bg-white rounded-2xl shadow-md p-8">
        <h1 className="text-3xl font-bold mb-2">Cadastro de Imóvel</h1>
        <p className="text-gray-500 mb-6">Preencha os dados conforme o padrão do sistema.</p>

        {message && <p className="mb-4 text-blue-600 font-medium">{message}</p>}

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            name="name"
            type="text"
            placeholder="Título do imóvel (ex: Apto Barão Geraldo)"
            className="p-3 border rounded-lg"
            onChange={(e) => handleChange(e)}
            required
          />

          <div className="grid grid-cols-2 gap-4">
            <input
              type="number"
              placeholder="Preço (R$)"
              className="p-3 border rounded-lg"
              onChange={(e) => setForm({...form, price: e.target.value})}
              required
            />
            <input
              type="text"
              placeholder="CEP (00000-000)"
              className="p-3 border rounded-lg"
              onChange={(e) => handleChange(e, "location", "CEP")}
              required
            />
          </div>

          <div className="grid grid-cols-3 gap-4">
            <input
              className="col-span-2 p-3 border rounded-lg"
              placeholder="Rua"
              onChange={(e) => handleChange(e, "location", "street")}
              required
            />
            <input
              className="p-3 border rounded-lg"
              placeholder="Nº"
              onChange={(e) => handleChange(e, "location", "number")}
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <input
              className="p-3 border rounded-lg"
              placeholder="Cidade"
              onChange={(e) => handleChange(e, "location", "city")}
              required
            />
            <input
              className="p-3 border rounded-lg"
              placeholder="Estado (ex: SP)"
              onChange={(e) => handleChange(e, "location", "state")}
              required
            />
          </div>

          <input
            type="text"
            placeholder="Link da imagem (URL)"
            className="p-3 border rounded-lg text-blue-600"
            onChange={(e) => handleChange(e, "images", "URL")}
            required
          />

          <textarea
            name="description"
            placeholder="Descrição completa..."
            rows="4"
            className="p-3 border rounded-lg"
            onChange={(e) => handleChange(e)}
            required
          ></textarea>

          <button
            type="submit"
            disabled={loading}
            className="bg-black text-white p-3 rounded-lg hover:opacity-90 transition disabled:bg-gray-400"
          >
            {loading ? "Salvando no banco..." : "Cadastrar Imóvel"}
          </button>
        </form>
      </div>
    </main>
  );
}

export default CreateProperty;