// src/services/visitService.js
import API_URL from "./api";

export async function createVisit(data) {
  const res = await fetch(`${API_URL}/visits`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  const json = await res.json();
  if (!res.ok) throw json;
  return json;
}

export async function getMyVisits(token) {
  const res = await fetch(`${API_URL}/visits/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const json = await res.json();
  if (!res.ok) throw json;
  return json;
}

export async function getReceivedVisits(token) {
  const res = await fetch(`${API_URL}/visits/received`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const json = await res.json();
  if (!res.ok) throw json;
  return json;
}

export async function updateVisitStatus(visitId, status, token) {
  const res = await fetch(`${API_URL}/visits/${visitId}/status`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ status }),
  });
  const json = await res.json();
  if (!res.ok) throw json;
  return json;
}
