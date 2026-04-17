import { useState, useEffect } from "react";
import { PropertyCard } from "../components/PropertyCard";
import { getProperties } from "../services/propertyService";

function Properties() {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getProperties();
        setProperties(data); // O backend retorna a lista de to_dict() do property.py
      } catch (err) {
        console.error("Erro ao buscar imóveis:", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) return <div className="text-center pt-40">Carregando imóveis do banco...</div>;

  return (
    <main className="min-h-screen bg-gray-50 px-6 pt-28 pb-10">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Imóveis Disponíveis</h1>

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {properties.map((prop) => (
            <PropertyCard 
              key={prop.id}
              id={prop.id}
              title={prop.name} // Mapeando 'name' do back para 'title' do front
              city={prop.location?.city} 
              state={prop.location?.state}
              description={prop.description}
              price={`R$ ${prop.price}`}
              imageUrl={prop.images?.[0]?.URL} // Pega a primeira imagem da lista
            />
          ))}
        </div>
        
        {properties.length === 0 && (
          <p className="text-center text-gray-500 mt-10">Nenhum imóvel encontrado no banco de dados.</p>
        )}
      </div>
    </main>
  );
}

export default Properties;