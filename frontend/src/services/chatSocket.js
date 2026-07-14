import { io } from "socket.io-client";

import API_URL from "./api";

export function createChatSocket(token) {
  return io(API_URL, {
    autoConnect: true,
    auth: { token },
  });
}