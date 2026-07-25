<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 px-4 py-12">
    <div class="max-w-md w-full bg-white p-8 rounded-xl shadow-lg border border-gray-200">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-indigo-600">Registrasi Yudisium</h2>
        <p class="text-gray-500 mt-2">Daftarkan akun sesuai dengan peran Anda</p>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-4">
        
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Nama Lengkap (Sesuai Akte)</label>
          <input v-model="form.full_name" type="text" placeholder="Masukkan nama lengkap" required 
            class="w-full p-2.5 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none">
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">NIM / Username</label>
            <input v-model="form.username" type="text" placeholder="Masukkan NIM" required 
              class="w-full p-2.5 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none">
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Thn Angkatan</label>
            <input v-model="form.angkatan" type="number" placeholder="Contoh: 2020" required 
              class="w-full p-2.5 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none">
          </div>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Email</label>
          <input v-model="form.email" type="email" placeholder="contoh@kampus.ac.id" required 
            class="w-full p-2.5 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none">
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Program Studi</label>
          <select v-model="form.prodi" required 
            class="w-full p-2.5 border rounded-lg bg-white focus:ring-2 focus:ring-indigo-500 outline-none">
            <option value="" disabled selected>Pilih Program Studi</option>
            <option value="AKUNTANSI">Akuntansi</option>
            <option value="MANAJEMEN">Manajemen</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Peran (Role)</label>
          <select v-model="form.role" required 
            class="w-full p-2.5 border rounded-lg bg-white focus:ring-2 focus:ring-indigo-500 outline-none">
            <option value="" disabled selected>Pilih Peran Anda</option>
            <option value="MAHASISWA">Mahasiswa</option>
            <option value="BAAK">Biro Administrasi Akademik Kemahasiswaan </option>
            <option value="AKADEMIK">Bagian Akademik</option>
            <option value="PERPUS">Bagian Perpustakaan</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Password</label>
          <input v-model="form.password" type="password" placeholder="Minimal 8 karakter" required 
            class="w-full p-2.5 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none">
        </div>

        <button type="submit" :disabled="loading || form.password.length < 8" 
          class="w-full bg-indigo-600 text-white py-3 mt-2 rounded-lg font-bold hover:bg-indigo-700 transition shadow-md disabled:opacity-50">
          <span v-if="loading">Menyimpan Data...</span>
          <span v-else>Daftar Sekarang</span>
        </button>
      </form>

      <p class="mt-6 text-center text-sm text-gray-600">
        Sudah punya akun? 
        <router-link to="/login" class="text-indigo-600 font-bold hover:underline">Login di sini</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '../api';
import { useRouter } from 'vue-router';

const router = useRouter();
const loading = ref(false);

const form = ref({
  full_name: '',
  username: '',
  angkatan: '',
  email: '',
  prodi: '',
  password: '',
  role: ''
});

const handleRegister = async () => {
  loading.value = true;
  try {
    await api.post('users/register/', form.value);
    alert('Registrasi Berhasil! Silakan Login.');
    router.push('/login');
  } catch (err) {
    const errorDetail = err.response?.data ? JSON.stringify(err.response.data) : 'Terjadi kesalahan';
    alert('Gagal Daftar: ' + errorDetail);
  } finally {
    loading.value = false;
  }
};
</script>