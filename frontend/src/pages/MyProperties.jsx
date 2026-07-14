import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { getPropertiesByEnterprise } from "../services/propertyService";

function MyProperties() {
  const { user } = useAuth();
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchMyProperties() {
      if (!user?.id) return;
      
      try {
        setLoading(true);
        const data = await getPropertiesByEnterprise(user.id);
        setProperties(data);
      } catch (err) {
        setError("Não foi possível carregar seus imóveis.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    fetchMyProperties();
  }, [user?.id]);

  if (loading) return <div className="text-center pt-40">Carregando seus imóveis...</div>;

  return (
    <main className="min-h-screen bg-gray-100 px-6 pt-28 pb-10">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-2">
          <h1 className="text-3xl font-bold">Meus Imóveis</h1>
          <Link to="/criar-imovel">
            <button className="bg-blue-600 text-white px-4 py-2 rounded-lg font-bold hover:bg-blue-700 transition">
              + Novo Imóvel
            </button>
          </Link>
        </div>
        <p className="text-gray-600 mb-8">
          Gerencie os anúncios da imobiliária {user?.name}.
        </p>

        {error && <p className="text-red-500 mb-4">{error}</p>}

        {properties.length === 0 ? (
          <div className="bg-white rounded-2xl p-10 text-center shadow-md">
            <p className="text-gray-500">Você ainda não possui imóveis cadastrados.</p>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {properties.map((property) => (
              <div
                key={property.id}
                className="bg-white rounded-2xl shadow-md overflow-hidden border border-gray-200 flex flex-col"
              >
                {/* Imagem do Imóvel */}
                <div className="relative h-48 w-full bg-gray-200">
                  <img
                    src={property.images?.[0]?.URL || "https://via.placeholder.com/400x250?text=Sem+Foto"}
                    alt={property.name}
                    className="w-full h-full object-cover"
                  />
                  <span className="absolute top-2 right-2 bg-black/60 text-white text-[10px] font-bold px-2 py-1 rounded backdrop-blur-sm">
                    ID: {property.id}
                  </span>
                </div>

                <div className="p-6 flex flex-col grow">
                  <div className="mb-4">
                    <h2 className="text-xl font-semibold mb-1 truncate">{property.name}</h2>
                    <p className="text-gray-500 text-sm">
                      {property.location?.city} - {property.location?.state}
                    </p>
                  </div>

                  <p className="text-gray-700 text-sm line-clamp-2 mb-4 grow">
                    {property.description}
                  </p>

                  <p className="font-bold text-lg mb-4">
                    R$ {Number(property.price).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                  </p>

                  <div className="flex gap-3 mt-auto">
                    <Link to={`/imovel/${property.id}`} className="flex-1">
                      <button className="w-full bg-black text-white py-2 rounded-lg hover:opacity-90 transition text-xs font-bold uppercase">
                        Ver
                      </button>
                    </Link>
                    <Link to={`/editar-imovel/${property.id}`} className="flex-1">
                      <button className="w-full border border-black py-2 rounded-lg hover:bg-gray-100 transition text-xs font-bold uppercase">
                        Editar
                      </button>
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}

export default MyProperties;