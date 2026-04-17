// src/services/propertyService.js
import API_URL from "./api";

export async function getProperties() {
  const res = await fetch(`${API_URL}/properties`);
  const json = await res.json();
  if (!res.ok) throw json;
  return json;
}

export async function getPropertyById(id) {
  const res = await fetch(`${API_URL}/properties/${id}`);
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

export async function getPropertiesByEnterprise(enterpriseId) {
  const res = await fetch(`${API_URL}/properties/enterprise/${enterpriseId}`);
  const json = await res.json();
  if (!res.ok) throw json;
  return json;
}