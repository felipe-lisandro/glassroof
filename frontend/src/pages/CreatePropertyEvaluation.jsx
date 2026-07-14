import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  createPropertyAvaliationsBulk,
  getAvaliationCategories,
  getPropertyAvaliations,
  getPropertyById,
} from "../services/propertyService";
import { useAuth } from "../contexts/AuthContext";

function CreatePropertyEvaluation() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();

  const [property, setProperty] = useState(null);
  const [categories, setCategories] = useState([]);
  const [formByCategory, setFormByCategory] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!id || Number.isNaN(Number(id))) {
      setError("ID de imóvel inválido.");
      setLoading(false);
      return;
    }

    async function loadData() {
      try {
        setLoading(true);
        const propertyId = Number(id);
        const [propertyData, categoriesData, avaliationsData] = await Promise.all([
          getPropertyById(propertyId),
          getAvaliationCategories(),
          getPropertyAvaliations(propertyId),
        ]);

        const alreadyReviewed = (Array.isArray(avaliationsData) ? avaliationsData : []).some(
          (item) => item.user_id === user?.id
        );
        if (alreadyReviewed) {
          setError("Você já avaliou este imóvel e não pode criar nova avaliação.");
          setProperty(propertyData);
          setCategories([]);
          return;
        }

        const normalizedCategories = Array.isArray(categoriesData) ? categoriesData : [];
        const initialForm = {};
        normalizedCategories.forEach((category) => {
          initialForm[category.id] = { stars: "", comment: "" };
        });

        setProperty(propertyData);
        setCategories(normalizedCategories);
        setFormByCategory(initialForm);
        setError(null);
      } catch (err) {
        setError("Não foi possível carregar os dados para avaliação.");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [id]);

  function updateField(categoryId, field, value) {
    setFormByCategory((previous) => ({
      ...previous,
      [categoryId]: {
        ...previous[categoryId],
        [field]: value,
      },
    }));
  }

  function hasInvalidCategories() {
    return categories.some((category) => {
      const item = formByCategory[category.id] || { stars: "", comment: "" };
      const stars = Number(item.stars);
      return Number.isNaN(stars) || stars < 0 || stars > 5 || !item.comment?.trim();
    });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (!property) {
      return;
    }

    if (!isAuthenticated || !user?.id) {
      setError("Você precisa estar logado para enviar avaliações.");
      return;
    }

    if (hasInvalidCategories()) {
      setError("Você precisa informar nota e comentário para todas as categorias.");
      return;
    }

    try {
      setSubmitting(true);
      setError(null);

      await createPropertyAvaliationsBulk(property.id, {
        user_id: user.id,
        avaliations: categories.map((category) => {
          const item = formByCategory[category.id];
          return {
            category_id: category.id,
            stars: Number(item.stars),
            comment: item.comment.trim(),
            photos: [],
          };
        }),
      });

      navigate(`/imovel/${property.id}`);
    } catch (err) {
      setError("Falha ao enviar avaliações. Tente novamente.");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return <div className="text-center pt-40">Carregando formulário de avaliação...</div>;
  }

  if (error && !property) {
    return (
      <div className="text-center pt-40">
        <p className="text-red-500 mb-4">{error}</p>
        <Link to="/imoveis" className="text-blue-600 underline">
          Voltar para a listagem
        </Link>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 px-6 pt-28 pb-10">
      <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-lg overflow-hidden p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Avaliar imóvel</h1>
        <p className="text-gray-600 mb-6">
          {property?.name} - preencha todas as categorias para enviar sua avaliação.
        </p>

        {error && <p className="text-red-500 mb-4">{error}</p>}

        <form onSubmit={handleSubmit} className="space-y-6">
          {categories.map((category) => {
            const values = formByCategory[category.id] || { stars: "", comment: "" };
            return (
              <section key={category.id} className="border border-gray-200 rounded-xl p-4 bg-gray-50">
                <h2 className="text-lg font-semibold text-gray-900 mb-1">{category.name}</h2>
                <p className="text-sm text-gray-600 mb-4">{category.description}</p>

                <div className="grid gap-4 md:grid-cols-3">
                  <label className="flex flex-col text-sm text-gray-700">
                    Nota (0 a 5)
                    <select
                      className="mt-1 border border-gray-300 rounded-lg px-3 py-2 bg-white"
                      value={values.stars}
                      onChange={(e) => updateField(category.id, "stars", e.target.value)}
                      required
                    >
                      <option value="">Selecione</option>
                      {[0, 1, 2, 3, 4, 5].map((value) => (
                        <option key={value} value={value}>
                          {value}
                        </option>
                      ))}
                    </select>
                  </label>

                  <label className="md:col-span-2 flex flex-col text-sm text-gray-700">
                    Comentário
                    <textarea
                      className="mt-1 border border-gray-300 rounded-lg px-3 py-2 bg-white min-h-24"
                      value={values.comment}
                      onChange={(e) => updateField(category.id, "comment", e.target.value)}
                      maxLength={500}
                      required
                    />
                  </label>
                </div>
              </section>
            );
          })}

          <div className="flex gap-3">
            <Link
              to={`/imovel/${property?.id || ""}`}
              className="border border-black text-black px-6 py-2 rounded-lg hover:bg-gray-100 transition"
            >
              Cancelar
            </Link>
            <button
              type="submit"
              className="bg-black text-white px-6 py-2 rounded-lg hover:opacity-90 transition disabled:opacity-60"
              disabled={submitting}
            >
              {submitting ? "Enviando..." : "Enviar avaliações"}
            </button>
          </div>
        </form>
      </div>
    </main>
  );
}

export default CreatePropertyEvaluation;
