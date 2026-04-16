function MyProperties() {
  const properties = [
    {
      id: 1,
      title: "Apartamento Centro",
      city: "São Paulo",
      state: "SP",
      description: "Apartamento com ótima localização e segurança.",
    },
    {
      id: 2,
      title: "Casa na Praia",
      city: "Santos",
      state: "SP",
      description: "Casa ampla, próxima da praia e com garagem.",
    },
  ];

  return (
    <main className="min-h-screen bg-gray-100 px-6 pt-28 pb-10">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold mb-2">Meus Imóveis</h1>
        <p className="text-gray-600 mb-8">
          Aqui estão os imóveis cadastrados por você.
        </p>

        <div className="grid gap-6 md:grid-cols-2">
          {properties.map((property) => (
            <div
              key={property.id}
              className="bg-white rounded-2xl shadow-md p-6 border border-gray-200"
            >
              <h2 className="text-xl font-semibold mb-2">{property.title}</h2>
              <p className="text-gray-500 mb-2">
                {property.city} - {property.state}
              </p>
              <p className="text-gray-700 mb-4">{property.description}</p>

              <div className="flex gap-3">
                <button className="bg-black text-white px-4 py-2 rounded-lg hover:opacity-90 transition">
                  Ver detalhes
                </button>
                <button className="border border-black px-4 py-2 rounded-lg hover:bg-gray-100 transition">
                  Editar
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}

export default MyProperties;