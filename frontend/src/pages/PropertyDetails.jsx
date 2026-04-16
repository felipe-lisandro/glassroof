import { useParams, Link } from "react-router-dom";

function PropertyDetails() {
  const { id } = useParams();

  // Dados mock (simulação)
const properties = [
  {
    id: "1",
    title: "Apartamento Centro",
    city: "São Paulo",
    state: "SP",
    description:
      "Apartamento moderno com excelente localização, próximo ao metrô, com segurança 24h e área de lazer completa.",
    price: "R$ 2.300/mês",
  },
  {
    id: "2",
    title: "Casa na Praia",
    city: "Santos",
    state: "SP",
    description:
      "Casa ampla com vista para o mar, garagem coberta e espaço gourmet.",
    price: "R$ 3.500/mês",
  },
  {
    id: "3",
    title: "Studio Universitário",
    city: "Campinas",
    state: "SP",
    description:
      "Studio compacto, ideal para estudantes e perto da faculdade.",
    price: "R$ 1.400/mês",
  },
];

  const property = properties.find((p) => p.id === id);

  if (!property) {
    return <h1 className="p-10">Imóvel não encontrado</h1>;
  }

  return (
    <main className="min-h-screen bg-gray-100 px-6 pt-28 pb-10">
      <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-md p-8">
        <h1 className="text-3xl font-bold mb-2">{property.title}</h1>

        <p className="text-gray-500 mb-4">
          {property.city} - {property.state}
        </p>

        <p className="text-lg font-semibold mb-4">{property.price}</p>

        <p className="text-gray-700 mb-6">{property.description}</p>

        <Link to="/imoveis">
          <button className="bg-black text-white px-5 py-2 rounded-lg hover:opacity-90 transition">
            Voltar
          </button>
        </Link>
      </div>
    </main>
  );
}

export default PropertyDetails;