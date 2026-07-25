<template>
  <div class="min-h-screen bg-slate-50 flex flex-col md:flex-row overflow-x-hidden">
    <!-- SIDEBAR -->
    <aside class="w-full md:w-64 bg-slate-900 text-white flex flex-col shadow-xl shrink-0">
      <div class="p-6 text-xl font-bold border-b border-slate-800 flex items-center gap-3">
        <span class="bg-indigo-500 p-1 rounded text-white text-sm">🔑</span>
        Super Admin
      </div>
      <nav class="flex-1 p-4 space-y-2">
        <button @click="view = 'stats'" :class="view === 'stats' ? 'bg-indigo-600 shadow-lg shadow-indigo-900/50' : 'hover:bg-slate-800 text-slate-400'" class="w-full text-left p-3 rounded-lg flex items-center gap-3 transition-all duration-200">📊 Ringkasan Arus</button>
        <button @click="view = 'users'" :class="view === 'users' ? 'bg-indigo-600 shadow-lg shadow-indigo-900/50' : 'hover:bg-slate-800 text-slate-400'" class="w-full text-left p-3 rounded-lg flex items-center gap-3 transition-all duration-200">👥 Kelola Akun</button>

        <!-- BAAK: Mata Kuliah & Transkrip -->
        <p class="text-xs text-slate-500 font-bold px-4 mt-4 mb-2 uppercase tracking-widest">BAAK</p>
        <button @click="view = 'matakuliah'" :class="view === 'matakuliah' ? 'bg-indigo-600 shadow-lg shadow-indigo-900/50' : 'hover:bg-slate-800 text-slate-400'" class="w-full text-left p-3 rounded-lg flex items-center gap-3 transition-all duration-200">📚 Kelola Mata Kuliah</button>
        <button @click="view = 'transkrip'; fetchTranskrip()" :class="view === 'transkrip' ? 'bg-indigo-600 shadow-lg shadow-indigo-900/50' : 'hover:bg-slate-800 text-slate-400'" class="w-full text-left p-3 rounded-lg flex items-center gap-3 transition-all duration-200">📝 Verifikasi Transkrip</button>

        <!-- Akademik: Verifikasi Berkas Yudisium -->
        <p class="text-xs text-slate-500 font-bold px-4 mt-4 mb-2 uppercase tracking-widest">AKADEMIK</p>
        <button @click="view = 'akademik'; fetchAkademik()" :class="view === 'akademik' ? 'bg-indigo-600 shadow-lg shadow-indigo-900/50' : 'hover:bg-slate-800 text-slate-400'" class="w-full text-left p-3 rounded-lg flex items-center gap-3 transition-all duration-200">🎓 Verifikasi Akademik</button>

        <!-- Pendaftaran Yudisium -->
        <button @click="view = 'pendaftaran'; fetchPendaftaran()" :class="view === 'pendaftaran' ? 'bg-indigo-600 shadow-lg shadow-indigo-900/50' : 'hover:bg-slate-800 text-slate-400'" class="w-full text-left p-3 rounded-lg flex items-center gap-3 transition-all duration-200">📋 Verifikasi Pendaftaran</button>

        <!-- Perpustakaan -->
        <p class="text-xs text-slate-500 font-bold px-4 mt-4 mb-2 uppercase tracking-widest">PERPUSTAKAAN</p>
        <button @click="view = 'perpus'; fetchPerpus()" :class="view === 'perpus' ? 'bg-indigo-600 shadow-lg shadow-indigo-900/50' : 'hover:bg-slate-800 text-slate-400'" class="w-full text-left p-3 rounded-lg flex items-center gap-3 transition-all duration-200">📚 Verifikasi Perpustakaan</button>

        <!-- Periode -->
        <p class="text-xs text-slate-500 font-bold px-4 mt-4 mb-2 uppercase tracking-widest">PENGATURAN</p>
        <button @click="view = 'periode'; fetchPeriode()" :class="view === 'periode' ? 'bg-indigo-600 shadow-lg shadow-indigo-900/50' : 'hover:bg-slate-800 text-slate-400'" class="w-full text-left p-3 rounded-lg flex items-center gap-3 transition-all duration-200">📅 Periode Yudisium</button>
      </nav>
      <div class="p-4 border-t border-slate-800">
        <button @click="handleLogout" class="w-full py-2 bg-rose-600 hover:bg-rose-700 rounded-lg text-sm font-bold transition">Keluar Sistem</button>
      </div>
    </aside>

    <!-- MAIN CONTENT -->
    <main class="flex-1 p-6 md:p-10 overflow-y-auto max-w-full">

      <!-- ===== STATS VIEW ===== -->
      <div v-if="view === 'stats'" class="animate-in fade-in duration-500">
        <header class="mb-8 flex justify-between items-end">
          <div>
            <h1 class="text-3xl font-black text-slate-800">Dashboard Utama</h1>
            <p class="text-slate-500">Data verifikasi akademik terkini.</p>
          </div>
          <button @click="fetchAkademik" class="px-4 py-2 bg-white border border-slate-200 rounded-xl text-xs font-bold hover:bg-slate-50 flex items-center gap-2 transition">
            <span :class="{'animate-spin': loading}">🔄</span> Perbarui Data
          </button>
        </header>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 group hover:border-indigo-200 transition">
            <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Total Mahasiswa</p>
            <h3 class="text-4xl font-black text-slate-800">{{ stats.total }}</h3>
          </div>
          <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 border-l-4 border-l-amber-500 group hover:border-amber-200 transition">
            <p class="text-[10px] font-black text-amber-600 uppercase tracking-widest mb-1">Menunggu Verifikasi</p>
            <h3 class="text-4xl font-black text-slate-800">{{ stats.menunggu }}</h3>
          </div>
          <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 border-l-4 border-l-emerald-500 group hover:border-emerald-200 transition">
            <p class="text-[10px] font-black text-emerald-600 uppercase tracking-widest mb-1">Sudah Disetujui</p>
            <h3 class="text-4xl font-black text-slate-800">{{ stats.selesai }}</h3>
          </div>
          <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 border-l-4 border-l-rose-500 group hover:border-rose-200 transition">
            <p class="text-[10px] font-black text-rose-600 uppercase tracking-widest mb-1">Ditolak</p>
            <h3 class="text-4xl font-black text-slate-800">{{ stats.ditolak }}</h3>
          </div>
        </div>
      </div>

      <!-- ===== USERS VIEW ===== -->
      <div v-if="view === 'users'" class="animate-in slide-in-from-bottom-4 duration-500">
        <header class="mb-8">
          <h1 class="text-3xl font-black text-slate-800">Manajemen Pengguna</h1>
          <p class="text-slate-500">Kelola akses staff dan mahasiswa dalam satu tempat.</p>
        </header>
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div class="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 h-fit">
            <h2 class="text-lg font-bold mb-6 flex items-center gap-2"> Buat Akun Baru</h2>
            <form @submit.prevent="handleCreateAccount" class="space-y-4">
              <div>
                <label class="block text-[10px] font-black text-slate-500 mb-2 uppercase">Nama Lengkap</label>
                <input v-model="newUser.full_name" type="text" class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none" placeholder="Contoh: Budi Santoso" required>
              </div>
              <div>
                <label class="block text-[10px] font-black text-slate-500 mb-2 uppercase">Username / NIM</label>
                <input v-model="newUser.username" type="text" class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none font-mono" placeholder="ID Akun" required>
              </div>
              <div>
                <label class="block text-[10px] font-black text-slate-500 mb-2 uppercase">Tipe Role</label>
                <select v-model="newUser.role" class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none font-bold">
                  <option v-for="r in roles" :key="r" :value="r">{{ r }}</option>
                </select>
              </div>
              <div>
                <label class="block text-[10px] font-black text-slate-500 mb-2 uppercase">Password</label>
                <input v-model="newUser.password" type="password" class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none" required>
              </div>
              <button type="submit" :disabled="loading" class="w-full py-4 bg-indigo-600 text-white font-black rounded-xl hover:bg-indigo-700 transition disabled:bg-slate-300">
                {{ loading ? 'MENGIRIM...' : 'DAFTARKAN SEKARANG' }}
              </button>
            </form>
          </div>
          <div class="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            <div class="p-6 border-b border-slate-50 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <h3 class="font-bold text-slate-800">Data Staff & Mahasiswa</h3>
              <div class="relative w-full sm:w-64">
                <input v-model="searchUserQuery" type="text" placeholder="Cari Nama/Username..." class="w-full p-2.5 pl-10 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-indigo-500 outline-none transition">
                <span class="absolute left-3 top-3 opacity-30 text-xs">🔍</span>
              </div>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left">
                <thead class="bg-slate-50 text-slate-400 text-[10px] uppercase font-bold">
                  <tr>
                    <th class="px-6 py-4">Nama User</th>
                    <th class="px-6 py-4">Username</th>
                    <th class="px-6 py-4">Role</th>
                    <th class="px-6 py-4 text-center">Aksi</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100 text-sm">
                  <tr v-for="u in filteredUsers" :key="u.id" class="hover:bg-slate-50/50 transition">
                    <td class="px-6 py-4 font-bold text-slate-700">{{ u.full_name }}</td>
                    <td class="px-6 py-4 text-slate-500 font-mono">{{ u.username }}</td>
                    <td class="px-6 py-4">
                      <span class="px-2 py-1 rounded text-[9px] bg-indigo-50 text-indigo-600 font-black uppercase">{{ u.role }}</span>
                    </td>
                    <td class="px-6 py-4 flex justify-center gap-2">
                      <button @click="openEditModal(u)" class="text-indigo-600 hover:bg-indigo-50 px-3 py-1 rounded-lg font-bold">Edit</button>
                      <button @click="handleDelete(u)" class="text-rose-600 hover:bg-rose-50 px-3 py-1 rounded-lg font-bold">Hapus</button>
                    </td>
                  </tr>
                  <tr v-if="filteredUsers.length === 0">
                    <td colspan="4" class="p-12 text-center text-slate-400 italic">User tidak ditemukan.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== MATA KULIAH VIEW ===== -->
      <div v-if="view === 'matakuliah'" class="space-y-6 animate-in fade-in duration-500">
        <header class="mb-8">
          <h1 class="text-3xl font-black text-slate-800">📚 Kelola Mata Kuliah</h1>
          <p class="text-slate-500">Tambah, edit, atau hapus data mata kuliah untuk seluruh jurusan.</p>
        </header>
        <div class="bg-white p-5 rounded-2xl shadow-md border border-gray-100">
          <h3 class="font-bold text-gray-800 mb-4 flex items-center gap-2">🔍 Filter & Pencarian</h3>
          <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
            <input type="text" v-model="searchMatakuliah" placeholder="Cari Kode/Nama MK..." class="border border-gray-200 rounded-xl p-2.5 text-sm focus:ring-2 focus:ring-indigo-400 outline-none transition">
            <select v-model="filterJurusan" class="border border-gray-200 rounded-xl p-2.5 text-sm bg-white focus:ring-2 focus:ring-indigo-400 outline-none">
              <option value="">Semua Jurusan</option>
              <option value="Akuntansi">Akuntansi</option>
              <option value="Manajemen">Manajemen</option>
            </select>
            <select v-model="filterKategori" class="border border-gray-200 rounded-xl p-2.5 text-sm bg-white focus:ring-2 focus:ring-indigo-400 outline-none">
              <option value="">Semua Kategori</option>
              <option value="Wajib">Wajib</option>
              <option value="Pilihan">Pilihan</option>
              <option value="TA">Tugas Akhir</option>
            </select>
            <input v-if="filterKategori === 'Pilihan' || filterKategori === 'TA'" type="text" v-model="filterKelompok" placeholder="Cari Peminatan/Jalur..." class="border border-gray-200 rounded-xl p-2.5 text-sm focus:ring-2 focus:ring-indigo-400 outline-none">
            <button @click="bukaModalFormMk()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2.5 rounded-xl text-sm font-bold transition shadow-md flex items-center justify-center gap-2">
              <span>+</span> Tambah MK
            </button>
          </div>
        </div>
        <div class="bg-white rounded-2xl shadow-md border border-gray-100 overflow-hidden">
          <div class="p-4 border-b bg-indigo-50/50 flex justify-between items-center">
            <h3 class="font-bold text-indigo-900">📚 Data Mata Kuliah</h3>
            <span class="text-xs bg-indigo-200 text-indigo-800 px-3 py-1 rounded-full">Total: {{ filteredMataKuliah.length }} MK</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead class="bg-gray-50 text-gray-500 text-[11px] uppercase">
                <tr>
                  <th class="px-5 py-3">Kode</th>
                  <th class="px-5 py-3">Nama Mata Kuliah</th>
                  <th class="px-5 py-3 text-center w-16">SKS</th>
                  <th class="px-5 py-3">Jurusan</th>
                  <th class="px-5 py-3 text-center w-24">Kategori</th>
                  <th class="px-5 py-3">Peminatan/Jalur</th>
                  <th class="px-5 py-3 text-center w-20">Aksi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="mk in paginatedMatakuliah" :key="mk.kode" class="hover:bg-indigo-50/50 transition">
                  <td class="px-5 py-3 font-mono text-sm font-medium">{{ mk.kode }}</td>
                  <td class="px-5 py-3 font-medium">{{ mk.nama }}</td>
                  <td class="px-5 py-3 text-center font-bold">{{ mk.sks }}</td>
                  <td class="px-5 py-3 text-sm">
                    <span v-if="mk.jurusan === 'Semua Jurusan'" class="bg-gray-100 px-2 py-0.5 rounded-full text-xs">Semua</span>
                    <span v-else>{{ mk.jurusan }}</span>
                  </td>
                  <td class="px-5 py-3 text-center">
                    <span :class="{
                      'bg-blue-100 text-blue-700': mk.kategori === 'Wajib',
                      'bg-purple-100 text-purple-700': mk.kategori === 'Pilihan',
                      'bg-rose-100 text-rose-700': mk.kategori === 'TA'
                    }" class="px-2 py-0.5 rounded-full text-[10px] font-bold">{{ mk.kategori }}</span>
                  </td>
                  <td class="px-5 py-3 text-sm italic text-gray-500">{{ mk.kelompok || '-' }}</td>
                  <td class="px-5 py-3 text-center space-x-1">
                    <button @click="bukaModalFormMk(mk)" class="text-indigo-600 hover:bg-indigo-100 p-1.5 rounded-lg transition" title="Edit">✏️</button>
                    <button @click="hapusMataKuliah(mk.kode)" class="text-red-600 hover:bg-red-100 p-1.5 rounded-lg transition" title="Hapus">🗑️</button>
                  </td>
                </tr>
                <tr v-if="paginatedMatakuliah.length === 0">
                  <td colspan="7" class="px-5 py-10 text-center text-gray-400">📭 Tidak ada data mata kuliah</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="px-5 py-3 border-t flex flex-wrap gap-3 justify-between items-center bg-gray-50 text-sm">
            <span class="text-gray-500">Menampilkan {{ ((currentPageMatakuliah-1)*rowsPerPageMatakuliah)+1 }} - {{ Math.min(currentPageMatakuliah*rowsPerPageMatakuliah, filteredMataKuliah.length) }} dari {{ filteredMataKuliah.length }}</span>
            <div class="flex gap-2 items-center">
              <button @click="prevPageMatakuliah" :disabled="currentPageMatakuliah===1" class="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-100 transition">Prev</button>
              <span class="text-sm">Halaman {{ currentPageMatakuliah }} / {{ totalPagesMatakuliah }}</span>
              <button @click="nextPageMatakuliah" :disabled="currentPageMatakuliah===totalPagesMatakuliah" class="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-100 transition">Next</button>
            </div>
            <select v-model="rowsPerPageMatakuliah" class="border rounded-lg px-2 py-1 text-sm bg-white">
              <option :value="10">10</option>
              <option :value="25">25</option>
              <option :value="50">50</option>
            </select>
          </div>
        </div>
      </div>

      <!-- ===== VERIFIKASI AKADEMIK ===== -->
      <div v-if="view === 'akademik'" class="space-y-6 animate-in fade-in duration-500">
        <header class="mb-4 flex justify-between items-center flex-wrap gap-3">
          <div>
            <h1 class="text-3xl font-black text-slate-800">🎓 Verifikasi Akademik</h1>
            <p class="text-slate-500">Validasi berkas akademik mahasiswa (foto ijazah, akte, KTP, 3x4).</p>
          </div>
          <div class="flex gap-2">
            <button @click="fetchAkademik" class="px-4 py-2 bg-white border border-slate-200 rounded-xl text-xs font-bold hover:bg-slate-50 flex items-center gap-2 transition">
              <span :class="{'animate-spin': loading}">🔄</span> Refresh
            </button>
          </div>
        </header>

        <!-- Statistik -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-white p-4 rounded-xl shadow-sm border-l-4 border-orange-500">
            <p class="text-xs text-gray-400 uppercase tracking-wide">Menunggu Verifikasi</p>
            <h3 class="text-2xl font-bold text-orange-600">{{ akademikMenungguCount }}</h3>
          </div>
          <div class="bg-white p-4 rounded-xl shadow-sm border-l-4 border-green-500">
            <p class="text-xs text-gray-400 uppercase tracking-wide">Sudah Disetujui</p>
            <h3 class="text-2xl font-bold text-green-600">{{ akademikDisetujuiCount }}</h3>
          </div>
          <div class="bg-white p-4 rounded-xl shadow-sm border-l-4 border-red-500">
            <p class="text-xs text-gray-400 uppercase tracking-wide">Ditolak</p>
            <h3 class="text-2xl font-bold text-red-600">{{ akademikDitolakCount }}</h3>
          </div>
        </div>

        <!-- Pencarian & Filter -->
        <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
          <div class="flex flex-col md:flex-row gap-3">
            <input type="text" v-model="searchAkademik" placeholder="🔍 Cari Nama/NIM..." class="flex-1 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-indigo-400 outline-none">
            <select v-model="filterStatusAkademik" class="w-44 border border-slate-200 rounded-xl px-4 py-2.5 text-sm bg-white focus:ring-2 focus:ring-indigo-400 outline-none">
              <option value="">Semua Status</option>
              <option value="MENUNGGU">⏳ Menunggu</option>
              <option value="DISETUJUI">✅ Disetujui</option>
              <option value="DITOLAK">❌ Ditolak</option>
            </select>
            <button @click="resetFilterAkademik" class="bg-gray-200 hover:bg-gray-300 px-4 py-2.5 rounded-xl text-sm font-medium transition">Reset Filter</button>
          </div>
        </div>

        <!-- Tabel Akademik -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="p-4 border-b bg-indigo-50/50 flex justify-between items-center">
            <h3 class="font-bold text-indigo-900">📋 Data Mahasiswa Akademik</h3>
            <span class="text-xs bg-indigo-200 text-indigo-800 px-3 py-1 rounded-full">Total: {{ filteredAkademik.length }} mahasiswa</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead class="bg-gray-50 text-gray-500 text-[11px] uppercase">
                <tr>
                  <th class="px-5 py-3">Mahasiswa</th>
                  <th class="px-5 py-3">NIM</th>
                  <th class="px-5 py-3 text-center">Status Akademik</th>
                  <th class="px-5 py-3">Catatan</th>
                  <th class="px-5 py-3 text-center">Berkas</th>
                  <th class="px-5 py-3 text-center w-32">Aksi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="item in paginatedAkademik" :key="item.id || item.mahasiswa_id" class="hover:bg-gray-50 transition">
                  <td class="px-5 py-3 font-medium">{{ item.full_name || '-' }}</td>
                  <td class="px-5 py-3 font-mono text-sm">{{ item.nim || '-' }}</td>
                  <td class="px-5 py-3 text-center">
                    <span :class="getBadgeClass(item.status_akademik || item.status_akhir)" class="px-2 py-0.5 rounded-full text-[10px] font-bold">
                      {{ getStatusText(item.status_akademik || item.status_akhir || 'MENUNGGU') }}
                    </span>
                  </td>
                  <td class="px-5 py-3 text-sm max-w-[150px] truncate" :title="item.catatan_akademik">
                    {{ item.catatan_akademik || '-' }}
                  </td>
                  <td class="px-5 py-3 text-center">
                    <button @click="openBerkasAkademik(item)" class="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-lg text-xs font-bold hover:bg-indigo-200 transition">
                      📂 Lihat ({{ getAkademikFileCount(item) }})
                    </button>
                  </td>
                  <td class="px-5 py-3 text-center">
                    <div class="flex justify-center gap-1 flex-wrap">
                      <template v-if="(item.status_akademik || item.status_akhir) === 'MENUNGGU' || !item.status_akademik">
                        <button @click="bukaModalVerifikasiAkademik(item)" class="bg-indigo-600 hover:bg-indigo-700 text-white px-2 py-1 rounded-lg text-[10px] font-bold transition shadow-sm">✅ Verifikasi</button>
                      </template>
                      <template v-else-if="(item.status_akademik || item.status_akhir) === 'DISETUJUI'">
                        <button @click="openBerkasAkademik(item)" class="bg-slate-600 hover:bg-slate-700 text-white px-2 py-1 rounded-lg text-[10px] font-bold transition shadow-sm">📂 Detail</button>
                      </template>
                      <span v-else class="text-xs text-gray-400">-</span>
                    </div>
                  </td>
                </tr>
                <tr v-if="paginatedAkademik.length === 0">
                  <td colspan="6" class="px-5 py-10 text-center text-gray-400">📭 Tidak ada data mahasiswa akademik</td>
                </tr>
              </tbody>
            </table>
          </div>
          <!-- Pagination -->
          <div class="px-5 py-3 border-t flex flex-wrap gap-3 justify-between items-center bg-gray-50 text-sm">
            <span class="text-gray-500">Menampilkan {{ ((currentPageAkademik-1)*rowsPerPageAkademik)+1 }} - {{ Math.min(currentPageAkademik*rowsPerPageAkademik, filteredAkademik.length) }} dari {{ filteredAkademik.length }} data</span>
            <div class="flex gap-2 items-center">
              <button @click="prevPageAkademik" :disabled="currentPageAkademik===1" class="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-100 transition">Prev</button>
              <span class="text-sm">Halaman {{ currentPageAkademik }} / {{ totalPagesAkademik }}</span>
              <button @click="nextPageAkademik" :disabled="currentPageAkademik===totalPagesAkademik" class="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-100 transition">Next</button>
            </div>
            <select v-model="rowsPerPageAkademik" class="border rounded-lg px-2 py-1 text-sm bg-white">
              <option :value="10">10</option>
              <option :value="25">25</option>
              <option :value="50">50</option>
            </select>
          </div>
        </div>
      </div>

      <!-- ===== VERIFIKASI TRANSKRIP (seperti BAAK) ===== -->
      <div v-if="view === 'transkrip'" class="space-y-6 animate-in fade-in duration-500">
        <header class="mb-4 flex justify-between items-center">
          <div>
            <h1 class="text-3xl font-black text-slate-800">📝 Verifikasi Transkrip Nilai</h1>
            <p class="text-slate-500">Validasi transkrip nilai yang diajukan oleh mahasiswa.</p>
          </div>
          <button @click="fetchTranskrip" class="px-4 py-2 bg-white border border-slate-200 rounded-xl text-xs font-bold hover:bg-slate-50 flex items-center gap-2 transition">
            <span :class="{'animate-spin': loading}">🔄</span> Refresh
          </button>
        </header>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-white p-4 rounded-xl shadow-sm border-l-4 border-orange-500">
            <p class="text-xs text-gray-400 uppercase tracking-wide">Antrian Menunggu</p>
            <h3 class="text-2xl font-bold text-orange-600">{{ transkripMenungguCount }}</h3>
          </div>
          <div class="bg-white p-4 rounded-xl shadow-sm border-l-4 border-green-500">
            <p class="text-xs text-gray-400 uppercase tracking-wide">Disetujui</p>
            <h3 class="text-2xl font-bold text-green-600">{{ transkripDisetujuiCount }}</h3>
          </div>
          <div class="bg-white p-4 rounded-xl shadow-sm border-l-4 border-red-500">
            <p class="text-xs text-gray-400 uppercase tracking-wide">Ditolak</p>
            <h3 class="text-2xl font-bold text-red-600">{{ transkripDitolakCount }}</h3>
          </div>
        </div>
        <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
          <div class="flex flex-col md:flex-row gap-3">
            <input type="text" v-model="searchTranskrip" placeholder="🔍 Cari Nama/NIM..." class="flex-1 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-indigo-400 outline-none">
            <select v-model="filterStatusTranskrip" class="w-44 border border-slate-200 rounded-xl px-4 py-2.5 text-sm bg-white focus:ring-2 focus:ring-indigo-400 outline-none">
              <option value="">Semua Status</option>
              <option value="MENUNGGU">⏳ Menunggu</option>
              <option value="DISETUJUI">✅ Disetujui</option>
              <option value="DITOLAK">❌ Ditolak</option>
            </select>
            <button @click="resetFilterTranskrip" class="bg-gray-200 hover:bg-gray-300 px-4 py-2.5 rounded-xl text-sm font-medium transition">Reset Filter</button>
          </div>
        </div>
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="p-4 border-b bg-indigo-50/50 flex justify-between items-center">
            <h3 class="font-bold text-indigo-900">📄 Data Transkrip Nilai</h3>
            <span class="text-xs bg-indigo-200 text-indigo-800 px-3 py-1 rounded-full">Total: {{ filteredTranskrip.length }} data</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead class="bg-gray-50 text-gray-500 text-[11px] uppercase">
                <tr>
                  <th class="px-5 py-3">Mahasiswa</th>
                  <th class="px-5 py-3">NIM</th>
                  <th class="px-5 py-3">File Transkrip & Nilai</th>
                  <th class="px-5 py-3 text-center w-28">Status</th>
                  <th class="px-5 py-3">Catatan</th>
                  <th class="px-5 py-3 text-center w-32">Aksi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="item in paginatedTranskrip" :key="item.id" class="hover:bg-gray-50 transition">
                  <td class="px-5 py-3 font-medium">{{ item.full_name || '-' }}</td>
                  <td class="px-5 py-3 font-mono text-sm">{{ item.nim || '-' }}</td>
                  <td class="px-5 py-3">
                    <div class="flex flex-col gap-1">
                      <!-- Link PDF jika ada -->
                      <a v-if="getFileUrl(item)" :href="getFileUrl(item)" target="_blank" class="text-indigo-600 hover:underline inline-flex items-center gap-1 text-sm">📄 Lihat PDF</a>
                      
                      <!-- Tombol Lihat Nilai & Edit Nilai jika ada data nilai -->
                      <div v-if="item.data_nilai && item.data_nilai.length > 0" class="flex flex-wrap gap-1 mt-1">
                        <button @click="bukaDetailNilai(item)" class="bg-indigo-100 text-indigo-700 hover:bg-indigo-200 px-2 py-0.5 rounded text-[10px] font-bold transition">📋 Lihat Nilai</button>
                        <button @click="openEditNilaiModal(item.id, item.full_name, item.data_nilai)" class="bg-amber-100 text-amber-700 hover:bg-amber-200 px-2 py-0.5 rounded text-[10px] font-bold transition shadow-sm">✏️ Edit Nilai</button>
                      </div>
                      
                      <span v-if="!item.file_transkrip && (!item.data_nilai || item.data_nilai.length === 0)" class="text-gray-400 text-sm">-</span>
                    </div>
                  </td>
                  <td class="px-5 py-3 text-center">
                    <span :class="getBadgeClass(getStatus(item))" class="px-2 py-0.5 rounded-full text-[10px] font-bold">
                      {{ getStatusText(getStatus(item)) }}
                    </span>
                  </td>
                  <td class="px-5 py-3 text-sm max-w-[200px] truncate" :title="item.catatan_baak || item.catatan_dpa">
                    {{ item.catatan_baak || item.catatan_dpa || '-' }}
                  </td>
                  <td class="px-5 py-3 text-center">
                    <div class="flex justify-center gap-1 flex-wrap">
                      <template v-if="getStatus(item) === 'MENUNGGU'">
                        <button @click="verifikasiTranskrip(item.id, 'DISETUJUI')" class="bg-green-500 hover:bg-green-600 text-white px-2 py-1 rounded-lg text-[10px] font-bold transition shadow-sm">✅ Setujui</button>
                        <button @click="openTolakTranskripModal(item.id, item.full_name)" class="bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded-lg text-[10px] font-bold transition shadow-sm">❌ Tolak</button>
                      </template>
                      <template v-else>
                        <button v-if="item.data_nilai && item.data_nilai.length > 0" @click="bukaDetailNilai(item)" class="bg-slate-600 hover:bg-slate-700 text-white px-2 py-1 rounded-lg text-[10px] font-bold transition shadow-sm">📋 Detail</button>
                        <button v-else @click="bukaDetailTranskrip(item)" class="bg-slate-600 hover:bg-slate-700 text-white px-2 py-1 rounded-lg text-[10px] font-bold transition shadow-sm">📋 Detail</button>
                      </template>
                    </div>
                  </td>
                </tr>
                <tr v-if="paginatedTranskrip.length === 0">
                  <td colspan="6" class="px-5 py-10 text-center text-gray-400">📭 Tidak ada data transkrip</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="px-5 py-3 border-t flex flex-wrap gap-3 justify-between items-center bg-gray-50 text-sm">
            <span class="text-gray-500">Menampilkan {{ ((currentPageTranskrip-1)*rowsPerPageTranskrip)+1 }} - {{ Math.min(currentPageTranskrip*rowsPerPageTranskrip, filteredTranskrip.length) }} dari {{ filteredTranskrip.length }} data</span>
            <div class="flex gap-2 items-center">
              <button @click="prevPageTranskrip" :disabled="currentPageTranskrip===1" class="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-100 transition">Prev</button>
              <span class="text-sm">Halaman {{ currentPageTranskrip }} / {{ totalPagesTranskrip }}</span>
              <button @click="nextPageTranskrip" :disabled="currentPageTranskrip===totalPagesTranskrip" class="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-100 transition">Next</button>
            </div>
            <select v-model="rowsPerPageTranskrip" class="border rounded-lg px-2 py-1 text-sm bg-white">
              <option :value="10">10</option>
              <option :value="25">25</option>
              <option :value="50">50</option>
            </select>
          </div>
        </div>
      </div>

      <!-- ===== VERIFIKASI PENDAFTARAN YUDISIUM ===== -->
      <div v-if="view === 'pendaftaran'" class="space-y-6 animate-in fade-in duration-500">
        <header class="mb-4 flex justify-between items-center flex-wrap gap-3">
          <div>
            <h1 class="text-3xl font-black text-slate-800">📋 Verifikasi Pendaftaran Yudisium</h1>
            <p class="text-slate-500">Validasi pendaftaran yudisium final sebelum kelulusan.</p>
          </div>
          <div class="flex gap-2">
            <button @click="fetchPendaftaran" class="px-4 py-2 bg-white border border-slate-200 rounded-xl text-xs font-bold hover:bg-slate-50 flex items-center gap-2 transition">
              <span :class="{'animate-spin': loading}">🔄</span> Refresh
            </button>
          </div>
        </header>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-white p-4 rounded-xl shadow-sm border-l-4 border-orange-500">
            <p class="text-xs text-gray-400 uppercase tracking-wide">Menunggu Verifikasi</p>
            <h3 class="text-2xl font-bold text-orange-600">{{ pendaftaranMenungguCount }}</h3>
          </div>
          <div class="bg-white p-4 rounded-xl shadow-sm border-l-4 border-green-500">
            <p class="text-xs text-gray-400 uppercase tracking-wide">Sudah Diverifikasi</p>
            <h3 class="text-2xl font-bold text-green-600">{{ pendaftaranDiverifikasiCount }}</h3>
          </div>
          <div class="bg-white p-4 rounded-xl shadow-sm border-l-4 border-indigo-500">
            <p class="text-xs text-gray-400 uppercase tracking-wide">Total Pendaftaran</p>
            <h3 class="text-2xl font-bold text-indigo-600">{{ filteredPendaftaran.length }}</h3>
          </div>
        </div>
        <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
          <div class="flex flex-col md:flex-row gap-3">
            <input type="text" v-model="searchPendaftaran" placeholder="🔍 Cari Nama/NIM..." class="flex-1 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-indigo-400 outline-none">
            <button @click="resetFilterPendaftaran" class="bg-gray-200 hover:bg-gray-300 px-4 py-2.5 rounded-xl text-sm font-medium transition">Reset Filter</button>
          </div>
        </div>
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="p-4 border-b bg-indigo-50/50 flex justify-between items-center">
            <h3 class="font-bold text-indigo-900">📋 Data Pendaftaran Yudisium</h3>
            <span class="text-xs bg-indigo-200 text-indigo-800 px-3 py-1 rounded-full">Total: {{ filteredPendaftaran.length }} pendaftaran</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead class="bg-gray-50 text-gray-500 text-[11px] uppercase">
                <tr>
                  <th class="px-5 py-3">Mahasiswa</th>
                  <th class="px-5 py-3">NIM</th>
                  <th class="px-5 py-3">Status</th>
                  <th class="px-5 py-3">Catatan BAAK</th>
                  <th class="px-5 py-3 text-center w-24">Aksi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="item in paginatedPendaftaran" :key="item.id" class="hover:bg-gray-50 transition">
                  <td class="px-5 py-3 font-medium">{{ item.mahasiswa_nama || item.nama_lengkap || '-' }}</td>
                  <td class="px-5 py-3 font-mono text-sm">{{ item.nim || '-' }}</td>
                  <td class="px-5 py-3">
                    <span :class="getBadgeClass(item.status)" class="px-2 py-0.5 rounded-full text-[10px] font-bold">
                      {{ getStatusText(item.status) }}
                    </span>
                  </td>
                  <td class="px-5 py-3 text-sm max-w-[200px] truncate" :title="item.catatan_baak">
                    {{ item.catatan_baak || '-' }}
                  </td>
                  <td class="px-5 py-3 text-center">
                    <button @click="bukaModalKomentarPendaftaran(item)" 
                            :class="item.status === 'MENUNGGU' ? 'bg-indigo-600 hover:bg-indigo-700' : 'bg-slate-600 hover:bg-slate-700'"
                            class="text-white px-3 py-1.5 rounded-lg text-xs font-bold transition shadow-sm">
                      {{ item.status === 'MENUNGGU' ? '💬 Verifikasi' : '📋 Lihat' }}
                    </button>
                  </td>
                </tr>
                <tr v-if="paginatedPendaftaran.length === 0">
                  <td colspan="5" class="px-5 py-10 text-center text-gray-400">📭 Tidak ada data pendaftaran</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="px-5 py-3 border-t flex flex-wrap gap-3 justify-between items-center bg-gray-50 text-sm">
            <span class="text-gray-500">Menampilkan {{ ((currentPagePendaftaran-1)*rowsPerPagePendaftaran)+1 }} - {{ Math.min(currentPagePendaftaran*rowsPerPagePendaftaran, filteredPendaftaran.length) }} dari {{ filteredPendaftaran.length }} data</span>
            <div class="flex gap-2 items-center">
              <button @click="prevPagePendaftaran" :disabled="currentPagePendaftaran===1" class="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-100 transition">Prev</button>
              <span class="text-sm">Halaman {{ currentPagePendaftaran }} / {{ totalPagesPendaftaran }}</span>
              <button @click="nextPagePendaftaran" :disabled="currentPagePendaftaran===totalPagesPendaftaran" class="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-100 transition">Next</button>
            </div>
            <select v-model="rowsPerPagePendaftaran" class="border rounded-lg px-2 py-1 text-sm bg-white">
              <option :value="10">10</option>
              <option :value="25">25</option>
              <option :value="50">50</option>
            </select>
          </div>
        </div>
      </div>

      <!-- ===== VERIFIKASI PERPUSTAKAAN ===== -->
      <div v-if="view === 'perpus'" class="space-y-6 animate-in fade-in duration-500">
        <header class="mb-4 flex justify-between items-center flex-wrap gap-3">
          <div>
            <h1 class="text-3xl font-black text-slate-800">📚 Verifikasi Bebas Perpustakaan</h1>
            <p class="text-slate-500">Validasi pengajuan bebas perpustakaan dan kirim surat.</p>
          </div>
          <div class="flex gap-2">
            <button @click="fetchPerpus" class="px-4 py-2 bg-white border border-slate-200 rounded-xl text-xs font-bold hover:bg-slate-50 flex items-center gap-2 transition">
              <span :class="{'animate-spin': loading}">🔄</span> Refresh
            </button>
            <button @click="openTemplateModalPerpus" class="px-4 py-2 bg-amber-500 hover:bg-amber-600 text-white rounded-xl text-xs font-bold transition shadow-md flex items-center gap-2">📝 Template Surat</button>
            <button @click="openTtdModalPerpus" class="px-4 py-2 bg-indigo-500 hover:bg-indigo-600 text-white rounded-xl text-xs font-bold transition shadow-md flex items-center gap-2">✍️ Tanda Tangan</button>
          </div>
        </header>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-white p-4 rounded-xl shadow-sm border-l-4 border-orange-500">
            <p class="text-xs text-gray-400 uppercase tracking-wide">Menunggu Verifikasi</p>
            <h3 class="text-2xl font-bold text-orange-600">{{ perpusMenungguCount }}</h3>
          </div>
          <div class="bg-white p-4 rounded-xl shadow-sm border-l-4 border-green-500">
            <p class="text-xs text-gray-400 uppercase tracking-wide">Sudah Disetujui</p>
            <h3 class="text-2xl font-bold text-green-600">{{ perpusDisetujuiCount }}</h3>
          </div>
          <div class="bg-white p-4 rounded-xl shadow-sm border-l-4 border-red-500">
            <p class="text-xs text-gray-400 uppercase tracking-wide">Ditolak</p>
            <h3 class="text-2xl font-bold text-red-600">{{ perpusDitolakCount }}</h3>
          </div>
        </div>
        <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200">
          <div class="flex flex-col md:flex-row gap-3">
            <input type="text" v-model="searchPerpus" placeholder="🔍 Cari Nama/NIM..." class="flex-1 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-indigo-400 outline-none">
            <select v-model="filterStatusPerpus" class="w-44 border border-slate-200 rounded-xl px-4 py-2.5 text-sm bg-white focus:ring-2 focus:ring-indigo-400 outline-none">
              <option value="">Semua Status</option>
              <option value="MENUNGGU">⏳ Menunggu</option>
              <option value="DISETUJUI">✅ Disetujui</option>
              <option value="DITOLAK">❌ Ditolak</option>
            </select>
            <button @click="resetFilterPerpus" class="bg-gray-200 hover:bg-gray-300 px-4 py-2.5 rounded-xl text-sm font-medium transition">Reset Filter</button>
          </div>
        </div>
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="p-4 border-b bg-indigo-50/50 flex justify-between items-center">
            <h3 class="font-bold text-indigo-900">📋 Daftar Pengajuan Perpustakaan</h3>
            <span class="text-xs bg-indigo-200 text-indigo-800 px-3 py-1 rounded-full">Total: {{ filteredPerpus.length }} data</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead class="bg-gray-50 text-gray-500 text-[11px] uppercase">
                <tr>
                  <th class="px-5 py-3">Mahasiswa</th>
                  <th class="px-5 py-3">NIM</th>
                  <th class="px-5 py-3">Status</th>
                  <th class="px-5 py-3">Catatan</th>
                  <th class="px-5 py-3 text-center">Berkas</th>
                  <th class="px-5 py-3 text-center w-32">Aksi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="item in paginatedPerpus" :key="item.id" class="hover:bg-gray-50 transition">
                  <td class="px-5 py-3 font-medium">{{ item.full_name || '-' }}</td>
                  <td class="px-5 py-3 font-mono text-sm">{{ item.nim || '-' }}</td>
                  <td class="px-5 py-3">
                    <span :class="getBadgeClass(item.status)" class="px-2 py-0.5 rounded-full text-[10px] font-bold">
                      {{ getStatusText(item.status) }}
                    </span>
                  </td>
                  <td class="px-5 py-3 text-sm max-w-[150px] truncate" :title="item.catatan_perpus">
                    {{ item.catatan_perpus || '-' }}
                  </td>
                  <td class="px-5 py-3 text-center">
                    <button @click="openBerkasModalPerpus(item)" class="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-lg text-xs font-bold hover:bg-indigo-200 transition">
                      📂 Lihat ({{ getAllFilesCount(item) }})
                    </button>
                  </td>
                  <td class="px-5 py-3 text-center">
                    <div class="flex justify-center gap-1 flex-wrap">
                      <template v-if="item.status === 'MENUNGGU'">
                        <button @click="setujuiPerpus(item)" class="bg-green-500 hover:bg-green-600 text-white px-2 py-1 rounded-lg text-[10px] font-bold transition shadow-sm">✅ Setujui</button>
                        <button @click="openTolakPerpusModal(item.id, item.full_name)" class="bg-red-500 hover:bg-red-600 text-white px-2 py-1 rounded-lg text-[10px] font-bold transition shadow-sm">❌ Tolak</button>
                      </template>
                      <template v-else-if="item.status === 'DISETUJUI'">
                        <button @click="bukaModalSuratPerpus(item)" class="bg-teal-600 hover:bg-teal-700 text-white px-2 py-1 rounded-lg text-[10px] font-bold transition shadow-sm">📄 Surat</button>
                        <button @click="openBerkasModalPerpus(item)" class="bg-indigo-600 hover:bg-indigo-700 text-white px-2 py-1 rounded-lg text-[10px] font-bold transition shadow-sm">📂 Detail</button>
                      </template>
                      <span v-else class="text-xs text-gray-400">-</span>
                    </div>
                  </td>
                </tr>
                <tr v-if="paginatedPerpus.length === 0">
                  <td colspan="6" class="px-5 py-10 text-center text-gray-400">📭 Tidak ada data pengajuan perpustakaan</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="px-5 py-3 border-t flex flex-wrap gap-3 justify-between items-center bg-gray-50 text-sm">
            <span class="text-gray-500">Menampilkan {{ ((currentPagePerpus-1)*rowsPerPagePerpus)+1 }} - {{ Math.min(currentPagePerpus*rowsPerPagePerpus, filteredPerpus.length) }} dari {{ filteredPerpus.length }} data</span>
            <div class="flex gap-2 items-center">
              <button @click="prevPagePerpus" :disabled="currentPagePerpus===1" class="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-100 transition">Prev</button>
              <span class="text-sm">Halaman {{ currentPagePerpus }} / {{ totalPagesPerpus }}</span>
              <button @click="nextPagePerpus" :disabled="currentPagePerpus===totalPagesPerpus" class="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-100 transition">Next</button>
            </div>
            <select v-model="rowsPerPagePerpus" class="border rounded-lg px-2 py-1 text-sm bg-white">
              <option :value="10">10</option>
              <option :value="25">25</option>
              <option :value="50">50</option>
            </select>
          </div>
        </div>
      </div>

      <!-- ===== PERIODE VIEW ===== -->
      <div v-if="view === 'periode'" class="animate-in fade-in duration-500">
        <header class="mb-8 flex justify-between items-center">
          <div>
            <h1 class="text-3xl font-black text-slate-800">📅 Periode Yudisium</h1>
            <p class="text-slate-500">Kelola periode pendaftaran yudisium.</p>
          </div>
          <button @click="bukaFormPeriode()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-xl text-sm font-bold shadow-md transition flex items-center gap-2">
            <span>➕</span> Tambah Periode
          </button>
        </header>
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
          <table class="w-full text-left">
            <thead class="bg-slate-50 text-slate-400 text-[10px] uppercase font-bold">
              <tr>
                <th class="px-6 py-4">Nama Periode</th>
                <th class="px-6 py-4">Tanggal Mulai</th>
                <th class="px-6 py-4">Tanggal Selesai</th>
                <th class="px-6 py-4 text-center">Status</th>
                <th class="px-6 py-4 text-center">Aksi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="periode in listPeriode" :key="periode.id" class="hover:bg-slate-50 transition">
                <td class="px-6 py-4 font-bold">{{ periode.nama_periode }}</td>
                <td class="px-6 py-4">{{ formatDate(periode.tanggal_mulai) }}</td>
                <td class="px-6 py-4">{{ formatDate(periode.tanggal_selesai) }}</td>
                <td class="px-6 py-4 text-center">
                  <span :class="periode.is_active ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-500'"
                        class="px-2 py-1 rounded text-[10px] font-bold uppercase">
                    {{ periode.is_active ? 'AKTIF' : 'TIDAK AKTIF' }}
                  </span>
                </td>
                <td class="px-6 py-4 text-center">
                  <div class="flex justify-center gap-2">
                    <button @click="toggleAktif(periode)" 
                            :class="periode.is_active ? 'bg-amber-500 hover:bg-amber-600' : 'bg-emerald-500 hover:bg-emerald-600'"
                            class="text-white px-3 py-1.5 rounded-lg text-xs font-bold transition shadow-sm">
                      {{ periode.is_active ? 'Nonaktifkan' : 'Aktifkan' }}
                    </button>
                    <button @click="bukaFormPeriode(periode)" 
                            class="bg-indigo-500 hover:bg-indigo-600 text-white px-3 py-1.5 rounded-lg text-xs font-bold transition shadow-sm">✏️ Edit</button>
                    <button @click="hapusPeriode(periode.id)" 
                            class="bg-red-500 hover:bg-red-600 text-white px-3 py-1.5 rounded-lg text-xs font-bold transition shadow-sm">🗑️ Hapus</button>
                  </div>
                </td>
              </tr>
              <tr v-if="listPeriode.length === 0">
                <td colspan="5" class="px-6 py-10 text-center text-slate-400 italic">Belum ada periode yudisium.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>

    <!-- ===== MODAL-MODAL ===== -->

    <!-- MODAL EDIT USER -->
    <div v-if="showEditModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center z-[60] p-4">
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-md overflow-hidden animate-in zoom-in-95 duration-200">
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <h3 class="font-black text-slate-800 uppercase text-sm">Modifikasi Data Akun</h3>
          <button @click="showEditModal = false" class="text-slate-400 hover:text-slate-600">✕</button>
        </div>
        <div class="p-8 space-y-5">
          <div>
            <label class="block text-[10px] font-black text-slate-400 uppercase mb-2">Nama Lengkap</label>
            <input v-model="editUser.full_name" type="text" class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none font-bold">
          </div>
          <div>
            <label class="block text-[10px] font-black text-slate-400 uppercase mb-2">Username Baru / ID</label>
            <input v-model="editUser.username" type="text" class="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none font-mono">
          </div>
          <div>
            <label class="block text-[10px] font-black text-slate-400 uppercase mb-3">Tingkatan Hak Akses</label>
            <div class="grid grid-cols-2 gap-2">
              <button v-for="r in roles" :key="r" type="button" @click="editUser.role = r"
                :class="editUser.role === r ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'"
                class="py-2.5 px-3 border rounded-xl text-[9px] font-black transition uppercase shadow-sm">
                {{ r }}
              </button>
            </div>
          </div>
        </div>
        <div class="p-6 bg-slate-50 flex gap-3">
          <button @click="showEditModal = false" class="flex-1 py-3 text-slate-500 font-bold hover:bg-slate-100 rounded-xl transition">Batal</button>
          <button @click="submitEdit" :disabled="loading" class="flex-1 py-3 bg-indigo-600 text-white font-black rounded-xl hover:bg-indigo-700 transition shadow-lg shadow-indigo-200">
            {{ loading ? 'MENYIMPAN...' : 'SIMPAN PERUBAHAN' }}
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL VERIFIKASI AKADEMIK -->
    <div v-if="showVerifikasiAkademikModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center z-[70] p-4" @click.self="showVerifikasiAkademikModal = false">
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-lg overflow-hidden animate-in fade-in duration-300">
        <div class="p-6 border-b flex justify-between items-center bg-rose-600 text-white">
          <h3 class="font-black uppercase tracking-widest text-sm">Verifikasi Berkas Akademik</h3>
          <button @click="showVerifikasiAkademikModal = false" class="text-white/50 hover:text-white">✕</button>
        </div>
        <div class="p-8 space-y-6">
          <div class="flex items-center gap-4 border-b border-slate-100 pb-4">
            <div class="w-16 h-16 bg-slate-100 rounded-2xl flex items-center justify-center text-2xl">🎓</div>
            <div>
              <h4 class="font-black text-xl text-slate-800">{{ selectedAkademik?.full_name }}</h4>
              <p class="text-rose-600 font-mono text-sm">{{ selectedAkademik?.nim }}</p>
            </div>
          </div>
          <div>
            <p class="text-xs font-black text-slate-400 uppercase mb-3">Dokumen Terlampir</p>
            <div class="grid grid-cols-2 gap-3">
              <div v-for="(doc, key) in akademikFileLabels" :key="key" 
                   class="p-3 border border-slate-200 rounded-lg bg-slate-50 flex justify-between items-center">
                <span class="text-[10px] font-bold text-slate-700">{{ doc }}</span>
                <a v-if="selectedAkademik && selectedAkademik[key]" :href="getFullImageUrl(selectedAkademik[key])" target="_blank" 
                   class="text-rose-600 bg-rose-50 px-2 py-1 rounded text-[10px] font-bold">Buka</a>
                <span v-else class="text-[10px] font-bold text-red-500 bg-red-50 px-2 py-1 rounded">KOSONG</span>
              </div>
            </div>
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Catatan (wajib jika ditolak)</label>
            <textarea v-model="formCatatanAkademik" rows="3" 
                      class="w-full border border-gray-200 rounded-lg p-3 text-sm outline-none focus:ring-2 focus:ring-rose-500"
                      placeholder="Masukkan catatan revisi jika ada..."></textarea>
          </div>
        </div>
        <div class="p-6 bg-slate-50 flex justify-end gap-3">
          <button @click="showVerifikasiAkademikModal = false" class="px-4 py-2 text-sm font-bold text-slate-500 hover:text-slate-700">Batal</button>
          <button @click="submitVerifikasiAkademik('DITOLAK')" class="px-4 py-2 bg-red-100 text-red-600 hover:bg-red-200 rounded-lg text-sm font-bold transition">Tolak / Revisi</button>
          <button @click="submitVerifikasiAkademik('DISETUJUI')" class="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg text-sm font-bold shadow-md transition">Setujui</button>
        </div>
      </div>
    </div>

    <!-- MODAL LIHAT BERKAS AKADEMIK -->
    <div v-if="showBerkasAkademikModal" class="fixed inset-0 bg-black/80 z-[100] flex items-center justify-center p-4" @click.self="showBerkasAkademikModal = false">
      <div class="bg-white rounded-2xl w-full max-w-4xl max-h-[85vh] flex flex-col shadow-2xl">
        <div class="p-5 bg-rose-600 text-white flex justify-between rounded-t-2xl">
          <div>
            <h3 class="font-bold text-lg flex items-center gap-2">📂 Semua Berkas Akademik - {{ selectedBerkasAkademik?.full_name }}</h3>
            <p class="text-xs text-rose-200">NIM: {{ selectedBerkasAkademik?.nim }}</p>
          </div>
          <button @click="showBerkasAkademikModal = false" class="text-white hover:text-red-400 transition text-xl">&times;</button>
        </div>
        <div class="flex-1 overflow-y-auto p-6 bg-gray-100">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-xs text-gray-400">Status Validasi</p>
                <p class="text-lg font-bold" :class="{
                  'text-green-600': selectedBerkasAkademik?.status_akademik === 'DISETUJUI',
                  'text-red-600': selectedBerkasAkademik?.status_akademik === 'DITOLAK',
                  'text-orange-600': selectedBerkasAkademik?.status_akademik === 'MENUNGGU' || !selectedBerkasAkademik?.status_akademik
                }">
                  {{ selectedBerkasAkademik?.status_akademik === 'DISETUJUI' ? '✅ DISETUJUI' : 
                     selectedBerkasAkademik?.status_akademik === 'DITOLAK' ? '❌ DITOLAK' : 
                     '⏳ MENUNGGU' }}
                </p>
              </div>
              <div class="text-right">
                <p class="text-xs text-gray-400">Terakhir Update</p>
                <p class="text-sm font-medium">{{ formatDate(selectedBerkasAkademik?.updated_at || selectedBerkasAkademik?.created_at) }}</p>
              </div>
            </div>
            <div v-if="selectedBerkasAkademik?.catatan_akademik" class="mt-3 p-2 bg-gray-50 rounded-lg text-xs text-gray-600">
              <span class="font-bold">Catatan:</span> {{ selectedBerkasAkademik.catatan_akademik }}
            </div>
          </div>
          <h4 class="font-bold text-gray-700 mb-4 flex items-center gap-2">📁 Semua Berkas</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="(label, key) in akademikFileLabels" :key="key" class="bg-white rounded-xl border border-gray-200 p-4 hover:shadow-md transition hover:border-rose-300">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="w-12 h-12 bg-rose-100 rounded-xl flex items-center justify-center"><span class="text-rose-600 text-xl">📄</span></div>
                  <div><p class="text-sm font-semibold text-gray-800">{{ label }}</p><p class="text-[10px] text-gray-400">PDF/Image</p></div>
                </div>
                <a v-if="selectedBerkasAkademik && selectedBerkasAkademik[key]" :href="getFullImageUrl(selectedBerkasAkademik[key])" target="_blank" class="bg-rose-600 text-white px-3 py-1.5 rounded-lg text-xs font-bold hover:bg-rose-700 transition">📄 Buka</a>
                <span v-else class="text-xs text-gray-400 italic">Kosong</span>
              </div>
            </div>
          </div>
        </div>
        <div class="p-4 bg-white border-t border-gray-200 flex justify-end gap-3 rounded-b-2xl">
          <button @click="showBerkasAkademikModal = false" class="px-5 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg text-sm font-bold transition">Tutup</button>
          <button v-if="(selectedBerkasAkademik?.status_akademik || selectedBerkasAkademik?.status_akhir) === 'MENUNGGU' || !selectedBerkasAkademik?.status_akademik" 
                  @click="showBerkasAkademikModal = false; bukaModalVerifikasiAkademik(selectedBerkasAkademik)" 
                  class="px-5 py-2 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-sm font-bold transition">✅ Verifikasi</button>
        </div>
      </div>
    </div>

    <!-- MODAL FORM MATA KULIAH -->
    <div v-if="isModalFormMkOpen" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto shadow-2xl">
        <div class="p-5 border-b bg-indigo-50 flex justify-between items-center">
          <h3 class="font-bold text-indigo-900 text-lg">{{ isEditMode ? '✏️ Edit Mata Kuliah' : '➕ Tambah Mata Kuliah' }}</h3>
          <button @click="isModalFormMkOpen=false" class="text-gray-400 hover:text-red-500 transition text-xl">&times;</button>
        </div>
        <form @submit.prevent="simpanMataKuliah" class="p-5 space-y-4">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-xs font-bold text-gray-600 block mb-1">Kode MK</label>
              <input type="text" v-model="formMk.kode" required :disabled="isEditMode" class="w-full border border-gray-200 rounded-xl p-2.5 text-sm focus:ring-2 focus:ring-indigo-400 outline-none">
            </div>
            <div>
              <label class="text-xs font-bold text-gray-600 block mb-1">SKS</label>
              <input type="number" v-model="formMk.sks" required class="w-full border border-gray-200 rounded-xl p-2.5 text-sm focus:ring-2 focus:ring-indigo-400 outline-none">
            </div>
          </div>
          <div>
            <label class="text-xs font-bold text-gray-600 block mb-1">Nama Mata Kuliah</label>
            <input type="text" v-model="formMk.nama" required class="w-full border border-gray-200 rounded-xl p-2.5 text-sm focus:ring-2 focus:ring-indigo-400 outline-none">
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-xs font-bold text-gray-600 block mb-1">Kategori</label>
              <select v-model="formMk.kategori" class="w-full border border-gray-200 rounded-xl p-2.5 text-sm bg-white focus:ring-2 focus:ring-indigo-400 outline-none">
                <option value="Wajib">Wajib</option>
                <option value="Pilihan">Pilihan</option>
                <option value="TA">Tugas Akhir</option>
              </select>
            </div>
            <div>
              <label class="text-xs font-bold text-gray-600 block mb-1">Jurusan</label>
              <select v-model="formMk.jurusan" class="w-full border border-gray-200 rounded-xl p-2.5 text-sm bg-white focus:ring-2 focus:ring-indigo-400 outline-none">
                <option value="Semua Jurusan">Semua Jurusan</option>
                <option value="Akuntansi">Akuntansi</option>
                <option value="Manajemen">Manajemen</option>
              </select>
            </div>
          </div>
          <div v-if="formMk.kategori === 'Pilihan'">
            <label class="text-xs font-bold text-gray-600 block mb-1">Peminatan</label>
            <input type="text" v-model="formMk.kelompok" placeholder="Contoh: Akuntansi Keuangan" class="w-full border border-gray-200 rounded-xl p-2.5 text-sm focus:ring-2 focus:ring-indigo-400 outline-none">
          </div>
          <div v-if="formMk.kategori === 'TA'">
            <label class="text-xs font-bold text-gray-600 block mb-1">Jalur TA</label>
            <input type="text" v-model="formMk.kelompok" placeholder="Contoh: Skripsi / Magang" class="w-full border border-gray-200 rounded-xl p-2.5 text-sm focus:ring-2 focus:ring-indigo-400 outline-none">
          </div>
          <div class="flex justify-end gap-2 pt-3">
            <button type="button" @click="isModalFormMkOpen=false" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-xl text-sm font-medium transition">Batal</button>
            <button type="submit" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-bold transition shadow-md">Simpan</button>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL TOLAK TRANSKRIP -->
    <div v-if="showTolakTranskripModal" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl w-full max-w-md shadow-2xl">
        <div class="p-5 border-b bg-red-50 flex justify-between items-center">
          <h3 class="font-bold text-red-800">❌ Tolak Transkrip</h3>
          <button @click="showTolakTranskripModal=false" class="text-gray-400 hover:text-red-500 transition text-xl">&times;</button>
        </div>
        <div class="p-5">
          <textarea v-model="catatanTolakTranskrip" placeholder="Alasan penolakan..." class="w-full border border-gray-200 rounded-xl p-3 h-28 focus:ring-2 focus:ring-red-400 outline-none"></textarea>
        </div>
        <div class="p-4 border-t bg-gray-50 flex justify-end gap-2 rounded-b-2xl">
          <button @click="showTolakTranskripModal=false" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-xl text-sm font-medium transition">Batal</button>
          <button @click="confirmTolakTranskrip" class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-xl text-sm font-bold transition shadow-md">Tolak</button>
        </div>
      </div>
    </div>

    <!-- MODAL DETAIL NILAI TRANSKRIP (dengan Revisi) -->
    <div v-if="showDetailNilaiModal" class="fixed inset-0 bg-black/70 z-[60] flex items-center justify-center p-4 backdrop-blur-sm" @click.self="showDetailNilaiModal = false">
      <div class="bg-white rounded-xl shadow-2xl w-full max-w-4xl max-h-[80vh] flex flex-col overflow-hidden animate-fadeIn">
        <div class="bg-indigo-700 text-white p-4 flex justify-between items-center">
          <div>
            <h3 class="font-bold text-lg flex items-center gap-2">📊 Detail Transkrip Nilai</h3>
            <p class="text-xs text-indigo-200">{{ selectedNilaiItem?.full_name }} ({{ selectedNilaiItem?.nim }})</p>
          </div>
          <button @click="showDetailNilaiModal = false" class="text-white hover:text-red-300 text-2xl">&times;</button>
        </div>
        <div class="flex-1 overflow-y-auto p-5 bg-gray-50">
          <div class="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
            <table class="w-full text-left border-collapse">
              <thead class="bg-gray-100 text-gray-500 text-[10px] uppercase font-bold">
                <tr>
                  <th class="px-4 py-3">Kode</th>
                  <th class="px-4 py-3">Mata Kuliah</th>
                  <th class="px-4 py-3 text-center">SKS</th>
                  <th class="px-4 py-3 text-center bg-gray-200">Nilai Asli</th>
                  <th class="px-4 py-3 text-center bg-amber-100">Nilai Revisi</th>
                  <th class="px-4 py-3 text-center bg-green-100">Nilai Akhir</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="nilai in (selectedNilaiItem?.data_nilai || [])" :key="nilai.kode_mk || nilai.kode" class="hover:bg-gray-50 transition">
                  <td class="px-4 py-2 font-mono text-sm text-gray-600">{{ nilai.kode_mk || nilai.kode }}</td>
                  <td class="px-4 py-2 font-medium text-gray-800">{{ nilai.nama_mk || nilai.nama }}</td>
                  <td class="px-4 py-2 text-center">{{ nilai.sks }}</td>
                  <td class="px-4 py-2 text-center bg-gray-50 font-bold text-gray-700">{{ nilai.nilai || nilai.huruf || '-' }}</td>
                  <td class="px-4 py-2 text-center bg-amber-50 font-bold text-amber-700">{{ nilai.nilai_revisi || '-' }}</td>
                  <td class="px-4 py-2 text-center bg-green-50 font-bold text-green-700">{{ nilai.nilai_revisi || nilai.nilai || '-' }}</td>
                </tr>
                <tr v-if="(selectedNilaiItem?.data_nilai || []).length === 0">
                  <td colspan="6" class="px-4 py-8 text-center text-gray-400 italic">Tidak ada data nilai</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="(selectedNilaiItem?.data_nilai || []).filter(i => i.nilai_revisi).length > 0" class="mt-4 p-3 bg-amber-50 rounded-xl border border-amber-200">
            <p class="font-bold text-amber-700">📝 Ringkasan Perubahan:</p>
            <ul class="text-sm">
              <li v-for="item in (selectedNilaiItem?.data_nilai || []).filter(i => i.nilai_revisi)" :key="item.kode_mk || item.kode">
                • {{ item.nama_mk || item.nama }}: {{ item.nilai || item.huruf }} → {{ item.nilai_revisi }}
              </li>
            </ul>
          </div>
        </div>
        <div class="p-4 bg-white border-t border-gray-200 flex justify-end">
          <button @click="showDetailNilaiModal = false" class="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-bold transition">Tutup</button>
        </div>
      </div>
    </div>

    <!-- MODAL EDIT NILAI (Baru) -->
    <div v-if="showEditNilaiModal" class="fixed inset-0 z-[70] bg-black/50 flex items-center justify-center p-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl w-full max-w-6xl max-h-[85vh] flex flex-col shadow-2xl">
        <div class="p-5 bg-gradient-to-r from-amber-600 to-amber-700 text-white flex justify-between rounded-t-2xl">
          <div>
            <h3 class="font-bold">✏️ Edit & Revisi Nilai - {{ editNilaiMhsName }}</h3>
            <p class="text-xs text-amber-100">⚠️ Nilai asli mahasiswa tetap tersimpan. Super Admin dapat menambah kolom baru dan merevisi nilai.</p>
          </div>
          <button @click="tutupEditNilaiModal" class="text-white hover:text-red-300 transition text-xl">&times;</button>
        </div>

        <div class="flex-1 overflow-y-auto p-5">
          <!-- Tab -->
          <div class="flex border-b mb-4 gap-4">
            <button @click="tabEditMode = 'revisi'" :class="tabEditMode === 'revisi' ? 'border-b-2 border-amber-500 text-amber-600' : 'text-gray-500'" class="px-4 py-2 font-medium text-sm transition">📝 Revisi Nilai</button>
            <button @click="tabEditMode = 'tambah'" :class="tabEditMode === 'tambah' ? 'border-b-2 border-amber-500 text-amber-600' : 'text-gray-500'" class="px-4 py-2 font-medium text-sm transition">➕ Tambah Mata Kuliah Baru</button>
          </div>

          <!-- Tab Revisi -->
          <div v-if="tabEditMode === 'revisi'">
            <div class="mb-3 bg-blue-50 p-3 rounded-xl text-sm border border-blue-200">
              <p class="font-bold text-blue-700">ℹ️ Informasi:</p>
              <p class="text-blue-600">Nilai asli dari mahasiswa tetap tersimpan di sistem. Pilih nilai revisi untuk mengganti nilai akhir.</p>
            </div>
            <div class="overflow-x-auto border rounded-xl">
              <table class="w-full text-sm border-collapse">
                <thead class="bg-gray-100 sticky top-0">
                  <tr>
                    <th class="p-3 text-left">Kode</th>
                    <th class="p-3 text-left">Mata Kuliah</th>
                    <th class="p-3 text-center">SKS</th>
                    <th class="p-3 text-center bg-gray-200">Nilai Asli</th>
                    <th class="p-3 text-center bg-amber-100">Nilai Revisi</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, idx) in editNilaiData" :key="idx" class="border-b">
                    <td class="p-3 font-mono text-xs">{{ item.kode_mk }}</td>
                    <td class="p-3 font-medium">{{ item.nama_mk }}</td>
                    <td class="p-3 text-center">{{ item.sks }}</td>
                    <td class="p-3 text-center bg-gray-50 font-bold text-gray-700">{{ item.nilai_asli || '-' }}</td>
                    <td class="p-3 text-center bg-amber-50">
                      <select v-model="item.nilai_revisi" class="border rounded-lg p-2 text-center font-bold w-24 border-amber-300 focus:ring-2 focus:ring-amber-400 outline-none">
                        <option value="">-- Tidak Direvisi --</option>
                        <option value="A">A</option>
                        <option value="A-">A-</option>
                        <option value="B+">B+</option>
                        <option value="B">B</option>
                        <option value="B-">B-</option>
                        <option value="C+">C+</option>
                        <option value="C">C</option>
                        <option value="D">D</option>
                        <option value="E">E</option>
                      </select>
                    </td>
                  </tr>
                  <tr v-if="editNilaiData.length === 0">
                    <td colspan="5" class="p-10 text-center text-gray-400">Belum ada data nilai</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Tab Tambah -->
          <div v-if="tabEditMode === 'tambah'">
            <div class="bg-green-50 p-4 rounded-xl mb-4 border border-green-200">
              <h4 class="font-bold text-green-700 mb-3">➕ Tambah Mata Kuliah Baru ke Transkrip</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                  <label class="text-xs font-bold text-gray-600">Kode MK</label>
                  <input type="text" v-model="formMKBaru.kode" class="w-full border border-gray-200 rounded-xl p-2 text-sm focus:ring-2 focus:ring-green-400 outline-none">
                </div>
                <div>
                  <label class="text-xs font-bold text-gray-600">SKS</label>
                  <input type="number" v-model="formMKBaru.sks" class="w-full border border-gray-200 rounded-xl p-2 text-sm focus:ring-2 focus:ring-green-400 outline-none">
                </div>
                <div class="md:col-span-2">
                  <label class="text-xs font-bold text-gray-600">Nama Mata Kuliah</label>
                  <input type="text" v-model="formMKBaru.nama_mk" class="w-full border border-gray-200 rounded-xl p-2 text-sm focus:ring-2 focus:ring-green-400 outline-none">
                </div>
                <div>
                  <label class="text-xs font-bold text-gray-600">Kategori</label>
                  <select v-model="formMKBaru.kategori" class="w-full border border-gray-200 rounded-xl p-2 text-sm bg-white">
                    <option value="Wajib">Wajib</option>
                    <option value="Pilihan">Pilihan</option>
                    <option value="TA">TA</option>
                  </select>
                </div>
                <div>
                  <label class="text-xs font-bold text-gray-600">Nilai</label>
                  <select v-model="formMKBaru.nilai" class="w-full border border-gray-200 rounded-xl p-2 text-sm bg-white">
                    <option value="">-- Pilih --</option>
                    <option value="A">A</option>
                    <option value="A-">A-</option>
                    <option value="B+">B+</option>
                    <option value="B">B</option>
                    <option value="B-">B-</option>
                    <option value="C+">C+</option>
                    <option value="C">C</option>
                    <option value="D">D</option>
                    <option value="E">E</option>
                  </select>
                </div>
              </div>
              <button @click="tambahMataKuliahKeNilai" class="mt-3 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-xl text-sm font-bold transition shadow-md">
                + Tambahkan
              </button>
            </div>
            <div v-if="mkBaruDitambahkan.length > 0" class="mt-4 border rounded-xl overflow-hidden">
              <h4 class="font-bold p-3 bg-gray-100 border-b">📌 Mata Kuliah Baru:</h4>
              <table class="w-full text-sm">
                <thead class="bg-gray-50">
                  <tr><th class="p-2">Kode</th><th>Nama</th><th>SKS</th><th>Nilai</th><th>Aksi</th></tr>
                </thead>
                <tbody>
                  <tr v-for="(mk, idx) in mkBaruDitambahkan" :key="idx" class="border-b">
                    <td class="p-2">{{ mk.kode_mk }}</td>
                    <td class="p-2">{{ mk.nama_mk }}</td>
                    <td class="p-2 text-center">{{ mk.sks }}</td>
                    <td class="p-2 text-center">{{ mk.nilai }}</td>
                    <td class="p-2 text-center"><button @click="hapusMKBaru(idx)" class="text-red-600 hover:bg-red-100 p-1 rounded">🗑️</button></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div class="p-4 border-t bg-gray-50 flex justify-end gap-3 rounded-b-2xl">
          <button @click="tutupEditNilaiModal" class="px-5 py-2 bg-gray-300 hover:bg-gray-400 rounded-xl text-sm font-bold transition">Batal</button>
          <button @click="simpanPerubahanNilai" class="px-5 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-xl text-sm font-bold transition shadow-md">Simpan Perubahan</button>
        </div>
      </div>
    </div>

    <!-- MODAL KOMENTAR PENDAFTARAN -->
    <div v-if="showKomentarPendaftaranModal" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl w-full max-w-md shadow-2xl">
        <div class="p-5 border-b" :class="selectedPendaftaran?.status === 'MENUNGGU' ? 'bg-orange-50' : 'bg-green-50'">
          <div class="flex justify-between items-center">
            <h3 class="font-bold" :class="selectedPendaftaran?.status === 'MENUNGGU' ? 'text-orange-800' : 'text-green-800'">
              {{ selectedPendaftaran?.status === 'MENUNGGU' ? '💬 Verifikasi Pendaftaran' : '📋 Detail Komentar' }}
            </h3>
            <button @click="closeKomentarPendaftaranModal" class="text-gray-400 hover:text-red-500 transition text-xl">&times;</button>
          </div>
        </div>
        <div class="p-5">
          <p class="text-sm mb-2">Mahasiswa: <strong>{{ selectedPendaftaran?.mahasiswa_nama || selectedPendaftaran?.nama_lengkap }}</strong></p>
          <p class="text-xs text-gray-500 mb-3">NIM: <strong>{{ selectedPendaftaran?.nim }}</strong></p>
          <div class="mb-4">
            <span :class="selectedPendaftaran?.status === 'MENUNGGU' ? 'bg-orange-100 text-orange-700' : 'bg-green-100 text-green-700'" 
                  class="px-2 py-0.5 rounded-full text-[10px] font-bold">
              {{ selectedPendaftaran?.status === 'MENUNGGU' ? '⏳ Menunggu Verifikasi' : '✅ Telah Diverifikasi' }}
            </span>
          </div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">
            {{ selectedPendaftaran?.status === 'MENUNGGU' ? 'Catatan Verifikasi' : 'Catatan BAAK' }}
          </label>
          <textarea 
            v-model="catatanKomentarPendaftaran" 
            placeholder="Tulis catatan verifikasi untuk mahasiswa..." 
            class="w-full border border-gray-200 rounded-xl p-3 h-28 outline-none focus:ring-2 focus:ring-indigo-400" 
            :disabled="isLoadingKomentar || selectedPendaftaran?.status !== 'MENUNGGU'"
          ></textarea>
          <div v-if="selectedPendaftaran?.status !== 'MENUNGGU' && selectedPendaftaran?.catatan_baak" class="mt-3 p-3 bg-gray-50 rounded-xl">
            <p class="text-xs font-bold text-gray-600 mb-1">📝 Catatan Sebelumnya:</p>
            <p class="text-sm text-gray-700">{{ selectedPendaftaran?.catatan_baak }}</p>
          </div>
        </div>
        <div class="p-4 border-t bg-gray-50 flex justify-end gap-2 rounded-b-2xl">
          <button @click="closeKomentarPendaftaranModal" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-xl text-sm font-medium transition">Tutup</button>
          <button 
            v-if="selectedPendaftaran?.status === 'MENUNGGU'"
            @click="kirimKomentarPendaftaran" 
            class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-xl text-sm font-bold transition flex items-center gap-2 shadow-md" 
            :disabled="isLoadingKomentar"
          >
            <span v-if="isLoadingKomentar" class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            <span>{{ isLoadingKomentar ? 'Memproses...' : '✅ Verifikasi & Kirim' }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL TEMPLATE SURAT PERPUSTAKAAN -->
    <div v-if="showTemplateModalPerpus" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl">
        <div class="p-5 bg-indigo-950 text-white flex justify-between rounded-t-2xl">
          <div>
            <h3 class="font-bold text-lg">📝 Edit Template Surat Bebas Perpustakaan</h3>
            <p class="text-xs text-indigo-200">Gunakan placeholder: [NAMA], [NIM], [JURUSAN], [TANGGAL], [PETUGAS]</p>
          </div>
          <button @click="showTemplateModalPerpus = false" class="text-white hover:text-red-400 transition text-xl">&times;</button>
        </div>
        <div class="flex-1 overflow-y-auto p-6 bg-gray-100">
          <div class="bg-white p-6 shadow-sm border border-gray-200 rounded">
            <textarea v-model="templateSuratPerpus" class="w-full h-[400px] p-4 border border-gray-300 bg-gray-50 focus:bg-white focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none resize-none font-mono text-sm leading-relaxed rounded"></textarea>
            <div class="mt-4 p-3 bg-blue-50 rounded-lg">
              <p class="text-xs font-bold text-blue-700 mb-2">📌 Placeholder yang tersedia:</p>
              <div class="flex flex-wrap gap-2 text-xs">
                <code class="bg-blue-100 px-2 py-1 rounded">[NAMA]</code>
                <code class="bg-blue-100 px-2 py-1 rounded">[NIM]</code>
                <code class="bg-blue-100 px-2 py-1 rounded">[JURUSAN]</code>
                <code class="bg-blue-100 px-2 py-1 rounded">[TANGGAL]</code>
                <code class="bg-blue-100 px-2 py-1 rounded">[PETUGAS]</code>
              </div>
            </div>
          </div>
        </div>
        <div class="p-4 bg-white border-t border-gray-200 flex justify-end gap-3 rounded-b-2xl">
          <button @click="showTemplateModalPerpus = false" class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 text-sm font-bold">Batal</button>
          <button @click="simpanTemplateSuratPerpus" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg shadow text-sm font-bold">💾 Simpan Template</button>
        </div>
      </div>
    </div>

    <!-- MODAL TANDA TANGAN PERPUSTAKAAN -->
    <div v-if="showTtdModalPerpus" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl w-full max-w-md flex flex-col shadow-2xl">
        <div class="p-5 bg-indigo-950 text-white flex justify-between rounded-t-2xl">
          <div>
            <h3 class="font-bold text-lg">✍️ Atur Tanda Tangan Digital</h3>
            <p class="text-xs text-indigo-200">Upload foto tanda tangan (PNG/JPG)</p>
          </div>
          <button @click="showTtdModalPerpus = false" class="text-white hover:text-red-400 transition text-xl">&times;</button>
        </div>
        <div class="p-6 bg-gray-50 flex flex-col items-center gap-4">
          <div class="w-full border-2 border-dashed border-gray-300 rounded-xl p-4 bg-white flex flex-col items-center justify-center min-h-[160px]">
            <div v-if="ttdPerpusPreview" class="flex flex-col items-center gap-2">
              <img :src="ttdPerpusPreview" class="max-h-28 object-contain rounded" alt="Preview Tanda Tangan" />
              <p class="text-[11px] text-gray-400 italic">Pratinjau tanda tangan</p>
            </div>
            <div v-else class="text-center py-4">
              <span class="text-3xl">🖋️</span>
              <p class="text-sm text-gray-500 mt-2 font-semibold">Belum Ada Tanda Tangan</p>
              <p class="text-xs text-gray-400">Silakan pilih file gambar</p>
            </div>
          </div>
          <div class="w-full">
            <label class="block text-xs font-bold text-gray-600 mb-2">Pilih File Tanda Tangan:</label>
            <input type="file" @change="uploadTtdPerpus" accept="image/png, image/jpeg" class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-bold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 border border-gray-200 rounded-lg p-1 bg-white cursor-pointer" />
          </div>
        </div>
        <div class="p-4 bg-white border-t border-gray-200 flex justify-between items-center rounded-b-2xl">
          <button v-if="ttdPerpusPreview" @click="hapusTtdPerpus" class="px-4 py-2 bg-red-50 hover:bg-red-100 text-red-600 rounded-lg text-sm font-bold transition">🗑️ Hapus TTD</button>
          <div v-else></div>
          <button @click="showTtdModalPerpus = false" class="px-4 py-2 bg-gray-800 hover:bg-gray-900 text-white rounded-lg text-sm font-bold transition">Selesai & Tutup</button>
        </div>
      </div>
    </div>

    <!-- MODAL TOLAK PERPUSTAKAAN -->
    <div v-if="showTolakPerpusModal" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl w-full max-w-md shadow-2xl">
        <div class="p-5 border-b bg-red-50 flex justify-between items-center">
          <h3 class="font-bold text-red-800">❌ Tolak Pengajuan Perpustakaan</h3>
          <button @click="showTolakPerpusModal=false" class="text-gray-400 hover:text-red-500 transition text-xl">&times;</button>
        </div>
        <div class="p-5">
          <p class="text-sm text-gray-600 mb-3">Mahasiswa: <strong>{{ tolakPerpusName }}</strong></p>
          <textarea v-model="catatanTolakPerpus" placeholder="Alasan penolakan (wajib)..." class="w-full border border-gray-200 rounded-xl p-3 h-28 focus:ring-2 focus:ring-red-400 outline-none"></textarea>
        </div>
        <div class="p-4 border-t bg-gray-50 flex justify-end gap-2 rounded-b-2xl">
          <button @click="showTolakPerpusModal=false" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-xl text-sm font-medium transition">Batal</button>
          <button @click="confirmTolakPerpus" class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-xl text-sm font-bold transition shadow-md">Tolak</button>
        </div>
      </div>
    </div>

    <!-- MODAL SURAT PERPUSTAKAAN -->
    <div v-if="showSuratPerpusModal" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl w-full max-w-6xl max-h-[90vh] flex flex-col shadow-2xl">
        <div class="p-5 bg-indigo-950 text-white flex justify-between rounded-t-2xl">
          <div>
            <h3 class="font-bold text-lg">📄 Surat Bebas Perpustakaan</h3>
            <p class="text-xs text-indigo-200">Edit isi, atur posisi TTD, dan kirim ke mahasiswa</p>
          </div>
          <button @click="showSuratPerpusModal = false" class="text-white hover:text-red-400 transition text-xl">&times;</button>
        </div>
        <div class="flex flex-1 overflow-hidden min-h-[500px]">
          <div class="w-1/2 p-4 bg-gray-100 border-r border-gray-200 flex flex-col overflow-y-auto">
            <label class="text-xs font-bold text-gray-600 mb-2">✏️ Edit Isi Surat:</label>
            <textarea v-model="isiSuratPerpus" class="flex-1 min-h-[200px] p-4 border border-gray-300 bg-white focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none resize-none font-mono text-sm leading-relaxed rounded"></textarea>
            <div class="mt-3 flex justify-between items-center">
              <button @click="resetKeTemplatePerpus" class="text-xs text-indigo-600 hover:text-indigo-800">↺ Reset ke Template</button>
              <span class="text-xs text-gray-400">Karakter: {{ isiSuratPerpus.length }}</span>
            </div>
            <div class="mt-4 p-4 bg-white rounded-lg border border-gray-200">
              <p class="text-xs font-bold text-gray-700 mb-3">✍️ Atur Posisi Tanda Tangan:</p>
              <div class="flex gap-4 items-start">
                <div class="flex-shrink-0">
                  <div v-if="ttdPerpusImage" class="border-2 border-dashed border-indigo-300 p-2 rounded-lg bg-gray-50">
                    <img :src="ttdPerpusImage" class="w-32 h-20 object-contain" />
                  </div>
                  <div v-else class="w-32 h-20 bg-gray-200 rounded-lg flex items-center justify-center text-xs text-gray-400">Belum ada TTD</div>
                  <button @click="openTtdModalPerpus" class="mt-2 text-[10px] text-indigo-600 hover:text-indigo-800 underline">Ganti Tanda Tangan</button>
                </div>
                <div class="flex-1">
                  <div class="mb-4">
                    <div class="flex justify-between items-center mb-1">
                      <p class="text-[10px] font-bold text-gray-600">Horizontal (Kiri-Kanan):</p>
                      <p class="text-[10px] font-bold text-indigo-600">{{ ttdPerpusPositionX }}%</p>
                    </div>
                    <input type="range" v-model="ttdPerpusPositionX" min="0" max="100" step="1" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600" />
                  </div>
                  <div class="mb-4">
                    <div class="flex justify-between items-center mb-1">
                      <p class="text-[10px] font-bold text-gray-600">Vertikal (Atas-Bawah):</p>
                      <p class="text-[10px] font-bold text-indigo-600">{{ ttdPerpusPositionY }}%</p>
                    </div>
                    <input type="range" v-model="ttdPerpusPositionY" min="0" max="100" step="1" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600" />
                    <p class="text-[9px] text-gray-400 mt-1">0% = atas, 100% = bawah</p>
                  </div>
                  <div class="mt-3 p-3 bg-indigo-50 rounded-lg text-center">
                    <p class="text-[10px] font-semibold text-indigo-700 mb-2">🎯 Preview Posisi TTD:</p>
                    <div class="relative border-2 border-dashed border-indigo-300 rounded-lg h-24 bg-white overflow-hidden">
                      <div class="absolute inset-0 flex items-center justify-center"><span class="text-[9px] text-gray-400">Area Surat</span></div>
                      <div class="absolute w-14 h-10 bg-indigo-500/70 border-2 border-indigo-700 rounded flex items-center justify-center text-[8px] font-bold text-white transition-all duration-150" 
                           :style="{ left: `${ttdPerpusPositionX}%`, top: `${ttdPerpusPositionY}%`, transform: 'translate(-50%, -50%)' }">TTD</div>
                    </div>
                  </div>
                  <div class="mt-3">
                    <label class="text-[10px] font-bold text-gray-600">Nama Pustakawan:</label>
                    <input v-model="petugasNamePerpus" type="text" class="w-full mt-1 px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 outline-none" placeholder="Masukkan nama pustakawan" />
                  </div>
                  <div class="mt-3">
                    <label class="text-[10px] font-bold text-gray-600">📝 Catatan Tambahan (opsional):</label>
                    <textarea v-model="catatanTambahanPerpus" class="w-full mt-1 px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 outline-none resize-none" rows="2" placeholder="Tambahkan catatan khusus untuk mahasiswa..."></textarea>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="w-1/2 p-4 bg-gray-100 flex flex-col">
            <label class="text-xs font-bold text-gray-600 mb-2">👁️ Preview Surat:</label>
            <div id="suratPreviewPerpus" class="flex-1 bg-white p-8 border border-gray-200 rounded overflow-y-auto shadow-inner" style="font-family: 'Times New Roman', serif; color: black;">
              <div class="max-w-2xl mx-auto">
                <div class="flex items-center justify-center border-b-[3px] border-black pb-4 mb-6">
                  <img v-if="logoUrl" :src="logoUrl" alt="Logo STIE SBI" class="w-20 h-20 object-contain mr-10" crossorigin="anonymous" />
                  <div class="text-center flex-1 pr-12">
                    <h2 class="text-lg font-bold uppercase m-0 leading-tight">PERPUSTAKAAN</h2>
                    <h1 class="text-2xl font-black uppercase m-0 leading-tight">STIE SOLUSI BISNIS INDONESIA YOGYAKARTA</h1>
                    <p class="text-sm m-0 mt-2">Jl. Ring Road Utara No. 17, Condongcatur, Depok, Sleman, Yogyakarta 55283</p>
                    <p class="text-xs m-0">Telp. (0274) 887984 | Email: perpustakaan@stie-sbi.ac.id</p>
                  </div>
                </div>
                <div class="whitespace-pre-wrap text-sm leading-relaxed space-y-3" style="font-family: 'Times New Roman', serif;">
                  <div class="text-center mb-4"><span class="font-bold underline text-base">SURAT BEBAS PINJAMAN PUSTAKA</span></div>
                  <p>Surat ini diberikan untuk permohonan mahasiswa yang sudah menyelesaikan semua biaya administrasi/denda :</p>
                  <p>Identitas pemohon surat bebas pinjam pustaka ini :</p>
                  <div class="ml-8 space-y-1">
                    <p>Nama &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : {{ selectedPerpusMhs?.full_name || '[NAMA]' }}</p>
                    <p>No. Mahasiswa &nbsp;&nbsp;&nbsp; : {{ selectedPerpusMhs?.nim || '[NIM]' }}</p>
                    <p>Jurusan &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : {{ selectedPerpusMhs?.jurusan || 'Akuntansi' }}</p>
                  </div>
                  <p>Semoga surat ini dapat memenuhi keperluan diatas.</p>
                  <div class="mt-10">
                    <p class="text-right">Yogyakarta, {{ tanggalSuratPerpus }}</p>
                    <p class="text-right mt-4">Pustakawan,</p>
                  </div>
                </div>
                <div style="position: relative; min-height: 150px; margin-top: 10px;">
                  <div v-if="ttdPerpusImage" class="absolute" :style="{ left: ttdPerpusPositionX + '%', top: ttdPerpusPositionY + '%', transform: 'translate(-50%, -50%)', textAlign: 'center', whiteSpace: 'nowrap', zIndex: 10 }">
                    <img :src="ttdPerpusImage" class="h-14 object-contain" crossorigin="anonymous" />
                    <p class="text-xs font-bold mt-1">{{ petugasNamePerpus || user.full_name }}</p>
                    <p class="text-[10px] text-gray-500">Pustakawan</p>
                  </div>
                  <div v-else class="text-red-500 text-xs italic text-center py-4">(Tanda tangan belum diatur)</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="p-4 bg-white border-t border-gray-200 flex justify-end gap-3 rounded-b-2xl">
          <button @click="showSuratPerpusModal = false" class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 text-sm font-bold">Batal</button>
          <button @click="generateAndSendPDFPerpus" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg shadow text-sm font-bold">📎 Generate PDF & Kirim</button>
        </div>
      </div>
    </div>

    <!-- MODAL LIHAT BERKAS PERPUSTAKAAN -->
    <div v-if="showBerkasPerpusModal" class="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4" @click.self="showBerkasPerpusModal = false">
      <div class="bg-white rounded-2xl w-full max-w-4xl max-h-[85vh] flex flex-col shadow-2xl">
        <div class="p-5 bg-indigo-950 text-white flex justify-between rounded-t-2xl">
          <div>
            <h3 class="font-bold text-lg flex items-center gap-2">📂 Semua Berkas - {{ selectedBerkasPerpus?.full_name }}</h3>
            <p class="text-xs text-indigo-200">NIM: {{ selectedBerkasPerpus?.nim }}</p>
          </div>
          <button @click="showBerkasPerpusModal = false" class="text-white hover:text-red-400 transition text-xl">&times;</button>
        </div>
        <div class="flex-1 overflow-y-auto p-6 bg-gray-100">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-xs text-gray-400">Status Validasi</p>
                <p class="text-lg font-bold" :class="{ 'text-green-600': selectedBerkasPerpus?.status === 'DISETUJUI', 'text-red-600': selectedBerkasPerpus?.status === 'DITOLAK', 'text-orange-600': selectedBerkasPerpus?.status === 'MENUNGGU' }">
                  {{ selectedBerkasPerpus?.status === 'DISETUJUI' ? '✅ DISETUJUI' : selectedBerkasPerpus?.status === 'DITOLAK' ? '❌ DITOLAK' : '⏳ MENUNGGU' }}
                </p>
              </div>
              <div class="text-right">
                <p class="text-xs text-gray-400">Tanggal Upload</p>
                <p class="text-sm font-medium">{{ formatDate(selectedBerkasPerpus?.created_at) }}</p>
              </div>
            </div>
            <div v-if="selectedBerkasPerpus?.catatan_perpus" class="mt-3 p-2 bg-gray-50 rounded-lg text-xs text-gray-600">
              <span class="font-bold">Catatan:</span> {{ selectedBerkasPerpus.catatan_perpus }}
            </div>
          </div>
          <h4 class="font-bold text-gray-700 mb-4 flex items-center gap-2">📁 Semua Berkas ({{ getAllFilesCount(selectedBerkasPerpus) }})</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="(fileInfo, fileKey) in getAllFilesList(selectedBerkasPerpus)" :key="fileKey" class="bg-white rounded-xl border border-gray-200 p-4 hover:shadow-md transition hover:border-indigo-300">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center"><span class="text-indigo-600 text-xl">📄</span></div>
                  <div><p class="text-sm font-semibold text-gray-800 capitalize">{{ fileInfo.label }}</p><p class="text-[10px] text-gray-400">PDF</p></div>
                </div>
                <a :href="getFullImageUrl(fileInfo.url)" target="_blank" class="bg-indigo-600 text-white px-3 py-1.5 rounded-lg text-xs font-bold hover:bg-indigo-700 transition">📄 Buka PDF</a>
              </div>
            </div>
          </div>
          <div v-if="selectedBerkasPerpus?.link_surat_pdf" class="mt-6">
            <div class="bg-green-50 rounded-xl border border-green-200 p-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center"><span class="text-green-600 text-xl">📜</span></div>
                  <div><p class="text-sm font-semibold text-green-800">Surat Bebas Perpustakaan</p><p class="text-[10px] text-green-600">Dokumen Resmi</p></div>
                </div>
                <a :href="getFullImageUrl(selectedBerkasPerpus.link_surat_pdf)" target="_blank" class="bg-green-600 text-white px-4 py-2 rounded-lg text-xs font-bold hover:bg-green-700 transition">📄 Buka Surat</a>
              </div>
            </div>
          </div>
          <div v-if="getAllFilesCount(selectedBerkasPerpus) === 0 && !selectedBerkasPerpus?.link_surat_pdf" class="text-center py-16 text-gray-400">
            <span class="text-5xl block mb-3">📭</span><p class="text-sm">Belum ada berkas</p>
          </div>
        </div>
        <div class="p-4 bg-white border-t border-gray-200 flex justify-end gap-3 rounded-b-2xl">
          <button @click="showBerkasPerpusModal = false" class="px-5 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg text-sm font-bold transition">Tutup</button>
          <button v-if="selectedBerkasPerpus?.status === 'MENUNGGU'" @click="setujuiPerpus(selectedBerkasPerpus)" class="px-5 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-bold transition">✔ Setujui</button>
        </div>
      </div>
    </div>

    <!-- MODAL FORM PERIODE -->
    <div v-if="showModalPeriode" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex justify-center items-center z-[80] p-4" @click.self="showModalPeriode = false">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden transform transition-all">
        <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50">
          <h2 class="font-bold text-gray-800 text-lg">{{ isEditPeriode ? '✏️ Edit Periode' : '➕ Tambah Periode' }}</h2>
          <button @click="showModalPeriode = false" class="text-gray-400 hover:text-red-500 transition font-bold text-xl">&times;</button>
        </div>
        <form @submit.prevent="simpanPeriode" class="p-6 space-y-4">
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Nama Periode</label>
            <input type="text" v-model="formPeriode.nama_periode" required 
                   class="w-full border border-gray-200 rounded-lg p-2.5 text-sm outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Tanggal Mulai</label>
            <input type="date" v-model="formPeriode.tanggal_mulai" required 
                   class="w-full border border-gray-200 rounded-lg p-2.5 text-sm outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-1">Tanggal Selesai</label>
            <input type="date" v-model="formPeriode.tanggal_selesai" required 
                   class="w-full border border-gray-200 rounded-lg p-2.5 text-sm outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div class="flex justify-end gap-3 pt-2">
            <button type="button" @click="showModalPeriode = false" class="px-4 py-2 text-sm font-bold text-gray-500 hover:text-gray-700">Batal</button>
            <button type="submit" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-bold shadow-md transition">
              {{ isEditPeriode ? 'Update' : 'Simpan' }}
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const router = useRouter();
const view = ref('stats');
const loading = ref(false);
const user = ref({ full_name: '', role: '' });

// --- DATA STATES (AKADEMIK sebagai sumber utama) ---
const users = ref([]);
const daftarAkademik = ref([]);
const stats = ref({ total: 0, menunggu: 0, selesai: 0, ditolak: 0 });
const roles = ['MAHASISWA', 'DPA', 'AKADEMIK', 'KEUANGAN', 'PERPUS', 'SUPERADMIN'];

// --- MATA KULIAH STATES ---
const daftarMataKuliahData = ref([]);
const searchMatakuliah = ref('');
const filterJurusan = ref('');
const filterKategori = ref('');
const filterKelompok = ref('');
const currentPageMatakuliah = ref(1);
const rowsPerPageMatakuliah = ref(10);
const isModalFormMkOpen = ref(false);
const isEditMode = ref(false);
const formMk = ref({ kode: '', nama: '', sks: 2, jurusan: 'Semua Jurusan', kategori: 'Wajib', kelompok: '' });

// --- USER MANAGEMENT ---
const newUser = ref({ full_name: '', username: '', role: 'MAHASISWA', password: '' });
const showEditModal = ref(false);
const editUser = ref({ id: null, full_name: '', username: '', role: '' });
const originalUserData = ref({});
const searchUserQuery = ref('');

// --- VERIFIKASI AKADEMIK ---
const searchAkademik = ref('');
const filterStatusAkademik = ref('');
const currentPageAkademik = ref(1);
const rowsPerPageAkademik = ref(10);
const showVerifikasiAkademikModal = ref(false);
const showBerkasAkademikModal = ref(false);
const selectedAkademik = ref(null);
const selectedBerkasAkademik = ref(null);
const formCatatanAkademik = ref('');

const akademikFileLabels = {
  foto_ijazah: '🎓 Ijazah Akhir',
  foto_akte: '📄 Akte Kelahiran',
  foto_ktp: '🪪 KTP',
  foto_3x4: '📸 Pas Foto 3x4'
};

// --- VERIFIKASI TRANSKRIP (perbaikan) ---
const daftarTranskrip = ref([]);
const searchTranskrip = ref('');
const filterStatusTranskrip = ref('');
const currentPageTranskrip = ref(1);
const rowsPerPageTranskrip = ref(10);
const showTolakTranskripModal = ref(false);
const tolakTranskripId = ref(null);
const catatanTolakTranskrip = ref('');
const showDetailNilaiModal = ref(false);
const selectedNilaiItem = ref(null);

// --- EDIT NILAI (BARU) ---
const showEditNilaiModal = ref(false);
const editNilaiId = ref(null);
const editNilaiMhsName = ref('');
const editNilaiData = ref([]);
const mkBaruDitambahkan = ref([]);
const tabEditMode = ref('revisi');
const formMKBaru = ref({ kode: '', nama_mk: '', sks: 2, kategori: 'Wajib', nilai: '' });

// --- VERIFIKASI PENDAFTARAN ---
const daftarPendaftaran = ref([]);
const searchPendaftaran = ref('');
const currentPagePendaftaran = ref(1);
const rowsPerPagePendaftaran = ref(10);
const showKomentarPendaftaranModal = ref(false);
const selectedPendaftaran = ref(null);
const catatanKomentarPendaftaran = ref('');
const isLoadingKomentar = ref(false);

// --- PERPUSTAKAAN ---
const daftarPerpus = ref([]);
const searchPerpus = ref('');
const filterStatusPerpus = ref('');
const currentPagePerpus = ref(1);
const rowsPerPagePerpus = ref(10);
const showTemplateModalPerpus = ref(false);
const templateSuratPerpus = ref(`SURAT BEBAS PINJAMAN PUSTAKA

Surat ini diberikan untuk permohonan mahasiswa yang sudah menyelesaikan semua biaya administrasi/denda :

Identitas pemohon surat bebas pinjam pustaka ini :

Nama : [NAMA]
No. Mahasiswa : [NIM]
Jurusan : [JURUSAN]

Semoga surat ini dapat memenuhi keperluan diatas.

[TANGGAL]
Pustakawan,

[PETUGAS]`);
const showTtdModalPerpus = ref(false);
const ttdPerpusImage = ref(null);
const ttdPerpusPreview = ref(null);
const ttdPerpusUrl = ref(null);
const ttdPerpusPositionX = ref(85);
const ttdPerpusPositionY = ref(85);
const showSuratPerpusModal = ref(false);
const isiSuratPerpus = ref('');
const selectedPerpusMhs = ref(null);
const petugasNamePerpus = ref('');
const catatanTambahanPerpus = ref('');
const tanggalSuratPerpus = ref('');
const showTolakPerpusModal = ref(false);
const tolakPerpusId = ref(null);
const tolakPerpusName = ref('');
const catatanTolakPerpus = ref('');
const showBerkasPerpusModal = ref(false);
const selectedBerkasPerpus = ref(null);
const logoUrl = ref('');

// --- PERIODE ---
const listPeriode = ref([]);
const showModalPeriode = ref(false);
const isEditPeriode = ref(false);
const formPeriode = ref({ nama_periode: '', tanggal_mulai: '', tanggal_selesai: '' });
const editPeriodeId = ref(null);

// ========== HELPER FUNCTIONS ==========
const formatDate = (dateString) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' });
};

const getUserId = (obj) => obj.id || obj.pk || obj.uuid;

const getStatus = (item) => {
  if (!item) return 'MENUNGGU';
  let status = item.status || item.status_transkrip || 'MENUNGGU';
  if (status === 'DISETUJU') return 'DISETUJUI';
  if (status === 'SETUJU') return 'DISETUJUI';
  if (status === 'TOLAK') return 'DITOLAK';
  return status;
};

const getStatusText = (status) => {
  const map = {
    'DISETUJUI': '✅ Disetujui',
    'DITOLAK': '❌ Ditolak',
    'MENUNGGU': '⏳ Menunggu',
    'BELUM': '⚪ Belum',
    'PROSES': '🔄 Proses',
    'SELESAI': '✅ Selesai'
  };
  return map[status] || status || '⚪ Belum';
};

const getBadgeClass = (status) => {
  const s = getStatus({ status });
  if (s === 'DISETUJUI' || s === 'SELESAI') return 'bg-green-100 text-green-700 px-2 py-0.5 rounded-full text-[10px] font-bold';
  if (s === 'DITOLAK') return 'bg-red-100 text-red-700 px-2 py-0.5 rounded-full text-[10px] font-bold';
  if (s === 'MENUNGGU') return 'bg-orange-100 text-orange-700 px-2 py-0.5 rounded-full text-[10px] font-bold';
  return 'bg-gray-100 text-gray-500 px-2 py-0.5 rounded-full text-[10px] font-bold';
};

const getFileUrl = (item) => {
  if (!item) return null;
  let fileUrl = item.file_transkrip || item.berkas || item.file || item.file_url;
  if (!fileUrl) return null;
  if (fileUrl.startsWith('http')) return fileUrl;
  if (fileUrl.startsWith('/media/') || fileUrl.startsWith('media/')) {
    const clean = fileUrl.startsWith('/') ? fileUrl : `/${fileUrl}`;
    return `http://127.0.0.1:8000${clean}`;
  }
  return `http://127.0.0.1:8000/media/${fileUrl}`;
};

const getFullImageUrl = (path) => {
  if (!path) return '';
  if (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('data:image')) {
    return path;
  }
  const backendBaseUrl = api.defaults.baseURL ? api.defaults.baseURL.replace(/\/api\/?$/, '') : 'http://localhost:8000';
  return `${backendBaseUrl}${path.startsWith('/') ? path : '/' + path}`;
};

// ========== FUNGSI AKADEMIK ==========
const fetchAkademik = async () => {
  loading.value = true;
  try {
    const res = await api.get('akademik/list-mahasiswa/');
    daftarAkademik.value = res.data.map(m => ({
      ...m,
      status_akademik: m.status_akademik || m.status_akhir || 'MENUNGGU'
    }));
    stats.value.total = daftarAkademik.value.length;
    stats.value.menunggu = daftarAkademik.value.filter(m => (m.status_akademik || m.status_akhir) === 'MENUNGGU').length;
    stats.value.selesai = daftarAkademik.value.filter(m => (m.status_akademik || m.status_akhir) === 'DISETUJUI').length;
    stats.value.ditolak = daftarAkademik.value.filter(m => (m.status_akademik || m.status_akhir) === 'DITOLAK').length;
    console.log('✅ Data akademik dimuat:', daftarAkademik.value.length, 'mahasiswa');
  } catch (err) {
    console.error('❌ Gagal fetch akademik:', err);
    if (err.response?.status === 401) router.push('/login');
  } finally {
    loading.value = false;
  }
};

const akademikMenungguCount = computed(() => daftarAkademik.value.filter(m => (m.status_akademik || m.status_akhir) === 'MENUNGGU').length);
const akademikDisetujuiCount = computed(() => daftarAkademik.value.filter(m => (m.status_akademik || m.status_akhir) === 'DISETUJUI').length);
const akademikDitolakCount = computed(() => daftarAkademik.value.filter(m => (m.status_akademik || m.status_akhir) === 'DITOLAK').length);

const filteredAkademik = computed(() => {
  return daftarAkademik.value.filter(item => {
    const status = item.status_akademik || item.status_akhir || 'MENUNGGU';
    const matchStatus = !filterStatusAkademik.value || status === filterStatusAkademik.value;
    const matchSearch = !searchAkademik.value || 
      (item.full_name || '').toLowerCase().includes(searchAkademik.value.toLowerCase()) ||
      (item.nim || '').toLowerCase().includes(searchAkademik.value.toLowerCase());
    return matchStatus && matchSearch;
  });
});

const totalPagesAkademik = computed(() => Math.ceil(filteredAkademik.value.length / rowsPerPageAkademik.value));
const paginatedAkademik = computed(() => {
  const start = (currentPageAkademik.value - 1) * rowsPerPageAkademik.value;
  return filteredAkademik.value.slice(start, start + rowsPerPageAkademik.value);
});

const prevPageAkademik = () => { if (currentPageAkademik.value > 1) currentPageAkademik.value--; };
const nextPageAkademik = () => { if (currentPageAkademik.value < totalPagesAkademik.value) currentPageAkademik.value++; };
const resetFilterAkademik = () => { searchAkademik.value = ''; filterStatusAkademik.value = ''; currentPageAkademik.value = 1; };

const getAkademikFileCount = (item) => {
  if (!item) return 0;
  let count = 0;
  if (item.foto_ijazah) count++;
  if (item.foto_akte) count++;
  if (item.foto_ktp) count++;
  if (item.foto_3x4) count++;
  return count;
};

const openBerkasAkademik = (item) => {
  selectedBerkasAkademik.value = item;
  showBerkasAkademikModal.value = true;
};

const bukaModalVerifikasiAkademik = (item) => {
  selectedAkademik.value = item;
  formCatatanAkademik.value = item.catatan_akademik || '';
  showVerifikasiAkademikModal.value = true;
};

const submitVerifikasiAkademik = async (statusKeputusan) => {
  if (!selectedAkademik.value) return;
  if (statusKeputusan === 'DITOLAK' && !formCatatanAkademik.value.trim()) {
    alert('Harap berikan catatan alasan penolakan!');
    return;
  }
  const mahasiswaId = selectedAkademik.value.mahasiswa_id || selectedAkademik.value.id;
  const payload = {
    mahasiswa_id: mahasiswaId,
    status: statusKeputusan,
    catatan: formCatatanAkademik.value
  };
  try {
    await api.post('akademik/verifikasi-berkas/', payload);
    alert(`Sukses! Berkas akademik telah ${statusKeputusan === 'DISETUJUI' ? 'disetujui' : 'ditolak'}.`);
    showVerifikasiAkademikModal.value = false;
    await fetchAkademik();
  } catch (err) {
    const msg = err.response?.data?.error || 'Gagal menghubungi server';
    alert('Gagal Verifikasi: ' + msg);
  }
};

// ========== FUNGSI USERS ==========
const fetchUsers = async () => {
  try { const res = await api.get('users/'); users.value = Array.isArray(res.data) ? res.data : (res.data.results || []); } catch (err) { console.error("Users Error:", err); }
};

const filteredUsers = computed(() => {
  if (!searchUserQuery.value) return users.value;
  const q = searchUserQuery.value.toLowerCase();
  return users.value.filter(u => u.full_name.toLowerCase().includes(q) || u.username.toLowerCase().includes(q));
});

const handleCreateAccount = async () => {
  loading.value = true;
  try {
    await api.post('users/register/', newUser.value);
    alert(`✅ Berhasil: ${newUser.value.username} telah aktif.`);
    newUser.value = { full_name: '', username: '', role: 'MAHASISWA', password: '' };
    await fetchUsers();
  } catch (err) {
    alert("❌ Error: " + JSON.stringify(err.response?.data || "Server Error"));
  } finally {
    loading.value = false;
  }
};

const openEditModal = (user) => {
  const id = getUserId(user);
  originalUserData.value = { ...user };
  editUser.value = { id, full_name: user.full_name, username: user.username, role: user.role };
  showEditModal.value = true;
};

const submitEdit = async () => {
  loading.value = true;
  const id = editUser.value.id;
  const updatedData = {};
  if (editUser.value.full_name !== originalUserData.value.full_name) updatedData.full_name = editUser.value.full_name;
  if (editUser.value.username !== originalUserData.value.username) updatedData.username = editUser.value.username;
  if (editUser.value.role !== originalUserData.value.role) updatedData.role = editUser.value.role;
  if (Object.keys(updatedData).length === 0) { showEditModal.value = false; loading.value = false; return; }
  try {
    await api.patch(`users/${id}/`, updatedData);
    showEditModal.value = false;
    await fetchUsers();
  } catch (err) {
    alert("❌ Gagal Update.");
  } finally {
    loading.value = false;
  }
};

const handleDelete = async (user) => {
  if (confirm(`Permanen hapus akun ${user.full_name}?`)) {
    try {
      await api.delete(`users/${getUserId(user)}/`);
      await fetchUsers();
    } catch (err) {
      alert("Gagal menghapus.");
    }
  }
};

// ========== FUNGSI MATA KULIAH ==========
const fetchMataKuliah = async () => {
  try {
    const res = await api.get('matakuliah/');
    daftarMataKuliahData.value = res.data;
  } catch (err) {
    console.error("Mata Kuliah Error:", err);
    daftarMataKuliahData.value = [];
  }
};

const filteredMataKuliah = computed(() => {
  return daftarMataKuliahData.value.filter(mk => {
    const matchSearch = !searchMatakuliah.value || mk.kode.toLowerCase().includes(searchMatakuliah.value.toLowerCase()) || mk.nama.toLowerCase().includes(searchMatakuliah.value.toLowerCase());
    const matchJurusan = !filterJurusan.value || mk.jurusan === 'Semua Jurusan' || mk.jurusan === filterJurusan.value;
    const matchKategori = !filterKategori.value || mk.kategori === filterKategori.value;
    const matchKelompok = !filterKelompok.value || (mk.kelompok && mk.kelompok.toLowerCase().includes(filterKelompok.value.toLowerCase()));
    return matchSearch && matchJurusan && matchKategori && matchKelompok;
  });
});

const totalPagesMatakuliah = computed(() => Math.ceil(filteredMataKuliah.value.length / rowsPerPageMatakuliah.value));
const paginatedMatakuliah = computed(() => {
  const start = (currentPageMatakuliah.value - 1) * rowsPerPageMatakuliah.value;
  return filteredMataKuliah.value.slice(start, start + rowsPerPageMatakuliah.value);
});

const prevPageMatakuliah = () => { if (currentPageMatakuliah.value > 1) currentPageMatakuliah.value--; };
const nextPageMatakuliah = () => { if (currentPageMatakuliah.value < totalPagesMatakuliah.value) currentPageMatakuliah.value++; };

const bukaModalFormMk = (mk = null) => {
  if (mk) {
    isEditMode.value = true;
    formMk.value = { ...mk };
  } else {
    isEditMode.value = false;
    formMk.value = { kode: '', nama: '', sks: 2, jurusan: 'Semua Jurusan', kategori: 'Wajib', kelompok: '' };
  }
  isModalFormMkOpen.value = true;
};

const simpanMataKuliah = async () => {
  loading.value = true;
  try {
    if (isEditMode.value) {
      await api.put(`matakuliah/${formMk.value.kode}/`, formMk.value);
      alert('✅ Mata kuliah berhasil diperbarui');
    } else {
      await api.post('matakuliah/', formMk.value);
      alert('✅ Mata kuliah berhasil ditambahkan');
    }
    isModalFormMkOpen.value = false;
    await fetchMataKuliah();
  } catch (err) {
    console.error(err);
    alert('❌ Gagal menyimpan mata kuliah: ' + (err.response?.data?.message || err.message));
  } finally {
    loading.value = false;
  }
};

const hapusMataKuliah = async (kode) => {
  if (confirm(`Hapus mata kuliah dengan kode ${kode}?`)) {
    try {
      await api.delete(`matakuliah/${kode}/`);
      alert('✅ Mata kuliah berhasil dihapus');
      await fetchMataKuliah();
    } catch (err) {
      console.error(err);
      alert('❌ Gagal menghapus mata kuliah');
    }
  }
};

watch([searchMatakuliah, filterJurusan, filterKategori, filterKelompok], () => { currentPageMatakuliah.value = 1; });

// ========== FUNGSI TRANSKRIP (diperbaiki) ==========
const fetchTranskrip = async () => {
  loading.value = true;
  try {
    const res = await api.get('baak/berkas-masuk/');
    const data = Array.isArray(res.data) ? res.data : (res.data.results || []);
    daftarTranskrip.value = data.map(item => ({
      ...item,
      file_transkrip: item.file_transkrip || item.berkas || item.file_url || null,
      status: item.status || item.status_transkrip || 'MENUNGGU',
      full_name: item.full_name || item.mahasiswa_nama || item.nama || 'Tidak diketahui',
      nim: item.nim || item.mahasiswa_nim || '-',
      catatan_baak: item.catatan_baak || item.catatan || null,
      data_nilai: (item.data_nilai || []).map(n => ({
        ...n,
        nilai_revisi: n.nilai_revisi || '' // pastikan properti nilai_revisi ada
      }))
    }));
    console.log('✅ Data transkrip dimuat:', daftarTranskrip.value.length, 'data');
  } catch (err) {
    console.error('❌ Gagal fetch transkrip:', err);
    daftarTranskrip.value = [];
  } finally {
    loading.value = false;
  }
};

const filteredTranskrip = computed(() => {
  return daftarTranskrip.value.filter(item => {
    const status = getStatus(item);
    const matchStatus = !filterStatusTranskrip.value || status === filterStatusTranskrip.value;
    const matchSearch = !searchTranskrip.value ||
      (item.full_name || '').toLowerCase().includes(searchTranskrip.value.toLowerCase()) ||
      (item.nim || '').toLowerCase().includes(searchTranskrip.value.toLowerCase());
    return matchStatus && matchSearch;
  });
});

const transkripMenungguCount = computed(() => daftarTranskrip.value.filter(i => getStatus(i) === 'MENUNGGU').length);
const transkripDisetujuiCount = computed(() => daftarTranskrip.value.filter(i => getStatus(i) === 'DISETUJUI').length);
const transkripDitolakCount = computed(() => daftarTranskrip.value.filter(i => getStatus(i) === 'DITOLAK').length);

const totalPagesTranskrip = computed(() => Math.ceil(filteredTranskrip.value.length / rowsPerPageTranskrip.value));
const paginatedTranskrip = computed(() => {
  const start = (currentPageTranskrip.value - 1) * rowsPerPageTranskrip.value;
  return filteredTranskrip.value.slice(start, start + rowsPerPageTranskrip.value);
});

const prevPageTranskrip = () => { if (currentPageTranskrip.value > 1) currentPageTranskrip.value--; };
const nextPageTranskrip = () => { if (currentPageTranskrip.value < totalPagesTranskrip.value) currentPageTranskrip.value++; };
const resetFilterTranskrip = () => { searchTranskrip.value = ''; filterStatusTranskrip.value = ''; currentPageTranskrip.value = 1; };

const openTolakTranskripModal = (id, nama) => {
  tolakTranskripId.value = id;
  catatanTolakTranskrip.value = '';
  showTolakTranskripModal.value = true;
};

const confirmTolakTranskrip = async () => {
  if (!catatanTolakTranskrip.value.trim()) {
    alert('Alasan penolakan wajib diisi!');
    return;
  }
  await verifikasiTranskrip(tolakTranskripId.value, 'DITOLAK', catatanTolakTranskrip.value);
  showTolakTranskripModal.value = false;
};

const verifikasiTranskrip = async (id, status, catatan = null) => {
  try {
    await api.patch(`transkrip-nilai/${id}/verifikasi/`, {
      status: status,
      catatan_baak: status === 'DISETUJUI' ? 'Data transkrip valid dan sesuai' : catatan,
    });
    alert(`Berhasil ${status === 'DISETUJUI' ? 'menyetujui' : 'menolak'} transkrip`);
    await fetchTranskrip();
  } catch (err) {
    console.error(err);
    alert('Gagal melakukan verifikasi: ' + (err.response?.data?.error || err.message));
  }
};

const bukaDetailTranskrip = (item) => {
  alert(`Detail transkrip:\nNama: ${item.full_name}\nNIM: ${item.nim}\nStatus: ${getStatusText(getStatus(item))}\nCatatan: ${item.catatan_baak || item.catatan_dpa || '-'}`);
};

const bukaDetailNilai = (item) => {
  selectedNilaiItem.value = item;
  showDetailNilaiModal.value = true;
};

// ========== FUNGSI EDIT NILAI (BARU) ==========
const openEditNilaiModal = (id, nama, dataNilai) => {
  editNilaiId.value = id;
  editNilaiMhsName.value = nama;
  const dataArray = Array.isArray(dataNilai) ? dataNilai : [];
  editNilaiData.value = dataArray.map(item => ({
    kode_mk: item.kode_mk || item.kode,
    nama_mk: item.nama_mk || item.nama,
    sks: item.sks,
    nilai_asli: item.nilai || item.huruf || '',
    nilai_revisi: item.nilai_revisi || ''
  }));
  mkBaruDitambahkan.value = [];
  tabEditMode.value = 'revisi';
  showEditNilaiModal.value = true;
};

const tutupEditNilaiModal = () => {
  showEditNilaiModal.value = false;
  editNilaiId.value = null;
  editNilaiMhsName.value = '';
  editNilaiData.value = [];
  mkBaruDitambahkan.value = [];
};

const tambahMataKuliahKeNilai = () => {
  if (!formMKBaru.value.kode || !formMKBaru.value.nama_mk) {
    alert('Kode MK dan Nama Mata Kuliah wajib diisi!');
    return;
  }
  mkBaruDitambahkan.value.push({
    kode_mk: formMKBaru.value.kode,
    nama_mk: formMKBaru.value.nama_mk,
    sks: parseInt(formMKBaru.value.sks) || 2,
    nilai: formMKBaru.value.nilai || '',
    nilai_revisi: formMKBaru.value.nilai || ''
  });
  formMKBaru.value = { kode: '', nama_mk: '', sks: 2, kategori: 'Wajib', nilai: '' };
};

const hapusMKBaru = (index) => {
  if (confirm('Hapus mata kuliah ini?')) {
    mkBaruDitambahkan.value.splice(index, 1);
  }
};

const simpanPerubahanNilai = async () => {
  try {
    // Ambil data transkrip yang ada
    const response = await api.get(`transkrip-nilai/${editNilaiId.value}/`);
    const originalData = response.data;
    
    // Gabungkan data nilai yang sudah direvisi + yang baru ditambahkan
    const savedDataNilai = [];
    
    // Nilai yang sudah ada (dengan revisi)
    for (const item of editNilaiData.value) {
      savedDataNilai.push({
        kode_mk: item.kode_mk,
        nama_mk: item.nama_mk,
        sks: parseInt(item.sks) || 2,
        nilai: item.nilai_asli,
        nilai_revisi: item.nilai_revisi || ''
      });
    }
    
    // Tambahkan mata kuliah baru
    for (const item of mkBaruDitambahkan.value) {
      savedDataNilai.push({
        kode_mk: item.kode_mk,
        nama_mk: item.nama_mk,
        sks: parseInt(item.sks) || 2,
        nilai: item.nilai || '',
        nilai_revisi: item.nilai || ''
      });
    }
    
    // Kirim update ke server
    await api.put(`transkrip-nilai/${editNilaiId.value}/`, {
      pendaftaran: originalData.pendaftaran,
      data_nilai: savedDataNilai,
      status: 'MENUNGGU' // atau status yang sesuai
    });
    
    alert('✅ Perubahan nilai berhasil disimpan!');
    tutupEditNilaiModal();
    await fetchTranskrip(); // refresh data
  } catch (err) {
    console.error('Gagal simpan perubahan nilai:', err);
    alert('❌ Gagal menyimpan: ' + (err.response?.data?.error || err.message));
  }
};

watch([searchTranskrip, filterStatusTranskrip], () => currentPageTranskrip.value = 1);

// ========== FUNGSI PENDAFTARAN ==========
const fetchPendaftaran = async () => {
  try {
    const res = await api.get('pendaftaran-yudisium/');
    daftarPendaftaran.value = res.data;
  } catch (err) {
    console.error("Gagal fetch pendaftaran:", err);
  }
};

const filteredPendaftaran = computed(() => {
  return daftarPendaftaran.value.filter(item => {
    const matchSearch = !searchPendaftaran.value || (item.mahasiswa_nama || item.nama_lengkap || '').toLowerCase().includes(searchPendaftaran.value.toLowerCase()) || (item.nim || '').toLowerCase().includes(searchPendaftaran.value.toLowerCase());
    return matchSearch;
  });
});

const pendaftaranMenungguCount = computed(() => filteredPendaftaran.value.filter(i => i.status === 'MENUNGGU').length);
const pendaftaranDiverifikasiCount = computed(() => filteredPendaftaran.value.filter(i => i.status !== 'MENUNGGU').length);

const totalPagesPendaftaran = computed(() => Math.ceil(filteredPendaftaran.value.length / rowsPerPagePendaftaran.value));
const paginatedPendaftaran = computed(() => {
  const start = (currentPagePendaftaran.value - 1) * rowsPerPagePendaftaran.value;
  return filteredPendaftaran.value.slice(start, start + rowsPerPagePendaftaran.value);
});

const prevPagePendaftaran = () => { if (currentPagePendaftaran.value > 1) currentPagePendaftaran.value--; };
const nextPagePendaftaran = () => { if (currentPagePendaftaran.value < totalPagesPendaftaran.value) currentPagePendaftaran.value++; };
const resetFilterPendaftaran = () => { searchPendaftaran.value = ''; currentPagePendaftaran.value = 1; };

const bukaModalKomentarPendaftaran = (item) => {
  selectedPendaftaran.value = item;
  if (item.status === 'MENUNGGU') {
    catatanKomentarPendaftaran.value = 'Pendaftaran berhasil, silakan lanjutkan ke proses yudisium.';
  } else {
    catatanKomentarPendaftaran.value = item.catatan_baak || '';
  }
  showKomentarPendaftaranModal.value = true;
};

const closeKomentarPendaftaranModal = () => {
  showKomentarPendaftaranModal.value = false;
  selectedPendaftaran.value = null;
  catatanKomentarPendaftaran.value = '';
};

const kirimKomentarPendaftaran = async () => {
  if (!catatanKomentarPendaftaran.value.trim()) {
    alert('Komentar wajib diisi!');
    return;
  }
  isLoadingKomentar.value = true;
  try {
    await api.patch(`pendaftaran-yudisium/${selectedPendaftaran.value.id}/verifikasi/`, {
      catatan_baak: catatanKomentarPendaftaran.value,
      status: 'DISETUJUI'
    });
    alert('✅ Pendaftaran berhasil diverifikasi!');
    closeKomentarPendaftaranModal();
    await fetchPendaftaran();
  } catch (err) {
    console.error(err);
    alert('Gagal: ' + (err.response?.data?.error || err.message));
  } finally {
    isLoadingKomentar.value = false;
  }
};

watch(searchPendaftaran, () => currentPagePendaftaran.value = 1);

// ========== FUNGSI PERPUSTAKAAN ==========
const fetchPerpus = async () => {
  try {
    const res = await api.get('bebas-perpus/');
    daftarPerpus.value = res.data.map(m => ({ ...m, jurusan: m.jurusan || 'Akuntansi' }));
    daftarPerpus.value.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  } catch (err) {
    console.error("Gagal fetch perpus:", err);
  }
};

const perpusMenungguCount = computed(() => daftarPerpus.value.filter(i => i.status === 'MENUNGGU').length);
const perpusDisetujuiCount = computed(() => daftarPerpus.value.filter(i => i.status === 'DISETUJUI').length);
const perpusDitolakCount = computed(() => daftarPerpus.value.filter(i => i.status === 'DITOLAK').length);

const filteredPerpus = computed(() => {
  return daftarPerpus.value.filter(item => {
    const matchStatus = !filterStatusPerpus.value || item.status === filterStatusPerpus.value;
    const matchSearch = !searchPerpus.value ||
      (item.full_name || '').toLowerCase().includes(searchPerpus.value.toLowerCase()) ||
      (item.nim || '').toLowerCase().includes(searchPerpus.value.toLowerCase());
    return matchStatus && matchSearch;
  });
});

const totalPagesPerpus = computed(() => Math.ceil(filteredPerpus.value.length / rowsPerPagePerpus.value));
const paginatedPerpus = computed(() => {
  const start = (currentPagePerpus.value - 1) * rowsPerPagePerpus.value;
  return filteredPerpus.value.slice(start, start + rowsPerPagePerpus.value);
});

const prevPagePerpus = () => { if (currentPagePerpus.value > 1) currentPagePerpus.value--; };
const nextPagePerpus = () => { if (currentPagePerpus.value < totalPagesPerpus.value) currentPagePerpus.value++; };
const resetFilterPerpus = () => { searchPerpus.value = ''; filterStatusPerpus.value = ''; currentPagePerpus.value = 1; };

const getAllFilesCount = (item) => {
  if (!item) return 0;
  let count = item.file_abstrak ? 1 : 0;
  const fileFields = ['bagian_awal', 'bab1', 'bab2', 'bab3', 'bab4', 'bab5', 'daftar_pustaka', 'lampiran', 'jurnal_publikasi', 'lampiran_cetak', 'cek_plagiasi_jurnal'];
  count += fileFields.filter(field => item[field]).length;
  return count;
};

const getAllFilesList = (item) => {
  if (!item) return [];
  const files = [];
  if (item.file_abstrak) files.push({ key: 'file_abstrak', url: item.file_abstrak, label: 'File Abstrak PDF' });
  const fileFields = [
    { key: 'bagian_awal', label: 'Bagian Awal' },
    { key: 'bab1', label: 'Bab 1 - Pendahuluan' },
    { key: 'bab2', label: 'Bab 2 - Tinjauan Pustaka' },
    { key: 'bab3', label: 'Bab 3 - Metodologi' },
    { key: 'bab4', label: 'Bab 4 - Hasil & Pembahasan' },
    { key: 'bab5', label: 'Bab 5 - Kesimpulan' },
    { key: 'daftar_pustaka', label: 'Daftar Pustaka' },
    { key: 'lampiran', label: 'Lampiran' },
    { key: 'jurnal_publikasi', label: 'Jurnal Publikasi' },
    { key: 'lampiran_cetak', label: 'Lampiran Cetak' },
    { key: 'cek_plagiasi_jurnal', label: 'Cek Plagiasi Jurnal' }
  ];
  fileFields.forEach(field => {
    if (item[field.key]) {
      files.push({ key: field.key, url: item[field.key], label: field.label });
    }
  });
  return files;
};

const openBerkasModalPerpus = (item) => {
  selectedBerkasPerpus.value = item;
  showBerkasPerpusModal.value = true;
};

const openTemplateModalPerpus = () => { showTemplateModalPerpus.value = true; };
const simpanTemplateSuratPerpus = () => {
  localStorage.setItem('template_surat_perpus_admin', templateSuratPerpus.value);
  alert('Template surat berhasil disimpan!');
  showTemplateModalPerpus.value = false;
};

const loadTemplatePerpus = () => {
  const saved = localStorage.getItem('template_surat_perpus_admin');
  if (saved) templateSuratPerpus.value = saved;
};

const openTtdModalPerpus = () => { showTtdModalPerpus.value = true; };

const loadTtdPerpus = async () => {
  try {
    const res = await api.get('ttd-perpus/');
    if (res.data.ttd_url) {
      const fullUrl = getFullImageUrl(res.data.ttd_url);
      ttdPerpusImage.value = fullUrl;
      ttdPerpusPreview.value = fullUrl;
      ttdPerpusUrl.value = res.data.ttd_url;
    }
  } catch (err) {
    const saved = localStorage.getItem('ttd_perpus_admin');
    if (saved) {
      ttdPerpusImage.value = saved;
      ttdPerpusPreview.value = saved;
    }
  }
};

const uploadTtdPerpus = async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  if (!file.type.match('image/png') && !file.type.match('image/jpeg')) {
    alert('Hanya PNG/JPG!');
    return;
  }
  const localPreview = URL.createObjectURL(file);
  ttdPerpusPreview.value = localPreview;
  ttdPerpusImage.value = localPreview;
  const formData = new FormData();
  formData.append('ttd', file);
  try {
    const res = await api.post('upload-ttd/', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
    if (res.data.ttd_url) {
      const fullUrl = getFullImageUrl(res.data.ttd_url);
      ttdPerpusImage.value = fullUrl;
      ttdPerpusPreview.value = fullUrl;
      ttdPerpusUrl.value = res.data.ttd_url;
      alert('TTD berhasil disimpan!');
      showTtdModalPerpus.value = false;
    }
  } catch (err) {
    localStorage.setItem('ttd_perpus_admin', localPreview);
    alert('TTD disimpan di browser (fallback)');
    showTtdModalPerpus.value = false;
  }
};

const hapusTtdPerpus = async () => {
  try {
    await api.delete('ttd-perpus/');
    ttdPerpusImage.value = null;
    ttdPerpusPreview.value = null;
    ttdPerpusUrl.value = null;
    localStorage.removeItem('ttd_perpus_admin');
    alert('TTD dihapus!');
    showTtdModalPerpus.value = false;
  } catch (err) {
    localStorage.removeItem('ttd_perpus_admin');
    ttdPerpusImage.value = null;
    ttdPerpusPreview.value = null;
    alert('TTD dihapus (fallback)');
    showTtdModalPerpus.value = false;
  }
};

const getTanggalIndonesia = () => {
  const date = new Date();
  const bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];
  return `${date.getDate()} ${bulan[date.getMonth()]} ${date.getFullYear()}`;
};

const generateSuratFromTemplatePerpus = (mhs) => {
  if (!mhs) return '';
  let surat = templateSuratPerpus.value;
  surat = surat.replace(/\[NAMA\]/g, mhs.full_name || '-');
  surat = surat.replace(/\[NIM\]/g, mhs.nim || '-');
  surat = surat.replace(/\[JURUSAN\]/g, mhs.jurusan || 'Akuntansi');
  surat = surat.replace(/\[TANGGAL\]/g, tanggalSuratPerpus.value);
  surat = surat.replace(/\[PETUGAS\]/g, petugasNamePerpus.value || user.value.full_name || 'Petugas Perpustakaan');
  return surat;
};

const bukaModalSuratPerpus = (mhs) => {
  selectedPerpusMhs.value = mhs;
  petugasNamePerpus.value = user.value.full_name || '';
  tanggalSuratPerpus.value = getTanggalIndonesia();
  isiSuratPerpus.value = generateSuratFromTemplatePerpus(mhs);
  if (mhs.ttd_position_x) ttdPerpusPositionX.value = mhs.ttd_position_x;
  if (mhs.ttd_position_y) ttdPerpusPositionY.value = mhs.ttd_position_y;
  showSuratPerpusModal.value = true;
};

const resetKeTemplatePerpus = () => {
  if (selectedPerpusMhs.value) {
    isiSuratPerpus.value = generateSuratFromTemplatePerpus(selectedPerpusMhs.value);
  }
};

const generateAndSendPDFPerpus = async () => {
  if (!selectedPerpusMhs.value) {
    alert('Error: Tidak ada mahasiswa dipilih!');
    return;
  }
  const loadingToast = document.createElement('div');
  loadingToast.className = 'fixed bottom-4 right-4 bg-indigo-600 text-white px-4 py-2 rounded-lg shadow-lg z-50';
  loadingToast.innerHTML = '⏳ Sedang memproses surat...';
  document.body.appendChild(loadingToast);

  try {
    const formData = new FormData();
    formData.append('pengajuan_id', selectedPerpusMhs.value.id || '');
    formData.append('nim', selectedPerpusMhs.value.nim || '');
    formData.append('email', selectedPerpusMhs.value.email || '');
    let namaMahasiswa = selectedPerpusMhs.value.full_name || selectedPerpusMhs.value.mahasiswa_nama || selectedPerpusMhs.value.nama || 'Mahasiswa';
    let prodiMahasiswa = selectedPerpusMhs.value.jurusan || selectedPerpusMhs.value.program_studi || selectedPerpusMhs.value.prodi || 'Akuntansi';
    formData.append('full_name', namaMahasiswa);
    formData.append('prodi', prodiMahasiswa);
    formData.append('catatan_perpus', catatanTambahanPerpus.value || '');
    formData.append('ttd_position_x', String(ttdPerpusPositionX.value));
    formData.append('ttd_position_y', String(ttdPerpusPositionY.value));
    if (ttdPerpusImage.value && ttdPerpusImage.value.startsWith('data:image')) {
      formData.append('ttd_base64', ttdPerpusImage.value);
    } else if (ttdPerpusUrl.value) {
      formData.append('ttd_petugas', ttdPerpusUrl.value);
    }
    const response = await api.post('generate-surat-pdf/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 60000
    });
    loadingToast.remove();
    if (response.data.success) {
      alert(`✅ Surat PDF berhasil dibuat untuk ${namaMahasiswa}!`);
      showSuratPerpusModal.value = false;
      catatanTambahanPerpus.value = '';
      await fetchPerpus();
    } else {
      alert('❌ Gagal: ' + (response.data.error || 'Unknown error'));
    }
  } catch (err) {
    loadingToast.remove();
    alert(`❌ Gagal generate PDF: ${err.response?.data?.error || err.message}`);
  }
};

const setujuiPerpus = async (mhs) => {
  if (!confirm(`Setujui pengajuan ${mhs.full_name || mhs.nim}?`)) return;
  try {
    const res = await api.post(`bebas-perpus/${mhs.id}/verifikasi/`, {
      status: 'DISETUJUI',
      catatan_perpus: ''
    });
    if (res.data.success) {
      alert('✅ Berkas disetujui!');
      await fetchPerpus();
      bukaModalSuratPerpus(mhs);
    } else {
      alert('❌ Gagal: ' + (res.data.error || 'Unknown error'));
    }
  } catch (err) {
    alert('Gagal: ' + (err.response?.data?.error || err.message));
  }
};

const openTolakPerpusModal = (id, nama) => {
  tolakPerpusId.value = id;
  tolakPerpusName.value = nama;
  catatanTolakPerpus.value = '';
  showTolakPerpusModal.value = true;
};

const confirmTolakPerpus = async () => {
  if (!catatanTolakPerpus.value.trim()) {
    alert('Alasan penolakan wajib diisi!');
    return;
  }
  try {
    const res = await api.post(`bebas-perpus/${tolakPerpusId.value}/verifikasi/`, {
      status: 'DITOLAK',
      catatan_perpus: catatanTolakPerpus.value
    });
    if (res.data.success) {
      alert('✅ Berkas ditolak! Notifikasi dikirim.');
      showTolakPerpusModal.value = false;
      catatanTolakPerpus.value = '';
      await fetchPerpus();
    } else {
      alert('❌ Gagal: ' + (res.data.error || 'Unknown error'));
    }
  } catch (err) {
    alert('Gagal: ' + (err.response?.data?.error || err.message));
  }
};

const fetchLogo = async () => {
  try {
    const res = await api.get('get-logo/');
    if (res.data.success && res.data.logo_url) {
      logoUrl.value = res.data.logo_url;
    } else {
      logoUrl.value = '/stie-sbilogo.png';
    }
  } catch (err) {
    logoUrl.value = '/stie-sbilogo.png';
  }
};

watch([searchPerpus, filterStatusPerpus], () => currentPagePerpus.value = 1);

// ========== FUNGSI PERIODE ==========
const fetchPeriode = async () => {
  try {
    const res = await api.get('periode-yudisium/');
    listPeriode.value = res.data;
  } catch (err) {
    console.error("Gagal ambil periode:", err);
  }
};

const bukaFormPeriode = (periode = null) => {
  if (periode) {
    isEditPeriode.value = true;
    editPeriodeId.value = periode.id;
    formPeriode.value = {
      nama_periode: periode.nama_periode,
      tanggal_mulai: periode.tanggal_mulai,
      tanggal_selesai: periode.tanggal_selesai
    };
  } else {
    isEditPeriode.value = false;
    editPeriodeId.value = null;
    formPeriode.value = { nama_periode: '', tanggal_mulai: '', tanggal_selesai: '' };
  }
  showModalPeriode.value = true;
};

const simpanPeriode = async () => {
  try {
    if (isEditPeriode.value) {
      await api.put(`periode-yudisium/${editPeriodeId.value}/`, formPeriode.value);
      alert('Periode berhasil diperbarui!');
    } else {
      await api.post('periode-yudisium/', formPeriode.value);
      alert('Periode baru berhasil ditambahkan!');
    }
    showModalPeriode.value = false;
    await fetchPeriode();
  } catch (err) {
    console.error("Gagal simpan periode:", err);
    alert('Gagal menyimpan periode: ' + (err.response?.data?.error || err.message));
  }
};

const hapusPeriode = async (id) => {
  if (!confirm('Yakin ingin menghapus periode ini?')) return;
  try {
    await api.delete(`periode-yudisium/${id}/`);
    alert('Periode berhasil dihapus.');
    await fetchPeriode();
  } catch (err) {
    console.error("Gagal hapus periode:", err);
    alert('Gagal menghapus periode.');
  }
};

const toggleAktif = async (periode) => {
  const newStatus = !periode.is_active;
  try {
    await api.patch(`periode-yudisium/${periode.id}/`, { is_active: newStatus });
    alert(`Periode berhasil ${newStatus ? 'diaktifkan' : 'dinonaktifkan'}.`);
    await fetchPeriode();
  } catch (err) {
    console.error("Gagal toggle status:", err);
    alert('Gagal mengubah status periode.');
  }
};

// ========== LOGOUT ==========
const handleLogout = () => {
  if (confirm("Keluar dari dashboard?")) {
    localStorage.clear();
    router.replace({ name: 'login' });
  }
};

// ========== WATCHERS ==========
watch([searchAkademik, filterStatusAkademik], () => currentPageAkademik.value = 1);

// ========== MOUNTED ==========
onMounted(async () => {
  await fetchAkademik();
  await fetchUsers();
  await fetchMataKuliah();
  await fetchTranskrip();
  await fetchPendaftaran();
  await fetchPeriode();
  await fetchPerpus();
  await fetchLogo();
  loadTemplatePerpus();
  loadTtdPerpus();
  tanggalSuratPerpus.value = getTanggalIndonesia();
});
</script>

<style scoped>
.animate-in { animation: fadeIn 0.4s ease-out; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.transition-all { transition-property: all; }
#suratPreviewPerpus {
  font-family: 'Times New Roman', Times, serif;
}
</style>
