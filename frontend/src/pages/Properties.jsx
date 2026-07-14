import { useState, useEffect } from "react";
import { PropertyCard } from "../components/PropertyCard";
import { getProperties } from "../services/propertyService";

function Properties() {
  const [properties, setProperties] = useState([]);
  const [pagination, setPagination] = useState({ page: 1, pages: 0, total: 0 });
  const [filters, setFilters] = useState({
    min_price: "",
    max_price: "",
    city: "",
    min_rating: "",
    sort_by: "id",
    sort_order: "asc",
  });
  const [appliedFilters, setAppliedFilters] = useState(filters);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const data = await getProperties({
          ...appliedFilters,
          page: pagination.page,
          per_page: 9,
        });
        setProperties(data.items || []);
        setPagination((previous) => ({
          ...previous,
          page: data.page,
          pages: data.pages,
          total: data.total,
        }));
      } catch (err) {
        console.error("Erro ao buscar imóveis:", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [appliedFilters, pagination.page]);

  function updateFilter(event) {
    const { name, value } = event.target;
    setFilters((previous) => ({ ...previous, [name]: value }));
  }

  function applyFilters(event) {
    event.preventDefault();
    setPagination((previous) => ({ ...previous, page: 1 }));
    setAppliedFilters(filters);
  }

  function clearFilters() {
    const cleared = {
      min_price: "",
      max_price: "",
      city: "",
      min_rating: "",
      sort_by: "id",
      sort_order: "asc",
    };
    setFilters(cleared);
    setAppliedFilters(cleared);
    setPagination((previous) => ({ ...previous, page: 1 }));
  }

  if (loading) return <div className="text-center pt-40">Carregando imóveis do banco...</div>;

  return (
    <main className="min-h-screen bg-gray-50 px-6 pt-28 pb-10">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Imóveis Disponíveis</h1>

        <form onSubmit={applyFilters} className="bg-white rounded-2xl shadow-md p-5 mb-8">
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <input
              name="min_price"
              type="number"
              min="0"
              placeholder="Preço mínimo"
              value={filters.min_price}
              onChange={updateFilter}
              className="border border-gray-300 rounded-lg px-3 py-2"
            />
            <input
              name="max_price"
              type="number"
              min="0"
              placeholder="Preço máximo"
              value={filters.max_price}
              onChange={updateFilter}
              className="border border-gray-300 rounded-lg px-3 py-2"
            />
            <input
              name="city"
              type="text"
              placeholder="Cidade"
              value={filters.city}
              onChange={updateFilter}
              className="border border-gray-300 rounded-lg px-3 py-2"
            />
            <select
              name="min_rating"
              value={filters.min_rating}
              onChange={updateFilter}
              className="border border-gray-300 rounded-lg px-3 py-2 bg-white"
            >
              <option value="">Nota mínima</option>
              {[1, 2, 3, 4, 5].map((rating) => (
                <option key={rating} value={rating}>{rating} estrelas ou mais</option>
              ))}
            </select>
            <select
              name="sort_by"
              value={filters.sort_by}
              onChange={updateFilter}
              className="border border-gray-300 rounded-lg px-3 py-2 bg-white"
            >
              <option value="id">Mais recentes</option>
              <option value="price">Preço</option>
              <option value="rating">Nota</option>
            </select>
            <select
              name="sort_order"
              value={filters.sort_order}
              onChange={updateFilter}
              className="border border-gray-300 rounded-lg px-3 py-2 bg-white"
            >
              <option value="asc">Crescente</option>
              <option value="desc">Decrescente</option>
            </select>
            <div className="flex gap-2 sm:col-span-2">
              <button type="submit" className="bg-black text-white px-5 py-2 rounded-lg hover:opacity-90 transition">
                Buscar
              </button>
              <button type="button" onClick={clearFilters} className="border border-black px-5 py-2 rounded-lg hover:bg-gray-100 transition">
                Limpar
              </button>
            </div>
          </div>
        </form>

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
              overallRating={prop.overall_rating}
            />
          ))}
        </div>
        
        {properties.length === 0 && (
          <p className="text-center text-gray-500 mt-10">Nenhum imóvel encontrado no banco de dados.</p>
        )}

        {pagination.pages > 1 && (
          <div className="flex items-center justify-center gap-4 mt-8">
            <button
              type="button"
              disabled={pagination.page <= 1}
              onClick={() => setPagination((previous) => ({ ...previous, page: previous.page - 1 }))}
              className="border border-black px-4 py-2 rounded-lg disabled:opacity-40"
            >
              Anterior
            </button>
            <span className="text-sm text-gray-600">
              Página {pagination.page} de {pagination.pages}
            </span>
            <button
              type="button"
              disabled={pagination.page >= pagination.pages}
              onClick={() => setPagination((previous) => ({ ...previous, page: previous.page + 1 }))}
              className="border border-black px-4 py-2 rounded-lg disabled:opacity-40"
            >
              Próxima
            </button>
          </div>
        )}
      </div>
    </main>
  );
}

export default Properties;