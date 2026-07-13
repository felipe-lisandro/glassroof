import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { getPropertyById } from "../services/propertyService";
import { createVisit } from "../services/visitService";

function AgendarVisita() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();

  const [property, setProperty] = useState(null);
  const [scheduledAt, setScheduledAt] = useState("");
  const [note, setNote] = useState("");
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const data = await getPropertyById(Number(id));
        setProperty(data);
      } catch {
        setError("Imóvel não encontrado.");
      }
    }
    load();
  }, [id]);

  async function handleSubmit(event) {
    event.preventDefault();
    setError(null);

    if (!isAuthenticated || !user?.id) {
      setError("Você precisa estar logado para agendar uma visita.");
      return;
    }
    if (!scheduledAt) {
      setError("Escolha uma data e horário.");
      return;
    }
    if (new Date(scheduledAt) < new Date()) {
      setError("A data escolhida não pode estar no passado.");
      return;
    }

    try {
      setSubmitting(true);
      await createVisit({
        property_id: Number(id),
        user_id: user.id,
        scheduled_at: scheduledAt,
        note: note.trim() || undefined,
      });
      navigate("/minhas-visitas");
    } catch (err) {
      setError(err?.error || "Não foi possível agendar a visita.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 px-6 pt-28 pb-10">
      <div className="max-w-lg mx-auto bg-white rounded-2xl shadow-lg p-8">
        <h1 className="text-3xl font-bold mb-2">Agendar visita</h1>
        {property && (
          <p className="text-gray-500 mb-6">
            {property.name} — {property.location?.city}, {property.location?.state}
          </p>
        )}

        {error && <p className="text-red-500 mb-4">{error}</p>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-sm text-gray-700">Data e horário</label>
            <input
              type="datetime-local"
              className="mt-1 w-full border border-gray-300 rounded-lg px-3 py-2"
              value={scheduledAt}
              onChange={(event) => setScheduledAt(event.target.value)}
            />
          </div>

          <div>
            <label className="text-sm text-gray-700">Observação (opcional)</label>
            <textarea
              className="mt-1 w-full border border-gray-300 rounded-lg px-3 py-2 min-h-24"
              value={note}
              onChange={(event) => setNote(event.target.value)}
              maxLength={500}
              placeholder="Ex.: prefiro no período da manhã"
            />
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="submit"
              disabled={submitting}
              className="bg-black text-white px-6 py-2 rounded-lg hover:opacity-90 transition disabled:opacity-50"
            >
              {submitting ? "Agendando..." : "Solicitar visita"}
            </button>
            <Link to={`/imovel/${id}`}>
              <button
                type="button"
                className="border border-black text-black px-6 py-2 rounded-lg hover:bg-gray-100 transition"
              >
                Cancelar
              </button>
            </Link>
          </div>
        </form>
      </div>
    </main>
  );
}

export default AgendarVisita;
