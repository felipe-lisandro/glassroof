import { PropertyCard } from "../components/PropertyCard";

function Properties() {
  // Esse array será substituído pela chamada da API Flask em breve
  const properties = [
    {
      id: 1,
      title: "Apartamento Centro",
      city: "São Paulo",
      state: "SP",
      description: "Apartamento moderno, próximo ao metrô e com portaria 24h.",
      price: "R$ 2.300/mês",
    },
    {
      id: 2,
      title: "Casa na Praia",
      city: "Santos",
      state: "SP",
      description: "Casa espaçosa, perto da praia e com garagem coberta.",
      price: "R$ 3.500/mês",
    },
    {
      id: 3,
      title: "Studio Universitário",
      city: "Campinas",
      state: "SP",
      description: "Studio compacto, ideal para estudantes e perto da faculdade.",
      price: "R$ 1.400/mês",
    },
  ];

  return (
    <main className="min-h-screen bg-gray-50 px-6 pt-28 pb-10">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Imóveis Disponíveis</h1>
          <p className="text-gray-600">
            Explore os imóveis cadastrados na plataforma Glassroof.
          </p>
        </header>

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {properties.map((property) => (
            <PropertyCard key={property.id} {...property} />
          ))}
        </div>

        {properties.length === 0 && (
          <div className="text-center py-20">
            <p className="text-gray-500">Nenhum imóvel encontrado no momento.</p>
          </div>
        )}
      </div>
    </main>
  );
}

export default Properties;