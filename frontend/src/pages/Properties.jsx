function Properties() {
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
    <main className="min-h-screen bg-gray-100 px-6 pt-28 pb-10">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-2">Imóveis Disponíveis</h1>
        <p className="text-gray-600 mb-8">
          Explore os imóveis cadastrados na plataforma.
        </p>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {properties.map((property) => (
            <div
              key={property.id}
              className="bg-white rounded-2xl shadow-md p-6 border border-gray-200"
            >
              <h2 className="text-xl font-semibold mb-2">{property.title}</h2>

              <p className="text-gray-500 mb-2">
                {property.city} - {property.state}
              </p>

              <p className="text-gray-700 mb-3">{property.description}</p>

              <p className="font-bold mb-4">{property.price}</p>

              <button className="bg-black text-white px-4 py-2 rounded-lg hover:opacity-90 transition">
                Ver detalhes
              </button>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}

export default Properties;