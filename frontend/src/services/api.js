const API_URL = "http://localhost:5000";

export async function registerPerson(data) {
  const res = await fetch(`${API_URL}/users/person`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  const json = await res.json();
  if (!res.ok) throw json;
  return json;
}

export async function loginUser(email, password) {
  const res = await fetch(`${API_URL}/users/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  const json = await res.json();
  if (!res.ok) throw json;
  return json;
}

export async function getProperties() {
  const res = await fetch(`${API_URL}/properties`);
  const json = await res.json();
  if (!res.ok) throw json;
  return json;
}

export async function createProperty(data, token) {
  const res = await fetch(`${API_URL}/properties/`, {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify(data),
  });
  const json = await res.json();
  if (!res.ok) throw json;
  return json;
}

export default API_URL;
