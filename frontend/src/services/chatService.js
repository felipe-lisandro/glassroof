import API_URL from "./api";

async function parseResponse(response) {
  const json = await response.json();
  if (!response.ok) {
    throw json;
  }
  return json;
}

export async function createChatRoom(propertyId, token) {
  const response = await fetch(`${API_URL}/chats`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ property_id: propertyId }),
  });

  return parseResponse(response);
}

export async function getChats(token) {
  const response = await fetch(`${API_URL}/chats`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return parseResponse(response);
}

export async function getChat(roomId, token) {
  const response = await fetch(`${API_URL}/chats/${roomId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return parseResponse(response);
}

export async function getChatMessages(roomId, token) {
  const response = await fetch(`${API_URL}/chats/${roomId}/messages`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return parseResponse(response);
}

export async function getUnreadChatCount(token) {
  const response = await fetch(`${API_URL}/chats/unread-count`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return parseResponse(response);
}

export async function markChatAsRead(roomId, token) {
  const response = await fetch(`${API_URL}/chats/${roomId}/read`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({}),
  });

  return parseResponse(response);
}