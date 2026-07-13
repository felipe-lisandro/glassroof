import { useState, useEffect, useCallback } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import {
  getMyVisits,
  getReceivedVisits,
  updateVisitStatus,
} from "../services/visitService";

const STATUS_LABEL = {
  pending: { text: "Pendente", className: "bg-amber-100 text-amber-800" },
  confirmed: { text: "Confirmada", className: "bg-green-100 text-green-800" },
  cancelled: { text: "Recusada", className: "bg-red-100 text-red-800" },
};

function StatusBadge({ status }) {
  const info = STATUS_LABEL[status] || { text: status, className: "bg-gray-100 text-gray-800" };
  return (
    <span className={`text-xs font-bold px-3 py-1 rounded-full ${info.className}`}>
      {info.text}
    </span>
  );
}

function formatDate(value) {
  if (!value) return "-";
  const date = new Date(value);
  return date.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
}

function MinhasVisitas() {
  const { user, token, isAuthenticated } = useAuth();
  const isEnterprise = user?.type === "enterprise";

  const [myVisits, setMyVisits] = useState([]);
  const [received, setReceived] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionError, setActionError] = useState(null);

  const load = useCallback(async () => {
    if (!token) return;
    try {
      setLoading(true);
      const mine = await getMyVisits(token);
      setMyVisits(Array.isArray(mine) ? mine : []);
      if (isEnterprise) {
        const rec = await getReceivedVisits(token);
        setReceived(Array.isArray(rec) ? rec : []);
      }
      setError(null);
    } catch {
      setError("Não foi possível carregar as visitas.");
    } finally {
      setLoading(false);
    }
  }, [token, isEnterprise]);

  useEffect(() => {
    load();
  }, [load]);

  async function handleStatus(visitId, status) {
    try {
      setActionError(null);
      await updateVisitStatus(visitId, status, token);
      setReceived((prev) =>
        prev.map((visit) => (visit.id === visitId ? { ...visit, status } : visit))
      );
    } catch (err) {
      setActionError(err?.error || "Falha ao atualizar a visita.");
    }
  }

  if (!isAuthenticated) {
    return (
      <div className="text-center pt-40">
        <p className="text-gray-600 mb-4">Você precisa estar logado para ver suas visitas.</p>
        <Link to="/login" className="text-blue-600 underline">Entrar</Link>
      </div>
    );
  }

  if (loading) return <div className="text-center pt-40">Carregando visitas...</div>;

  return (
    <main className="min-h-screen bg-gray-100 px-6 pt-28 pb-10">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Minhas Visitas</h1>
        {error && <p className="text-red-500 mb-4">{error}</p>}

        <section className="mb-10">
          <h2 className="text-xl font-semibold mb-4">Visitas solicitadas por mim</h2>
          {myVisits.length === 0 ? (
            <div className="bg-white rounded-2xl p-8 text-center shadow-md">
              <p className="text-gray-500">Você ainda não solicitou nenhuma visita.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {myVisits.map((visit) => (
                <div
                  key={visit.id}
                  className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 flex items-center justify-between"
                >
                  <div>
                    <p className="font-semibold text-gray-900">Imóvel #{visit.property_id}</p>
                    <p className="text-sm text-gray-500">{formatDate(visit.scheduled_at)}</p>
                    {visit.note && <p className="text-sm text-gray-600 mt-1">{visit.note}</p>}
                  </div>
                  <StatusBadge status={visit.status} />
                </div>
              ))}
            </div>
          )}
        </section>

        {isEnterprise && (
          <section>
            <h2 className="text-xl font-semibold mb-4">Visitas recebidas nos meus imóveis</h2>
            {actionError && <p className="text-red-500 mb-3">{actionError}</p>}
            {received.length === 0 ? (
              <div className="bg-white rounded-2xl p-8 text-center shadow-md">
                <p className="text-gray-500">Nenhuma visita solicitada aos seus imóveis.</p>
              </div>
            ) : (
              <div className="space-y-3">
                {received.map((visit) => (
                  <div
                    key={visit.id}
                    className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 flex items-center justify-between gap-4"
                  >
                    <div>
                      <p className="font-semibold text-gray-900">
                        Imóvel #{visit.property_id} — usuário #{visit.user_id}
                      </p>
                      <p className="text-sm text-gray-500">{formatDate(visit.scheduled_at)}</p>
                      {visit.note && <p className="text-sm text-gray-600 mt-1">{visit.note}</p>}
                    </div>
                    <div className="flex items-center gap-2">
                      <StatusBadge status={visit.status} />
                      {visit.status === "pending" && (
                        <>
                          <button
                            type="button"
                            onClick={() => handleStatus(visit.id, "confirmed")}
                            className="text-sm border border-green-600 text-green-700 px-3 py-1 rounded hover:bg-green-50 transition"
                          >
                            Confirmar
                          </button>
                          <button
                            type="button"
                            onClick={() => handleStatus(visit.id, "cancelled")}
                            className="text-sm border border-red-600 text-red-600 px-3 py-1 rounded hover:bg-red-50 transition"
                          >
                            Recusar
                          </button>
                        </>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}
      </div>
    </main>
  );
}

export default MinhasVisitas;
