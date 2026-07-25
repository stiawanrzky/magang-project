<script setup>
import { ref } from 'vue';
import api from '../api';
import { useRouter } from 'vue-router';

const router = useRouter();
const loading = ref(false);
const errorMessage = ref('');
const form = ref({ username: '', password: '' });

// Fungsi untuk menentukan route berdasarkan role
const getDashboardRoute = (role) => {
  if (role === 'MAHASISWA') return 'dashboardMhs';
  if (role.includes('DOSEN') || role === 'BAAK') return 'dashboardBAAK';
  if (role.includes('AKADEMIK')) return 'dashboardAkademik';
  if (role.includes('PERPUS')) return 'dashboardPerpus';
  if (role.includes('SUPERADMIN')) return 'dashboardAdmin';
  return null;
};

const handleLogin = async () => {
  loading.value = true;
  errorMessage.value = '';

  try {
    // 1. Ambil Token
    const resToken = await api.post('token/', form.value);
    
    // Clear storage lama sebelum set yang baru
    localStorage.clear(); 
    localStorage.setItem('access_token', resToken.data.access);
    localStorage.setItem('refresh_token', resToken.data.refresh);
    
    // 2. Ambil Profil User
    const resUser = await api.get('users/me/');
    const roleRaw = resUser.data.role || '';
    const role = roleRaw.toUpperCase().trim(); 

    localStorage.setItem('user_role', role);
    console.log("Login Berhasil! Role:", role);

    // 3. LOGIKA PENGALIHAN
    const targetRoute = getDashboardRoute(role);
    
    if (targetRoute) {
      await router.replace({ name: targetRoute });
    } else {
      throw new Error(`Role [${roleRaw}] tidak memiliki akses dashboard.`);
    }

  } catch (err) {
    localStorage.clear(); // Bersihkan jika gagal
    if (err.response && err.response.status === 401) {
      errorMessage.value = 'Username atau Password salah!';
    } else if (err.message) {
      errorMessage.value = err.message;
    } else {
      errorMessage.value = 'Gagal terhubung ke server backend.';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-50 px-4">
    <div class="max-w-md w-full bg-white p-8 rounded-2xl shadow-xl border border-slate-100">
      <div class="text-center mb-8">
        <h2 class="text-2xl font-black text-slate-800 uppercase tracking-tight">Login STIE SBI Yudisium</h2>
        <p class="text-slate-500 text-sm">Silakan masuk dengan akun Anda</p>
      </div>

      <div v-if="errorMessage" class="mb-6 p-3 bg-red-50 text-red-700 text-xs rounded-lg border-l-4 border-red-500 font-bold">
        ⚠️ {{ errorMessage }}
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-xs font-bold text-slate-500 mb-1 tracking-widest uppercase">Username</label>
          <input v-model="form.username" type="text" required class="w-full p-3 bg-slate-50 border rounded-xl outline-none focus:ring-2 focus:ring-indigo-500">
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-500 mb-1 tracking-widest uppercase">Password</label>
          <input v-model="form.password" type="password" required class="w-full p-3 bg-slate-50 border rounded-xl outline-none focus:ring-2 focus:ring-indigo-500">
        </div>
        <button type="submit" :disabled="loading" class="w-full bg-indigo-600 text-white py-3.5 rounded-xl font-black hover:bg-indigo-700 transition disabled:opacity-50 shadow-lg shadow-indigo-200">
          <span v-if="loading">MEMVERIFIKASI...</span>
          <span v-else>MASUK KE DASHBOARD</span>
        </button>
      </form>
      
      <div class="mt-8 text-center">
        <p class="text-xs text-slate-400">Belum punya akun? <router-link to="/register" class="text-indigo-600 font-bold">Daftar Sekarang</router-link></p>
      </div>
    </div>
  </div>
</template>