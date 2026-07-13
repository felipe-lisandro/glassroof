import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import {
  deletePropertyAvaliation,
  getPropertyAvaliations,
  getPropertyById,
  updatePropertyAvaliation,
} from "../services/propertyService";
import { useAuth } from "../contexts/AuthContext";

function PropertyDetails() {
  const { id } = useParams();
  const { user, token } = useAuth();
  const [property, setProperty] = useState(null);
  const [avaliations, setAvaliations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionError, setActionError] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({ comment: "", stars: "" });

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
        const [propertyData, avaliationsData] = await Promise.all([
          getPropertyById(propertyId),
          getPropertyAvaliations(propertyId),
        ]);

        setProperty(propertyData);
        setAvaliations(Array.isArray(avaliationsData) ? avaliationsData : []);
        setError(null);
      } catch (err) {

        setError("Imóvel não encontrado em nossa base de dados.");
      } finally {
        setLoading(false);
      }
    }

    loadProperty();
  }, [id]);

  const averageRating =
    avaliations.length > 0
      ? (avaliations.reduce((sum, item) => sum + Number(item.stars || 0), 0) / avaliations.length).toFixed(1)
      : null;

  const sortedAvaliations = [...avaliations].sort((a, b) => {
    const isAFromCurrentUser = a.user_id === user?.id;
    const isBFromCurrentUser = b.user_id === user?.id;

    if (isAFromCurrentUser && !isBFromCurrentUser) return -1;
    if (!isAFromCurrentUser && isBFromCurrentUser) return 1;

    const dateA = new Date(a.created_at || 0).getTime();
    const dateB = new Date(b.created_at || 0).getTime();
    return dateB - dateA;
  });

  const avaliationsByCategory = Object.entries(
    sortedAvaliations.reduce((acc, item) => {
      const categoryName = item.category_name || "Sem categoria";
      if (!acc[categoryName]) {
        acc[categoryName] = [];
      }
      acc[categoryName].push(item);
      return acc;
    }, {})
  )
    .map(([categoryName, items]) => {
      const categoryAverage =
        items.reduce((sum, current) => sum + Number(current.stars || 0), 0) / items.length;
      return {
        categoryName,
        items,
        average: categoryAverage,
      };
    })
    .sort((a, b) => a.categoryName.localeCompare(b.categoryName));

  function renderStars(value) {
    const rating = Math.max(0, Math.min(5, Number(value) || 0));
    const widthPercent = `${(rating / 5) * 100}%`;
    return (
      <span className="relative inline-block text-lg leading-none" aria-label={`${rating.toFixed(1)} de 5 estrelas`}>
        <span className="text-gray-300 tracking-wide">{"★★★★★"}</span>
        <span
          className="absolute left-0 top-0 overflow-hidden text-amber-500 tracking-wide"
          style={{ width: widthPercent }}
          aria-hidden="true"
        >
          {"★★★★★"}
        </span>
      </span>
    );
  }

  function startEditing(item) {
    setActionError(null);
    setEditingId(item.id);
    setEditForm({
      comment: item.comment || "",
      stars: String(Number(item.stars || 0)),
    });
  }

  function cancelEditing() {
    setEditingId(null);
    setEditForm({ comment: "", stars: "" });
  }

  async function handleSaveEdit(item) {
    if (!token) {
      setActionError("Você precisa estar logado para editar avaliações.");
      return;
    }

    const stars = Number(editForm.stars);
    if (!editForm.comment.trim() || Number.isNaN(stars) || stars < 0 || stars > 5) {
      setActionError("Informe comentário e nota válida de 0 a 5.");
      return;
    }

    try {
      setActionError(null);
      const updated = await updatePropertyAvaliation(
        property.id,
        item.id,
        {
          comment: editForm.comment.trim(),
          stars,
          photos: item.photos || [],
        },
        token
      );

      setAvaliations((previous) =>
        previous.map((current) => (current.id === item.id ? { ...current, ...updated } : current))
      );
      cancelEditing();
    } catch (err) {
      setActionError(err?.error || "Falha ao atualizar avaliação.");
    }
  }

  async function handleDelete(item) {
    if (!token) {
      setActionError("Você precisa estar logado para excluir avaliações.");
      return;
    }

    try {
      setActionError(null);
      await deletePropertyAvaliation(property.id, item.id, token);
      setAvaliations((previous) => previous.filter((current) => current.id !== item.id));
      if (editingId === item.id) {
        cancelEditing();
      }
    } catch (err) {
      setActionError(err?.error || "Falha ao excluir avaliação.");
    }
  }

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

          <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
            <h2 className="text-2xl font-semibold">Descrição</h2>
            <div className="flex items-center gap-3">
              <span className="text-base text-gray-500">Média da propriedade:</span>
              <span className="text-xl font-bold text-black">
                {averageRating !== null ? `${averageRating} / 5` : "Sem avaliações"}
              </span>
              {averageRating !== null && renderStars(averageRating)}
            </div>
          </div>
          <p className="text-gray-700 leading-relaxed mb-8 text-lg">
            {property.description}
          </p>

          <hr className="my-6" />

          <div className="mb-8">
            <h2 className="text-2xl font-semibold mb-4">Avaliações</h2>
            {actionError && <p className="text-red-500 mb-3">{actionError}</p>}
            <div className="flex items-center gap-3 mb-4">
              <span className="text-base text-gray-500">Nota final:</span>
              <span className="text-2xl font-bold text-black">
                {averageRating !== null ? `${averageRating} / 5` : "Sem avaliações"}
              </span>
              {averageRating !== null && renderStars(averageRating)}
              {avaliations.length > 0 && (
                <span className="text-sm text-gray-500">({avaliations.length} avaliações)</span>
              )}
            </div>

            {avaliations.length === 0 ? (
              <p className="text-gray-600">Este imóvel ainda não possui avaliações.</p>
            ) : (
              <div className="space-y-6">
                {avaliationsByCategory.map((categoryGroup) => (
                  <div key={categoryGroup.categoryName} className="border border-gray-200 rounded-xl p-4 bg-gray-50">
                    <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
                      <h3 className="text-lg font-semibold text-gray-900">{categoryGroup.categoryName}</h3>
                      <div className="flex items-center gap-2">
                        <span className="text-sm text-gray-600">Média da categoria:</span>
                        <span className="font-semibold text-black">{categoryGroup.average.toFixed(1)}/5</span>
                        {renderStars(categoryGroup.average)}
                      </div>
                    </div>

                    <div className="space-y-3">
                      {categoryGroup.items.map((item) => (
                        <div key={item.id} className="bg-white border border-gray-100 rounded-lg p-3">
                          <div className="flex items-center justify-between mb-2">
                            <span className="font-semibold text-gray-900">Avaliação anônima</span>
                            <div className="flex items-center gap-2">
                              {renderStars(item.stars)}
                              <span className="text-sm text-gray-600">{Number(item.stars || 0)}/5</span>
                            </div>
                          </div>

                          {editingId === item.id ? (
                            <div className="space-y-3">
                              <div>
                                <label className="text-sm text-gray-700">Nota (0 a 5)</label>
                                <select
                                  className="mt-1 w-full border border-gray-300 rounded-lg px-3 py-2"
                                  value={editForm.stars}
                                  onChange={(event) =>
                                    setEditForm((prev) => ({ ...prev, stars: event.target.value }))
                                  }
                                >
                                  {[0, 1, 2, 3, 4, 5].map((value) => (
                                    <option key={value} value={value}>
                                      {value}
                                    </option>
                                  ))}
                                </select>
                              </div>
                              <div>
                                <label className="text-sm text-gray-700">Comentário</label>
                                <textarea
                                  className="mt-1 w-full border border-gray-300 rounded-lg px-3 py-2 min-h-24"
                                  value={editForm.comment}
                                  onChange={(event) =>
                                    setEditForm((prev) => ({ ...prev, comment: event.target.value }))
                                  }
                                  maxLength={500}
                                />
                              </div>
                              <div className="flex gap-2">
                                <button
                                  className="bg-black text-white px-4 py-2 rounded-lg hover:opacity-90 transition"
                                  onClick={() => handleSaveEdit(item)}
                                  type="button"
                                >
                                  Salvar
                                </button>
                                <button
                                  className="border border-black text-black px-4 py-2 rounded-lg hover:bg-gray-100 transition"
                                  onClick={cancelEditing}
                                  type="button"
                                >
                                  Cancelar
                                </button>
                              </div>
                            </div>
                          ) : (
                            <>
                              <p className="text-gray-700">{item.comment}</p>
                              {user?.id === item.user_id && (
                                <div className="mt-3 flex gap-2">
                                  <button
                                    className="text-sm border border-black text-black px-3 py-1 rounded hover:bg-gray-100 transition"
                                    onClick={() => startEditing(item)}
                                    type="button"
                                  >
                                    Editar
                                  </button>
                                  <button
                                    className="text-sm border border-red-600 text-red-600 px-3 py-1 rounded hover:bg-red-50 transition"
                                    onClick={() => handleDelete(item)}
                                    type="button"
                                  >
                                    Excluir
                                  </button>
                                </div>
                              )}
                            </>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="flex gap-4">
            <Link to="/imoveis">
              <button className="border border-black text-black px-6 py-2 rounded-lg hover:bg-gray-100 transition">
                Voltar
              </button>
            </Link>
            <Link to={`/imovel/${property.id}/avaliar`}>
              <button className="bg-black text-white px-6 py-2 rounded-lg hover:opacity-90 transition">
                Criar Avaliação
              </button>
            </Link>
            <Link to={`/imovel/${property.id}/agendar`}>
              <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition">
                Agendar Visita
              </button>
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}

export default PropertyDetails;