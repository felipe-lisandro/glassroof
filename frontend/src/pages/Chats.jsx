import { useEffect, useState } from "react";
import { Link, Navigate } from "react-router-dom";

import { useAuth } from "../contexts/AuthContext";
import { getChats } from "../services/chatService";

function formatDate(value) {
  if (!value) return "Sem mensagens ainda";
  return new Date(value).toLocaleString("pt-BR");
}

function formatVisitDate(value) {
  if (!value) return "Data não informada";
  return new Date(value).toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function Chats() {
  const { token, user, isAuthenticated } = useAuth();
  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadRooms() {
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const data = await getChats(token);
        setRooms(Array.isArray(data) ? data : []);
        setError(null);
      } catch (err) {
        setError(err?.error || "Não foi possível carregar os chats.");
      } finally {
        setLoading(false);
      }
    }

    loadRooms();
  }, [token]);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <main className="min-h-screen bg-gray-50 px-6 pb-12 pt-28">
      <div className="mx-auto max-w-5xl">
        <header className="mb-8 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.25em] text-blue-600">Mensagens</p>
            <h1 className="text-4xl font-bold text-gray-900">Seus chats</h1>
          </div>
          <p className="text-sm text-gray-500">{user?.type === "enterprise" ? "Conversas recebidas das visitas agendadas" : "Conversas liberadas por visitas marcadas"}</p>
        </header>

        {loading && <p className="rounded-2xl bg-white p-6 text-gray-600 shadow-sm">Carregando conversas...</p>}
        {!loading && error && <p className="rounded-2xl bg-red-50 p-6 text-red-600 shadow-sm">{error}</p>}

        {!loading && !error && rooms.length === 0 && (
          <div className="rounded-2xl bg-white p-8 text-gray-600 shadow-sm">
            Nenhum chat disponível no momento. Para abrir uma conversa, o imóvel precisa ter uma visita marcada.
          </div>
        )}

        {!loading && !error && rooms.length > 0 && (
          <div className="grid gap-4">
            {rooms.map((room) => {
              const counterpart = user?.type === "enterprise" ? room.participants?.person : room.participants?.enterprise;
              return (
                <Link
                  key={room.id}
                  to={`/chats/${room.id}`}
                  className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
                >
                  <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gray-400">Imóvel</p>
                      <h2 className="text-xl font-semibold text-gray-900">{room.property?.name || "Imóvel"}</h2>
                    </div>
                    <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700">
                      Visita: {formatVisitDate(room.visit?.scheduled_at)}
                    </span>
                  </div>

                  <div className="mb-2 flex flex-wrap items-center justify-between gap-2 text-sm text-gray-600">
                    <span>Com {counterpart?.name || "participante"}</span>
                    <div className="flex items-center gap-2">
                      {room.unread_count > 0 && (
                        <span className="rounded-full bg-red-500 px-2 py-0.5 text-[10px] font-bold text-white">
                          {room.unread_count} nova{room.unread_count > 1 ? "s" : ""}
                        </span>
                      )}
                      <span>{formatDate(room.last_message_at || room.created_at)}</span>
                    </div>
                  </div>

                  <p className="line-clamp-2 text-sm text-gray-500">
                    {room.latest_message?.content || "Sala criada. Envie a primeira mensagem."}
                  </p>
                </Link>
              );
            })}
          </div>
        )}
      </div>
    </main>
  );
}