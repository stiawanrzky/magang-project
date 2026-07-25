import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/' // Sesuaikan dengan URL Django Anda
});

// INTERCEPTOR: Otomatis tempelkan token ke Header setiap kali panggil API
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export default api;