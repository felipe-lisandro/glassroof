import { Link } from "react-router-dom";

export function PropertyCard({ id, title, city, state, description, price }) {
  return (
    <div className="bg-white rounded-2xl shadow-md p-6 border border-gray-200 flex flex-col justify-between hover:shadow-lg transition-shadow">
      <div>
        <h2 className="text-xl font-semibold mb-2 text-gray-800">{title}</h2>
        <p className="text-sm text-gray-500 mb-2">
          {city} - {state}
        </p>
        <p className="text-gray-600 mb-3 line-clamp-3 text-sm">
          {description}
        </p>
      </div>
      
      <div className="mt-4">
        <p className="font-bold text-lg text-gray-900 mb-4">{price}</p>
        <Link to={`/imovel/${id}`}>
          <button className="w-full bg-black text-white px-4 py-2 rounded-lg hover:bg-gray-800 transition-colors font-medium">
            Ver detalhes
          </button>
        </Link>
      </div>
    </div>
  );
}