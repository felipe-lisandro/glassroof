import { useEffect, useRef, useState } from "react";
import { Link, Navigate, useParams } from "react-router-dom";

import { useAuth } from "../contexts/AuthContext";
import { getChat, getChatMessages, markChatAsRead } from "../services/chatService";
import { createChatSocket } from "../services/chatSocket";

function formatTimestamp(value) {
  if (!value) return "";
  return new Date(value).toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatVisitDate(value) {
  if (!value) return "Data da visita não informada";
  return new Date(value).toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function ChatRoom() {
  const { roomId } = useParams();
  const { token, user, isAuthenticated, refreshUnreadChatsCount } = useAuth();
  const [room, setRoom] = useState(null);
  const [messages, setMessages] = useState([]);
  const [draft, setDraft] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [socketError, setSocketError] = useState(null);
  const [socketConnected, setSocketConnected] = useState(false);
  const socketRef = useRef(null);
  const bottomRef = useRef(null);

  useEffect(() => {
    if (!bottomRef.current) return;
    bottomRef.current.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    async function loadRoom() {
      if (!token || !roomId) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const [roomData, messageData] = await Promise.all([
          getChat(roomId, token),
          getChatMessages(roomId, token),
        ]);
        setRoom(roomData);
        setMessages(Array.isArray(messageData) ? messageData : []);
        await markChatAsRead(roomId, token);
        await refreshUnreadChatsCount(token);
        setError(null);
      } catch (err) {
        setError(err?.error || "Não foi possível carregar esta conversa.");
      } finally {
        setLoading(false);
      }
    }

    loadRoom();
  }, [refreshUnreadChatsCount, roomId, token]);

  useEffect(() => {
    if (!token || !roomId) return undefined;

    const socket = createChatSocket(token);
    socketRef.current = socket;

    function handleConnect() {
      setSocketConnected(true);
      setSocketError(null);
      socket.emit("join_chat", { token, room_id: Number(roomId) });
    }

    function handleDisconnect() {
      setSocketConnected(false);
    }

    async function handleMessageCreated(message) {
      setMessages((current) => {
        if (current.some((item) => item.id === message.id)) {
          return current;
        }
        return [...current, message];
      });

      if (message.sender_id !== user?.id) {
        try {
          await markChatAsRead(roomId, token);
          await refreshUnreadChatsCount(token);
        } catch {
          setSocketError("Falha ao atualizar mensagens lidas.");
        }
      }
    }

    function handleChatError(payload) {
      setSocketError(payload?.error || "Falha na conexão em tempo real.");
    }

    socket.on("connect", handleConnect);
    socket.on("disconnect", handleDisconnect);
    socket.on("message_created", handleMessageCreated);
    socket.on("chat_error", handleChatError);

    return () => {
      socket.emit("leave_chat", { room_id: Number(roomId) });
      socket.off("connect", handleConnect);
      socket.off("disconnect", handleDisconnect);
      socket.off("message_created", handleMessageCreated);
      socket.off("chat_error", handleChatError);
      socket.disconnect();
    };
  }, [refreshUnreadChatsCount, roomId, token, user?.id]);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  const counterpart = user?.type === "enterprise" ? room?.participants?.person : room?.participants?.enterprise;

  function handleSubmit(event) {
    event.preventDefault();
    if (!socketRef.current || !draft.trim()) {
      return;
    }

    setSocketError(null);
    socketRef.current.emit("send_message", {
      token,
      room_id: Number(roomId),
      content: draft.trim(),
    });
    setDraft("");
  }

  return (
    <main className="min-h-screen bg-gray-100 px-6 pb-10 pt-28">
      <div className="mx-auto max-w-5xl overflow-hidden rounded-3xl bg-white shadow-xl">
        <header className="border-b border-gray-200 px-6 py-5">
          <div className="mb-2 flex items-center justify-between gap-4">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.22em] text-blue-600">Chat da visita</p>
              <h1 className="text-2xl font-bold text-gray-900">{room?.property?.name || "Conversa"}</h1>
            </div>
            <div className="flex items-center gap-4">
              {room?.property?.id && (
                <Link
                  to={`/imovel/${room.property.id}`}
                  className="text-sm font-semibold text-gray-700 hover:text-gray-900"
                >
                  Ver imóvel
                </Link>
              )}
              <Link to="/chats" className="text-sm font-semibold text-blue-600 hover:text-blue-700">
                Voltar para chats
              </Link>
            </div>
          </div>
          <div className="flex flex-wrap items-center gap-3 text-sm text-gray-500">
            <span>Com {counterpart?.name || "participante"}</span>
            <span>Visita marcada para {formatVisitDate(room?.visit?.scheduled_at)}</span>
            <span className={socketConnected ? "text-emerald-600" : "text-amber-600"}>
              {socketConnected ? "Conectado" : "Reconectando..."}
            </span>
          </div>
        </header>

        {loading && <div className="p-6 text-gray-600">Carregando conversa...</div>}
        {!loading && error && <div className="p-6 text-red-600">{error}</div>}

        {!loading && !error && (
          <>
            <section className="flex h-[60vh] flex-col gap-4 overflow-y-auto bg-gray-50 px-6 py-5">
              {messages.length === 0 && (
                <div className="rounded-2xl border border-dashed border-gray-300 bg-white p-6 text-center text-sm text-gray-500">
                  A sala está aberta. Envie a primeira mensagem para começar.
                </div>
              )}

              {messages.map((message) => {
                const isOwnMessage = message.sender_id === user?.id;

                return (
                  <div key={message.id} className={`flex ${isOwnMessage ? "justify-end" : "justify-start"}`}>
                    <article
                      className={`max-w-[75%] rounded-2xl px-4 py-3 shadow-sm ${
                        isOwnMessage ? "bg-blue-600 text-white" : "bg-white text-gray-900"
                      }`}
                    >
                      <p className="mb-2 text-xs font-semibold uppercase tracking-[0.16em] opacity-70">
                        {isOwnMessage ? "Você" : message.sender?.name || "Participante"}
                      </p>
                      <p className="whitespace-pre-wrap text-sm leading-6">{message.content}</p>
                      <p className={`mt-2 text-right text-[11px] ${isOwnMessage ? "text-blue-100" : "text-gray-400"}`}>
                        {formatTimestamp(message.created_at)}
                      </p>
                    </article>
                  </div>
                );
              })}
              <div ref={bottomRef} />
            </section>

            <footer className="border-t border-gray-200 px-6 py-5">
              {socketError && <p className="mb-3 text-sm text-red-600">{socketError}</p>}
              <form className="flex gap-3" onSubmit={handleSubmit}>
                <textarea
                  value={draft}
                  onChange={(event) => setDraft(event.target.value)}
                  placeholder="Escreva sua mensagem"
                  className="min-h-14 flex-1 resize-none rounded-2xl border border-gray-300 px-4 py-3 text-sm outline-none transition focus:border-blue-500"
                  maxLength={1000}
                />
                <button
                  type="submit"
                  disabled={!draft.trim() || !socketConnected}
                  className="rounded-2xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  Enviar
                </button>
              </form>
            </footer>
          </>
        )}
      </div>
    </main>
  );
}