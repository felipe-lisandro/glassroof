import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { getPropertyById } from "../services/propertyService";

function PropertyDetails() {
  const { id } = useParams();
  const [property, setProperty] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    
      if (!id || isNaN(Number(id))) {
      setError("ID de imóvel inválido.");
      setLoading(false);
      return;
    }

    async function loadProperty() {
      try {
        setLoading(true);

        const propertyId = Number(id);
        const data = await getPropertyById(propertyId);
        
        setProperty(data);
        setError(null);
      } catch (err) {

        setError("Imóvel não encontrado em nossa base de dados.");
      } finally {
        setLoading(false);
      }
    }

    loadProperty();
  }, [id]);

  if (loading) return <div className="text-center pt-40">Carregando detalhes...</div>;
  
  if (error || !property) {
    return (
      <div className="text-center pt-40">
        <p className="text-red-500 mb-4">{error || "Imóvel não encontrado"}</p>
        <Link to="/imoveis" className="text-blue-600 underline">Voltar para a listagem</Link>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 px-6 pt-28 pb-10">
      <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-lg overflow-hidden">
        
        {property.images && property.images.length > 0 && (
          <img 
            src={property.images[0].URL} 
            alt={property.name} 
            className="w-full h-96 object-cover"
          />
        )}

        <div className="p-8">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">{property.name}</h1>
              <p className="text-xl text-gray-500">
                {property.location?.street}, {property.location?.number} — {property.location?.city}, {property.location?.state}
              </p>
            </div>
            <p className="text-3xl font-bold text-black">
              R$ {Number(property.price).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
            </p>
          </div>

          <hr className="my-6" />

          <h2 className="text-2xl font-semibold mb-4">Descrição</h2>
          <p className="text-gray-700 leading-relaxed mb-8 text-lg">
            {property.description}
          </p>

          <div className="flex gap-4">
            <Link to="/imoveis">
              <button className="border border-black text-black px-6 py-2 rounded-lg hover:bg-gray-100 transition">
                Voltar
              </button>
            </Link>
            
            <button className="bg-black text-white px-6 py-2 rounded-lg hover:opacity-90 transition">
              Avaliar Imóvel
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}

export default PropertyDetails;