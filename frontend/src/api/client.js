import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  timeout: 120000,
});

export const ingestDialogue = (dialogue) =>
  api.post("/ingest", { dialogue });

export const getPatients = (query = "") =>
  api.get("/patients", { params: query ? { query } : {} });

export const getPatient = (patientId) =>
  api.get(`/patients/${patientId}`);

export const searchSimilar = (query, topK = 5) =>
  api.post(`/search/similar?query=${query}&top_k=${topK}`);

export const getAnalytics = () =>
  api.get("/analytics");