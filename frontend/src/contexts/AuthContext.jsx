import { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";

import { createChatSocket } from "../services/chatSocket";
import { getUnreadChatCount } from "../services/chatService";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("user");
    return saved ? JSON.parse(saved) : null;
  });
  const [unreadChatsCount, setUnreadChatsCount] = useState(0);
  const socketRef = useRef(null);

  function setAuth(newToken, newUser) {
    setToken(newToken);
    setUser(newUser);
    localStorage.setItem("token", newToken);
    localStorage.setItem("user", JSON.stringify(newUser));
  }

  function logout() {
    socketRef.current?.disconnect();
    socketRef.current = null;
    setToken(null);
    setUser(null);
    setUnreadChatsCount(0);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  }

  const refreshUnreadChatsCount = useCallback(async (activeToken = token) => {
    if (!activeToken) {
      setUnreadChatsCount(0);
      return;
    }

    try {
      const response = await getUnreadChatCount(activeToken);
      setUnreadChatsCount(Number(response?.unread_count || 0));
    } catch {
      setUnreadChatsCount(0);
    }
  }, [token]);

  useEffect(() => {
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split(".")[1]));
        if (payload.exp * 1000 < Date.now()) {
          logout();
        }
      } catch {
        logout();
      }
    }
  }, [refreshUnreadChatsCount, token]);

  useEffect(() => {
    if (!token) {
      socketRef.current?.disconnect();
      socketRef.current = null;
      setUnreadChatsCount(0);
      return undefined;
    }

    refreshUnreadChatsCount(token);

    const socket = createChatSocket(token);
    socketRef.current = socket;

    function handleUnreadCountUpdated(payload) {
      setUnreadChatsCount(Number(payload?.unread_count || 0));
    }

    function handleConnect() {
      refreshUnreadChatsCount(token);
    }

    socket.on("connect", handleConnect);
    socket.on("unread_count_updated", handleUnreadCountUpdated);

    return () => {
      socket.off("connect", handleConnect);
      socket.off("unread_count_updated", handleUnreadCountUpdated);
      socket.disconnect();
      if (socketRef.current === socket) {
        socketRef.current = null;
      }
    };
  }, [token]);

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        setAuth,
        logout,
        isAuthenticated: !!token,
        unreadChatsCount,
        refreshUnreadChatsCount,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}
