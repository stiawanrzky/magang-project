import api from '@/api';

const api = axios.create({
  baseURL: 'https://yudisium.pythonanywhere.com/api/'
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