import { Link } from "react-router-dom";

export function PropertyCard({
  id,
  title,
  city,
  state,
  description,
  price,
  imageUrl,
  overallRating,
}) {
  return (
    <div className="bg-white rounded-2xl shadow-md overflow-hidden border border-gray-200 flex flex-col">
      <img 
        src={imageUrl || "https://via.placeholder.com/400x250?text=Sem+Foto"} 
        alt={title}
        className="w-full h-48 object-cover"
      />
      <div className="p-6 flex flex-col grow">
        <h2 className="text-xl font-semibold mb-1">{title}</h2>
        <p className="text-gray-500 text-sm mb-3">{city} - {state}</p>
        <p className="text-gray-600 text-sm line-clamp-2 mb-4 grow">{description}</p>
        <div className="flex items-center gap-2 mb-3" aria-label="Nota geral do imóvel">
          {overallRating !== null && overallRating !== undefined ? (
            <>
              <span className="text-amber-500" aria-hidden="true">★</span>
              <span className="font-semibold text-gray-900">
                {Number(overallRating).toFixed(1)} / 5
              </span>
            </>
          ) : (
            <span className="text-sm text-gray-500">Sem avaliações</span>
          )}
        </div>
        <p className="font-bold text-lg mb-4">{price}</p>
        
        <Link to={`/imovel/${id}`}>
          <button className="w-full bg-black text-white py-2 rounded-lg hover:opacity-90 transition">
            Ver detalhes
          </button>
        </Link>
      </div>
    </div>
  );
}