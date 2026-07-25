<template>
  <div class="flex h-screen bg-gradient-to-br from-gray-50 to-gray-100">
    <!-- SIDEBAR - LEFT PANEL -->
    <aside class="w-64 bg-slate-900 text-white hidden md:flex flex-col shadow-xl">
      <div class="p-6 text-xl font-bold border-b border-indigo-700 flex items-center gap-3">
        <span class="p-2 bg-white/10 rounded-xl text-white text-lg">🏛️</span>
        <span>Panel BAAK</span>
      </div>
      <nav class="flex-1 p-4 space-y-2">
        <p class="text-[10px] text-indigo-300 font-bold px-4 mb-2 uppercase tracking-widest">Menu Utama</p>
        
        <button @click="activeMenu = 'matakuliah'; resetPagination()" 
                :class="activeMenu === 'matakuliah' ? 'bg-indigo-700 shadow-lg' : 'hover:bg-indigo-800/70'"
                class="w-full flex items-center space-x-3 py-3 px-4 rounded-xl transition-all text-left font-medium">
          <span>📚</span>
          <span>Kelola Mata Kuliah</span>
        </button>

        <button @click="activeMenu = 'antrian'; resetPagination()" 
                :class="activeMenu === 'antrian' ? 'bg-indigo-700 shadow-lg' : 'hover:bg-indigo-800/70'"
                class="w-full flex items-center space-x-3 py-3 px-4 rounded-xl transition-all text-left font-medium">
          <span>📋</span>
          <span>Antrian Transkrip</span>
          <span v-if="antrian.length > 0" class="ml-auto bg-red-500 text-white text-[10px] rounded-full px-2 py-0.5">{{ antrian.length }}</span>
        </button>

        <button @click="activeMenu = 'riwayat'; resetPagination(); refreshRiwayatData()" 
                :class="activeMenu === 'riwayat' ? 'bg-indigo-700 shadow-lg' : 'hover:bg-indigo-800/70'"
                class="w-full flex items-center space-x-3 py-3 px-4 rounded-xl transition-all text-left font-medium">
          <span>🕒</span>
          <span>Riwayat Validasi</span>
        </button>

        <button @click="activeMenu = 'daftar'; resetPagination()" 
                :class="activeMenu === 'daftar' ? 'bg-indigo-700 shadow-lg' : 'hover:bg-indigo-800/70'"
                class="w-full flex items-center space-x-3 py-3 px-4 rounded-xl transition-all text-left font-medium">
          <span>👥</span>
          <span>Monitoring Mahasiswa</span>
        </button>

        <button @click="activeMenu = 'pendaftaran'; resetPagination(); fetchPendaftaranYudisium()" 
                :class="activeMenu === 'pendaftaran' ? 'bg-indigo-700 shadow-lg' : 'hover:bg-indigo-800/70'"
                class="w-full flex items-center space-x-3 py-3 px-4 rounded-xl transition-all text-left font-medium">
          <span>📋</span>
          <span>Pendaftaran Yudisium</span>
          <span v-if="pendaftaranMenungguCount > 0" class="ml-auto bg-green-500 text-white text-[10px] rounded-full px-2 py-0.5">{{ pendaftaranMenungguCount }}</span>
        </button>
      </nav>
      <div class="p-4 border-t border-indigo-700">
        <button @click="handleLogout" class="w-full bg-red-600/80 hover:bg-red-600 py-2.5 rounded-xl text-sm font-bold transition-all">
          🚪 Keluar Sistem
        </button>
      </div>
    </aside>

    <!-- MAIN CONTENT - RIGHT PANEL -->
    <main class="flex-1 flex flex-col overflow-hidden">
      <header class="bg-white/80 backdrop-blur-md border-b border-gray-200 py-4 px-8 flex justify-between items-center sticky top-0 z-10 shadow-sm">
        <div>
          <h1 class="text-xl font-bold text-gray-800">{{ headerTitle }}</h1>
          <p class="text-xs text-gray-500">Selamat datang, {{ user.full_name || 'Petugas BAAK' }}</p>
        </div>
        <div class="flex items-center gap-4">
          <div class="text-right">
            <p class="text-sm font-bold text-gray-800">{{ user.username }}</p>
            <span class="text-[10px] bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full font-bold uppercase tracking-wider">Petugas BAAK</span>
          </div>
          <div class="w-8 h-8 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold">
            {{ (user.full_name || user.username || 'B').charAt(0).toUpperCase() }}
          </div>
        </div>
      </header>

      <section class="flex-1 overflow-y-auto p-6 md:p-8 space-y-6">

        <!-- MENU MATA KULIAH (sama seperti sebelumnya) -->
        <div v-if="activeMenu === 'matakuliah'" class="space-y-6">
          <!-- ... konten mata kuliah tetap sama ... -->
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

        <!-- MENU ANTRIAN TRANSKRIP (sama seperti sebelumnya) -->
        <div v-if="activeMenu === 'antrian'" class="space-y-6">
          <!-- ... konten antrian tetap sama ... -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div class="bg-white p-5 rounded-2xl shadow-md border-l-4 border-orange-500">
              <p class="text-xs text-gray-400 uppercase tracking-wide">Antrian Menunggu</p>
              <h3 class="text-3xl font-bold text-orange-600">{{ antrian.length }}</h3>
            </div>
            <div class="bg-white p-5 rounded-2xl shadow-md border-l-4 border-green-500">
              <p class="text-xs text-gray-400 uppercase tracking-wide">Sudah Disetujui</p>
              <h3 class="text-3xl font-bold text-green-600">{{ semuaRiwayatBerkas.filter(i => getStatus(i) === 'DISETUJUI').length }}</h3>
            </div>
            <div class="bg-white p-5 rounded-2xl shadow-md border-l-4 border-red-500">
              <p class="text-xs text-gray-400 uppercase tracking-wide">Ditolak</p>
              <h3 class="text-3xl font-bold text-red-600">{{ semuaRiwayatBerkas.filter(i => getStatus(i) === 'DITOLAK').length }}</h3>
            </div>
          </div>

          <div class="bg-white rounded-2xl shadow-md border border-gray-100 overflow-hidden">
            <div class="p-4 border-b bg-gray-50">
              <input type="text" v-model="searchAntrian" placeholder="🔍 Cari Nama Mahasiswa atau NIM..." class="w-full md:w-80 border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-indigo-400 outline-none transition">
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead class="bg-gray-50 text-gray-500 text-[11px] uppercase">
                  <tr>
                    <th class="px-5 py-3">Mahasiswa</th>
                    <th class="px-5 py-3">NIM</th>
                    <th class="px-5 py-3">Berkas Transkrip</th>
                    <th class="px-5 py-3 text-center">Aksi</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                  <tr v-for="item in paginatedAntrian" :key="item.id" class="hover:bg-gray-50 transition">
                    <td class="px-5 py-3 font-medium">{{ item.full_name || item.mahasiswa_nama || '-' }}</td>
                    <td class="px-5 py-3 font-mono text-sm">{{ item.nim || item.mahasiswa_nim || '-' }}</td>
                    <td class="px-5 py-3">
                      <div class="flex flex-col gap-1">
                        <a v-if="getFileUrl(item)" :href="getFileUrl(item)" target="_blank" class="text-indigo-600 text-sm hover:underline inline-flex items-center gap-1">📄 Lihat PDF</a>
                        <button v-if="item.data_nilai?.length" @click="bukaModalNilai(item.data_nilai, item.full_name, item.nim)" class="text-blue-600 text-sm text-left hover:underline">📊 Lihat Nilai</button>
                        <button v-if="item.data_nilai?.length" @click="openEditNilaiModal(item.id, item.full_name, item.data_nilai)" class="text-amber-600 text-sm text-left hover:underline">✏️ Edit/Revisi Nilai</button>
                        <span v-if="!item.file_transkrip && !item.data_nilai?.length" class="text-gray-400 text-sm">Belum ada data</span>
                      </div>
                    </td>
                    <td class="px-5 py-3 text-center">
                      <div class="flex justify-center gap-2">
                        <button @click="verifikasiTranskrip(item.id, 'DISETUJUI')" class="bg-green-500 hover:bg-green-600 text-white px-3 py-1.5 rounded-lg text-xs font-bold transition shadow-sm">✅ Setujui</button>
                        <button @click="openTolakTranskripModal(item.id, item.full_name)" class="bg-red-500 hover:bg-red-600 text-white px-3 py-1.5 rounded-lg text-xs font-bold transition shadow-sm">❌ Tolak</button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="paginatedAntrian.length === 0">
                    <td colspan="4" class="px-5 py-10 text-center text-gray-400">📭 Tidak ada antrian validasi</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="px-5 py-3 border-t flex flex-wrap gap-3 justify-between items-center bg-gray-50 text-sm">
              <span class="text-gray-500">Menampilkan {{ filteredAntrian.length }} dari {{ antrian.length }} antrian</span>
              <div class="flex gap-2 items-center">
                <button @click="prevPageAntrian" :disabled="currentPageAntrian===1" class="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-100 transition">Prev</button>
                <span class="text-sm">Halaman {{ currentPageAntrian }} / {{ totalPagesAntrian }}</span>
                <button @click="nextPageAntrian" :disabled="currentPageAntrian===totalPagesAntrian" class="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-100 transition">Next</button>
              </div>
              <select v-model="rowsPerPageAntrian" class="border rounded-lg px-2 py-1 text-sm bg-white">
                <option :value="10">10</option>
                <option :value="25">25</option>
                <option :value="50">50</option>
              </select>
            </div>
          </div>
        </div>

        <!-- MENU RIWAYAT VALIDASI (sama seperti sebelumnya) -->
        <div v-if="activeMenu === 'riwayat'" class="space-y-6">
          <!-- ... konten riwayat tetap sama ... -->
          <div class="flex justify-between items-center gap-3 flex-wrap">
            <div class="bg-blue-50 p-3 rounded-xl text-sm border border-blue-200 flex-1">
              <p class="font-bold text-blue-700">📊 Informasi Data</p>
              <p class="text-blue-600 text-xs">Total data: {{ semuaRiwayatBerkas.length }} | Dengan berkas: {{ totalDataDenganBerkas }} | Disetujui: {{ totalDisetujui }} | Ditolak: {{ totalDitolak }} | Menunggu: {{ totalMenunggu }}</p>
            </div>
            <button @click="refreshRiwayatData" class="bg-indigo-500 hover:bg-indigo-600 text-white px-4 py-2.5 rounded-xl text-sm font-bold transition shadow-md flex items-center gap-2">
              🔄 Refresh Data
            </button>
          </div>

          <div class="bg-white p-4 rounded-xl shadow-md border border-gray-100">
            <div class="flex flex-col md:flex-row gap-3">
              <input type="text" v-model="searchRiwayat" placeholder="🔍 Cari Nama/NIM..." class="flex-1 border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-indigo-400 outline-none">
              <select v-model="filterStatusRiwayat" class="w-44 border border-gray-200 rounded-xl px-4 py-2.5 text-sm bg-white focus:ring-2 focus:ring-indigo-400 outline-none">
                <option value="">Semua Status</option>
                <option value="DISETUJUI">✅ Disetujui</option>
                <option value="DITOLAK">❌ Ditolak</option>
                <option value="MENUNGGU">⏳ Menunggu</option>
              </select>
              <button @click="resetRiwayatFilter" class="bg-gray-200 hover:bg-gray-300 px-4 py-2.5 rounded-xl text-sm font-medium transition">Reset Filter</button>
            </div>
          </div>

          <div class="bg-white rounded-2xl shadow-md border border-gray-100 overflow-hidden">
            <div class="p-4 border-b bg-indigo-50/50 flex justify-between items-center">
              <h3 class="font-bold text-indigo-900">📜 Riwayat Validasi Transkrip</h3>
              <span class="text-xs bg-indigo-200 text-indigo-800 px-3 py-1 rounded-full">Total: {{ filteredRiwayat.length }} data</span>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead class="bg-gray-50 text-gray-500 text-[11px] uppercase">
                  <tr>
                    <th class="px-5 py-3">Mahasiswa</th>
                    <th class="px-5 py-3">NIM</th>
                    <th class="px-5 py-3">Berkas Transkrip</th>
                    <th class="px-5 py-3 text-center w-28">Status</th>
                    <th class="px-5 py-3">Catatan</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                  <tr v-for="item in paginatedRiwayat" :key="item.id" class="hover:bg-gray-50 transition">
                    <td class="px-5 py-3 font-medium">{{ item.full_name || item.mahasiswa_nama || '-' }}</td>
                    <td class="px-5 py-3 font-mono text-sm">{{ item.nim || item.mahasiswa_nim || '-' }}</td>
                    <td class="px-5 py-3">
                      <div class="flex flex-col gap-1">
                        <a v-if="getFileUrl(item)" :href="getFileUrl(item)" target="_blank" class="text-indigo-600 text-sm hover:underline inline-flex items-center gap-1">📄 Lihat Berkas</a>
                        <button v-if="item.data_nilai && item.data_nilai.length" @click="bukaModalNilai(item.data_nilai, item.full_name || item.mahasiswa_nama, item.nim || item.mahasiswa_nim)" class="text-blue-600 text-sm text-left hover:underline">📊 Lihat Detail Nilai</button>
                      </div>
                    </td>
                    <td class="px-5 py-3 text-center">
                      <span :class="getBadgeClass(getStatus(item))" class="px-2 py-0.5 rounded-full text-[10px] font-bold">
                        {{ getStatusText(getStatus(item)) }}
                      </span>
                    </td>
                    <td class="px-5 py-3 text-sm max-w-[250px] break-words" :title="item.catatan_dpa || item.catatan_baak">
                      {{ item.catatan_dpa || item.catatan_baak || '-' }}
                    </td>
                  </tr>
                  <tr v-if="paginatedRiwayat.length === 0">
                    <td colspan="5" class="px-5 py-10 text-center text-gray-400">
                      📭 Tidak ada data riwayat validasi
                      <button @click="refreshRiwayatData" class="ml-2 text-indigo-600 hover:underline">Refresh</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="px-5 py-3 border-t flex flex-wrap gap-3 justify-between items-center bg-gray-50 text-sm">
              <span class="text-gray-500">Menampilkan {{ ((currentPageRiwayat-1)*rowsPerPageRiwayat)+1 }} - {{ Math.min(currentPageRiwayat*rowsPerPageRiwayat, filteredRiwayat.length) }} dari {{ filteredRiwayat.length }} data</span>
              <div class="flex gap-2 items-center">
                <button @click="prevPageRiwayat" :disabled="currentPageRiwayat===1" class="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-100 transition">Prev</button>
                <span class="text-sm">Halaman {{ currentPageRiwayat }} / {{ totalPagesRiwayat }}</span>
                <button @click="nextPageRiwayat" :disabled="currentPageRiwayat===totalPagesRiwayat" class="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-100 transition">Next</button>
              </div>
              <select v-model="rowsPerPageRiwayat" class="border rounded-lg px-2 py-1 text-sm bg-white">
                <option :value="10">10</option>
                <option :value="25">25</option>
                <option :value="50">50</option>
                <option :value="100">100</option>
              </select>
            </div>
          </div>
        </div>

        <!-- MENU MONITORING MAHASISWA (sama seperti sebelumnya) -->
        <div v-if="activeMenu === 'daftar'" class="space-y-6">
          <!-- ... konten monitoring tetap sama ... -->
          <div class="bg-white p-4 rounded-xl shadow-md border border-gray-100">
            <div class="flex flex-col md:flex-row gap-3">
              <input type="text" v-model="searchMonitoring" placeholder="🔍 Cari Nama/NIM..." class="flex-1 border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-indigo-400 outline-none">
              <select v-model="filterStatusTranskrip" class="w-44 border border-gray-200 rounded-xl px-4 py-2.5 text-sm bg-white focus:ring-2 focus:ring-indigo-400 outline-none">
                <option value="">Semua Status</option>
                <option value="MENUNGGU">⏳ Menunggu</option>
                <option value="DISETUJUI">✅ Disetujui</option>
                <option value="DITOLAK">❌ Ditolak</option>
              </select>
            </div>
          </div>

          <div class="bg-white rounded-2xl shadow-md border border-gray-100 overflow-hidden">
            <div class="p-4 border-b bg-indigo-50/50 flex justify-between items-center">
              <h3 class="font-bold text-indigo-900">📊 Monitoring Kelengkapan Yudisium</h3>
              <span class="text-xs bg-indigo-200 text-indigo-800 px-3 py-1 rounded-full">Total: {{ filteredMonitoring.length }} Mahasiswa</span>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead class="bg-gray-50 text-gray-500 text-[11px] uppercase">
                  <tr>
                    <th class="px-5 py-3">Mahasiswa</th>
                    <th class="px-5 py-3">NIM</th>
                    <th class="px-5 py-3 text-center w-28">Transkrip</th>
                    <th class="px-5 py-3 text-center w-28">Bebas Perpus</th>
                    <th class="px-5 py-3 text-center w-28">Akademik</th>
                    <th class="px-5 py-3 text-center w-28">Status Akhir</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                  <tr v-for="mhs in paginatedMonitoring" :key="mhs.id" @click="lihatRiwayat(mhs)" class="hover:bg-indigo-50/50 cursor-pointer transition">
                    <td class="px-5 py-3 font-medium">{{ mhs.full_name || '-' }}</td>
                    <td class="px-5 py-3 font-mono text-sm">{{ mhs.nim || '-' }}</td>
                    <td class="px-5 py-3 text-center">
                      <span :class="getBadgeClass(mhs.status_transkrip || mhs.status)">{{ getStatusText(mhs.status_transkrip || mhs.status || 'BELUM') }}</span>
                    </td>
                    <td class="px-5 py-3 text-center">
                      <span :class="getBadgeClass(mhs.status_perpus)">{{ getStatusText(mhs.status_perpus || 'BELUM') }}</span>
                    </td>
                    <td class="px-5 py-3 text-center">
                      <span :class="getBadgeClass(mhs.status_akademik)">{{ getStatusText(mhs.status_akademik || 'BELUM') }}</span>
                    </td>
                    <td class="px-5 py-3 text-center">
                      <span :class="getBadgeClass(mhs.status_akhir)">{{ getStatusText(mhs.status_akhir || 'PROSES') }}</span>
                    </td>
                  </tr>
                  <tr v-if="paginatedMonitoring.length === 0">
                    <td colspan="6" class="px-5 py-10 text-center text-gray-400">📭 Belum ada data mahasiswa</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="px-5 py-3 border-t flex flex-wrap gap-3 justify-between items-center bg-gray-50 text-sm">
              <span class="text-gray-500">Menampilkan {{ ((currentPageMonitoring-1)*rowsPerPageMonitoring)+1 }} - {{ Math.min(currentPageMonitoring*rowsPerPageMonitoring, filteredMonitoring.length) }} dari {{ filteredMonitoring.length }}</span>
              <div class="flex gap-2 items-center">
                <button @click="prevPageMonitoring" :disabled="currentPageMonitoring===1" class="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-100 transition">Prev</button>
                <span class="text-sm">Halaman {{ currentPageMonitoring }} / {{ totalPagesMonitoring }}</span>
                <button @click="nextPageMonitoring" :disabled="currentPageMonitoring===totalPagesMonitoring" class="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-100 transition">Next</button>
              </div>
              <select v-model="rowsPerPageMonitoring" class="border rounded-lg px-2 py-1 text-sm bg-white">
                <option :value="10">10</option>
                <option :value="25">25</option>
                <option :value="50">50</option>
              </select>
            </div>
          </div>
        </div>

        <!-- ==================== MENU PENDAFTARAN YUDISIUM DENGAN DOWNLOAD EXCEL ==================== -->
        <div v-if="activeMenu === 'pendaftaran'" class="space-y-6">
          <!-- Tombol Aksi -->
          <div class="flex justify-between items-center gap-3 flex-wrap">
            <div class="flex gap-2">
              <button @click="manualRefresh" class="bg-indigo-500 hover:bg-indigo-600 text-white px-4 py-2.5 rounded-xl text-sm font-bold transition shadow-md flex items-center gap-2">
                🔄 Refresh Data
              </button>
              <button @click="exportPendaftaranToExcel" class="bg-green-500 hover:bg-green-600 text-white px-4 py-2.5 rounded-xl text-sm font-bold transition shadow-md flex items-center gap-2">
                📊 Download Excel
              </button>
            </div>
            <div class="text-sm text-gray-500">
              * Klik "Download Excel" untuk mengekspor semua data pendaftaran yudisium
            </div>
          </div>

          <!-- Statistik -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="bg-blue-50 p-4 rounded-xl border border-blue-200">
              <p class="text-xs text-blue-600 font-bold">TOTAL PENDAFTARAN</p>
              <p class="text-2xl font-bold text-blue-700">{{ filteredPendaftaran.length }}</p>
            </div>
            <div class="bg-orange-50 p-4 rounded-xl border border-orange-200">
              <p class="text-xs text-orange-600 font-bold">MENUNGGU VERIFIKASI</p>
              <p class="text-2xl font-bold text-orange-700">{{ pendaftaranMenungguCount }}</p>
            </div>
            <div class="bg-green-50 p-4 rounded-xl border border-green-200">
              <p class="text-xs text-green-600 font-bold">SUDAH DIVERIFIKASI</p>
              <p class="text-2xl font-bold text-green-700">{{ filteredPendaftaran.length - pendaftaranMenungguCount }}</p>
            </div>
            <div class="bg-purple-50 p-4 rounded-xl border border-purple-200">
              <p class="text-xs text-purple-600 font-bold">DATA SIAP EKSPOR</p>
              <p class="text-2xl font-bold text-purple-700">{{ filteredPendaftaran.length }}</p>
            </div>
          </div>

          <!-- Pencarian -->
          <div class="bg-white p-4 rounded-xl shadow-md border border-gray-100">
            <div class="flex flex-col md:flex-row gap-3">
              <input type="text" v-model="searchPendaftaran" placeholder="🔍 Cari Nama Mahasiswa atau NIM..." 
                     class="flex-1 border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:ring-2 focus:ring-indigo-400 outline-none transition">
              <button @click="resetPendaftaranFilter" class="bg-gray-200 hover:bg-gray-300 px-4 py-2.5 rounded-xl text-sm font-medium transition">
                Reset Filter
              </button>
            </div>
          </div>

          <!-- Tabel Data Pendaftaran Yudisium -->
          <div class="bg-white rounded-2xl shadow-md border border-gray-100 overflow-hidden">
            <div class="p-4 border-b bg-indigo-50/50 flex justify-between items-center">
              <h3 class="font-bold text-indigo-900">📋 Data Pendaftaran Yudisium</h3>
              <span class="text-xs bg-indigo-200 text-indigo-800 px-3 py-1 rounded-full">Total: {{ filteredPendaftaran.length }} pendaftaran</span>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse" id="pendaftaran-table">
                <thead class="bg-gray-50 text-gray-500 text-[11px] uppercase sticky top-0">
                  <tr>
                    <th class="px-5 py-3">No</th>
                    <th class="px-5 py-3">Nama Mahasiswa</th>
                    <th class="px-5 py-3">NIM</th>
                    <th class="px-5 py-3">Tempat Lahir</th>
                    <th class="px-5 py-3">Tanggal Lahir</th>
                    <th class="px-5 py-3">NIK</th>
                    <th class="px-5 py-3">Nama Ibu</th>
                    <th class="px-5 py-3">Nama Bapak</th>
                    <th class="px-5 py-3 text-center">Status</th>
                    <th class="px-5 py-3">Catatan BAAK</th>
                    <th class="px-5 py-3 text-center">Tanggal Daftar</th>
                    <th class="px-5 py-3 text-center w-24">Aksi</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                  <tr v-for="(item, index) in paginatedPendaftaran" :key="item.id" class="hover:bg-gray-50 transition">
                    <td class="px-5 py-3 text-center text-sm">{{ ((currentPagePendaftaran-1)*rowsPerPagePendaftaran) + index + 1 }}</td>
                    <td class="px-5 py-3 font-medium">{{ item.mahasiswa_nama || item.nama_lengkap || '-' }}</td>
                    <td class="px-5 py-3 font-mono text-sm">{{ item.nim || '-' }}</td>
                    <td class="px-5 py-3 text-sm">{{ item.tempat_lahir || '-' }}</td>
                    <td class="px-5 py-3 text-sm">{{ formatTanggalIndonesia(item.tanggal_lahir) }}</td>
                    <td class="px-5 py-3 font-mono text-xs">{{ item.nik || '-' }}</td>
                    <td class="px-5 py-3 text-sm">{{ item.nama_ibu_kandung || '-' }}</td>
                    <td class="px-5 py-3 text-sm">{{ item.nama_bapak_kandung || '-' }}</td>
                    <td class="px-5 py-3 text-center">
                      <span :class="getBadgeClass(item.status)" class="px-2 py-0.5 rounded-full text-[10px] font-bold">
                        {{ getStatusText(item.status) }}
                      </span>
                    </td>
                    <td class="px-5 py-3 text-sm max-w-[200px] truncate" :title="item.catatan_baak">
                      {{ item.catatan_baak || '-' }}
                    </td>
                    <td class="px-5 py-3 text-center text-sm">{{ formatTanggalIndonesia(item.created_at || item.tanggal_daftar) }}</td>
                    <td class="px-5 py-3 text-center">
                      <button 
                        @click="openKomentarPendaftaranModal(item)" 
                        :class="item.status === 'MENUNGGU' ? 'bg-indigo-500 hover:bg-indigo-600' : 'bg-gray-400'"
                        class="text-white px-3 py-1.5 rounded-lg text-xs font-bold transition shadow-sm"
                      >
                        {{ item.status === 'MENUNGGU' ? '💬 Verifikasi' : '📋 Lihat' }}
                      </button>
                    </td>
                  </tr>
                  <tr v-if="paginatedPendaftaran.length === 0">
                    <td colspan="12" class="px-5 py-10 text-center text-gray-400">
                      📭 Tidak ada data pendaftaran yudisium
                      <button @click="manualRefresh" class="ml-2 text-indigo-600 hover:underline">Refresh</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <!-- Pagination -->
            <div class="px-5 py-3 border-t flex flex-wrap gap-3 justify-between items-center bg-gray-50 text-sm">
              <span class="text-gray-500">Menampilkan {{ ((currentPagePendaftaran-1)*rowsPerPagePendaftaran)+1 }} - {{ Math.min(currentPagePendaftaran*rowsPerPagePendaftaran, filteredPendaftaran.length) }} dari {{ filteredPendaftaran.length }} pendaftaran</span>
              <div class="flex gap-2 items-center">
                <button @click="prevPagePendaftaran" :disabled="currentPagePendaftaran===1" class="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-100 transition">Prev</button>
                <span class="text-sm">Halaman {{ currentPagePendaftaran }} / {{ totalPagesPendaftaran }}</span>
                <button @click="nextPagePendaftaran" :disabled="currentPagePendaftaran===totalPagesPendaftaran" class="px-3 py-1 border rounded-lg disabled:opacity-50 hover:bg-gray-100 transition">Next</button>
              </div>
              <select v-model="rowsPerPagePendaftaran" class="border rounded-lg px-2 py-1 text-sm bg-white">
                <option :value="10">10</option>
                <option :value="25">25</option>
                <option :value="50">50</option>
                <option :value="100">100</option>
              </select>
            </div>
          </div>
        </div>

      </section>
    </main>

    <!-- MODAL-MODAL (sama seperti sebelumnya, tetap dipertahankan) -->
    <!-- ... Modal yang sudah ada tetap sama ... -->
    
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

    <!-- MODAL EDIT NILAI -->
    <div v-if="isEditNilaiModalOpen" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl w-full max-w-6xl max-h-[85vh] flex flex-col shadow-2xl">
        <div class="p-5 bg-gradient-to-r from-amber-600 to-amber-700 text-white flex justify-between rounded-t-2xl">
          <div>
            <h3 class="font-bold">✏️ Edit & Revisi Nilai - {{ editNilaiMhsName }}</h3>
            <p class="text-xs text-amber-100">⚠️ Nilai asli mahasiswa tetap tersimpan. BAAK dapat menambah kolom baru dan merevisi nilai.</p>
          </div>
          <button @click="tutupEditNilaiModal" class="text-white hover:text-red-300 transition text-xl">&times;</button>
        </div>
        
        <div class="flex-1 overflow-y-auto p-5">
          <div class="flex border-b mb-4 gap-4">
            <button @click="tabEditMode = 'revisi'" :class="tabEditMode === 'revisi' ? 'border-b-2 border-amber-500 text-amber-600' : 'text-gray-500'" class="px-4 py-2 font-medium text-sm transition">📝 Revisi Nilai</button>
            <button @click="tabEditMode = 'tambah'" :class="tabEditMode === 'tambah' ? 'border-b-2 border-amber-500 text-amber-600' : 'text-gray-500'" class="px-4 py-2 font-medium text-sm transition">➕ Tambah Mata Kuliah Baru</button>
          </div>

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

          <div v-if="tabEditMode === 'tambah'">
            <div class="bg-green-50 p-4 rounded-xl mb-4 border border-green-200">
              <h4 class="font-bold text-green-700 mb-3">➕ Tambah Mata Kuliah Baru ke Transkrip</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div><label class="text-xs font-bold text-gray-600">Kode MK</label><input type="text" v-model="formMKBaru.kode" class="w-full border border-gray-200 rounded-xl p-2 text-sm focus:ring-2 focus:ring-green-400 outline-none"></div>
                <div><label class="text-xs font-bold text-gray-600">SKS</label><input type="number" v-model="formMKBaru.sks" class="w-full border border-gray-200 rounded-xl p-2 text-sm focus:ring-2 focus:ring-green-400 outline-none"></div>
                <div class="md:col-span-2"><label class="text-xs font-bold text-gray-600">Nama Mata Kuliah</label><input type="text" v-model="formMKBaru.nama_mk" class="w-full border border-gray-200 rounded-xl p-2 text-sm focus:ring-2 focus:ring-green-400 outline-none"></div>
                <div><label class="text-xs font-bold text-gray-600">Kategori</label><select v-model="formMKBaru.kategori" class="w-full border border-gray-200 rounded-xl p-2 text-sm bg-white"><option value="Wajib">Wajib</option><option value="Pilihan">Pilihan</option><option value="TA">TA</option></select></div>
                <div><label class="text-xs font-bold text-gray-600">Nilai</label><select v-model="formMKBaru.nilai" class="w-full border border-gray-200 rounded-xl p-2 text-sm bg-white"><option value="">-- Pilih --</option><option value="A">A</option><option value="A-">A-</option><option value="B+">B+</option><option value="B">B</option><option value="B-">B-</option><option value="C+">C+</option><option value="C">C</option><option value="D">D</option><option value="E">E</option></select></div>
              </div>
              <button @click="tambahMataKuliahKeNilai" class="mt-3 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-xl text-sm font-bold transition shadow-md">+ Tambahkan</button>
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

    <!-- MODAL LIHAT NILAI -->
    <div v-if="isModalNilaiOpen" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl w-full max-w-5xl max-h-[80vh] flex flex-col shadow-2xl">
        <div class="p-5 bg-gradient-to-r from-indigo-700 to-indigo-800 text-white flex justify-between rounded-t-2xl">
          <div><h3 class="font-bold">📊 Detail Transkrip Nilai - {{ selectedMhsName }}</h3><p class="text-xs text-indigo-200">NIM: {{ selectedMhsNim }}</p></div>
          <button @click="tutupModalNilai" class="text-white hover:text-red-300 transition text-xl">&times;</button>
        </div>
        <div class="flex-1 overflow-y-auto p-5">
          <table class="w-full text-sm border-collapse">
            <thead class="bg-gray-100 sticky top-0">
              <tr>
                <th class="p-3 text-left">Kode</th>
                <th class="p-3 text-left">Mata Kuliah</th>
                <th class="p-3 text-center">SKS</th>
                <th class="p-3 text-center bg-gray-200">Nilai Asli</th>
                <th class="p-3 text-center bg-amber-100">Nilai Revisi</th>
                <th class="p-3 text-center bg-green-100">Nilai Akhir</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in selectedDataNilaiWithRevisi" :key="item.kode_mk" class="border-b">
                <td class="p-3">{{ item.kode_mk }}</td>
                <td class="p-3">{{ item.nama_mk }}</td>
                <td class="p-3 text-center">{{ item.sks }}</td>
                <td class="p-3 text-center bg-gray-50 font-bold text-gray-700">{{ item.nilai_asli || '-' }}</td>
                <td class="p-3 text-center bg-amber-50 font-bold text-amber-700">{{ item.nilai_revisi || '-' }}</td>
                <td class="p-3 text-center bg-green-50 font-bold text-green-700">{{ item.nilai_revisi || item.nilai_asli || '-' }}</td>
              </tr>
            </tbody>
          </table>
          <div v-if="selectedDataNilaiWithRevisi.filter(i => i.nilai_revisi).length > 0" class="mt-4 p-3 bg-amber-50 rounded-xl border border-amber-200">
            <p class="font-bold text-amber-700">📝 Ringkasan Perubahan:</p>
            <ul class="text-sm"><li v-for="item in selectedDataNilaiWithRevisi.filter(i => i.nilai_revisi)" :key="item.kode_mk">• {{ item.nama_mk }}: {{ item.nilai_asli }} → {{ item.nilai_revisi }}</li></ul>
          </div>
        </div>
        <div class="p-4 border-t flex justify-end"><button @click="tutupModalNilai" class="px-5 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-xl transition">Tutup</button></div>
      </div>
    </div>

    <!-- MODAL TOLAK PENGAJUAN -->
    <div v-if="isTolakModalOpen" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl w-full max-w-md shadow-2xl">
        <div class="p-5 border-b bg-red-50 flex justify-between items-center">
          <h3 class="font-bold text-red-800">❌ Tolak Pengajuan</h3>
          <button @click="isTolakModalOpen=false" class="text-gray-400 hover:text-red-500 transition text-xl">&times;</button>
        </div>
        <div class="p-5">
          <textarea v-model="catatanTolak" placeholder="Alasan penolakan..." class="w-full border border-gray-200 rounded-xl p-3 h-28 focus:ring-2 focus:ring-red-400 outline-none"></textarea>
        </div>
        <div class="p-4 border-t bg-gray-50 flex justify-end gap-2 rounded-b-2xl">
          <button @click="isTolakModalOpen=false" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-xl text-sm font-medium transition">Batal</button>
          <button @click="confirmTolak" class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-xl text-sm font-bold transition shadow-md">Tolak</button>
        </div>
      </div>
    </div>

    <!-- MODAL RIWAYAT MAHASISWA -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl w-full max-w-3xl max-h-[80vh] flex flex-col shadow-2xl">
        <div class="p-5 border-b bg-indigo-50 flex justify-between items-center">
          <div><h3 class="font-bold text-indigo-900">Riwayat Transkrip</h3><p class="text-xs text-gray-600">{{ selectedMahasiswa?.full_name }}</p></div>
          <button @click="closeModal" class="text-gray-400 hover:text-red-500 transition text-xl">&times;</button>
        </div>
        <div class="overflow-y-auto p-5">
          <table class="w-full text-sm border-collapse">
            <thead class="bg-gray-100">
              <tr><th class="p-2 text-left">No</th><th class="p-2 text-left">Berkas</th><th class="p-2 text-left">Status</th><th class="p-2 text-left">Tanggal</th></tr>
            </thead>
            <tbody>
              <tr v-for="(item,idx) in riwayatMahasiswa" :key="idx" class="border-b">
                <td class="p-2">{{ idx+1 }}</td>
                <td class="p-2"><a v-if="item.file_transkrip" :href="getFileUrl(item)" target="_blank" class="text-indigo-600 hover:underline">📄 PDF</a><span v-else class="text-gray-400">-</span></td>
                <td class="p-2"><span :class="getBadgeClass(item.status)">{{ getStatusText(item.status) }}</span></td>
                <td class="p-2">{{ formatTanggal(item.validated_at) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- MODAL KOMENTAR PENDAFTARAN YUDISIUM -->
    <div v-if="isKomentarPendaftaranModalOpen" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4 backdrop-blur-sm">
      <div class="bg-white rounded-2xl w-full max-w-md shadow-2xl">
        <div class="p-5 border-b" :class="komentarPendaftaranData?.status === 'MENUNGGU' ? 'bg-orange-50' : 'bg-green-50'">
          <div class="flex justify-between items-center">
            <h3 class="font-bold" :class="komentarPendaftaranData?.status === 'MENUNGGU' ? 'text-orange-800' : 'text-green-800'">
              {{ komentarPendaftaranData?.status === 'MENUNGGU' ? '💬 Verifikasi Pendaftaran' : '📋 Detail Komentar' }}
            </h3>
            <button @click="closeKomentarModal" class="text-gray-400 hover:text-red-500 transition text-xl">&times;</button>
          </div>
        </div>
        <div class="p-5">
          <p class="text-sm mb-2">Mahasiswa: <strong>{{ komentarPendaftaranData?.mahasiswa_nama || komentarPendaftaranData?.nama_lengkap }}</strong></p>
          <p class="text-xs text-gray-500 mb-3">NIM: <strong>{{ komentarPendaftaranData?.nim }}</strong></p>
          
          <div class="mb-4">
            <span :class="komentarPendaftaranData?.status === 'MENUNGGU' ? 'bg-orange-100 text-orange-700' : 'bg-green-100 text-green-700'" 
                  class="px-2 py-0.5 rounded-full text-[10px] font-bold">
              {{ komentarPendaftaranData?.status === 'MENUNGGU' ? '⏳ Menunggu Verifikasi' : '✅ Telah Diverifikasi' }}
            </span>
          </div>
          
          <label class="block text-sm font-semibold text-gray-700 mb-1">
            {{ komentarPendaftaranData?.status === 'MENUNGGU' ? 'Catatan Verifikasi' : 'Catatan BAAK' }}
          </label>
          
          <textarea 
            v-model="catatanKomentarPendaftaran" 
            placeholder="Tulis catatan verifikasi untuk mahasiswa..." 
            class="w-full border border-gray-200 rounded-xl p-3 h-28 outline-none focus:ring-2 focus:ring-indigo-400" 
            :disabled="isLoadingKomentar || komentarPendaftaranData?.status !== 'MENUNGGU'"
          ></textarea>
          
          <div v-if="komentarPendaftaranData?.status !== 'MENUNGGU' && komentarPendaftaranData?.catatan_baak" class="mt-3 p-3 bg-gray-50 rounded-xl">
            <p class="text-xs font-bold text-gray-600 mb-1">📝 Catatan Sebelumnya:</p>
            <p class="text-sm text-gray-700">{{ komentarPendaftaranData?.catatan_baak }}</p>
          </div>
        </div>
        <div class="p-4 border-t bg-gray-50 flex justify-end gap-2 rounded-b-2xl">
          <button @click="closeKomentarModal" class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-xl text-sm font-medium transition">Tutup</button>
          <button 
            v-if="komentarPendaftaranData?.status === 'MENUNGGU'"
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

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import * as XLSX from 'xlsx'
import api from '../api'

const router = useRouter()

// ========== DATA STATE ==========
const user = ref({ username: '', full_name: '', role: '' })
const activeMenu = ref('matakuliah')
const semuaRiwayatBerkas = ref([])
const antrian = ref([])
const daftarMahasiswa = ref([])
const daftarMataKuliahData = ref([])

// ========== PAGINATION ==========
const searchMatakuliah = ref('')
const filterJurusan = ref('')
const filterKategori = ref('')
const filterKelompok = ref('')
const currentPageMatakuliah = ref(1)
const rowsPerPageMatakuliah = ref(10)

const searchAntrian = ref('')
const currentPageAntrian = ref(1)
const rowsPerPageAntrian = ref(10)

const searchRiwayat = ref('')
const filterStatusRiwayat = ref('')
const currentPageRiwayat = ref(1)
const rowsPerPageRiwayat = ref(10)

const searchMonitoring = ref('')
const filterStatusTranskrip = ref('')
const currentPageMonitoring = ref(1)
const rowsPerPageMonitoring = ref(10)

// ========== MODAL STATE ==========
const isModalFormMkOpen = ref(false)
const isEditMode = ref(false)
const formMk = ref({ kode: '', nama: '', sks: 2, jurusan: 'Semua Jurusan', kategori: 'Wajib', kelompok: '' })

const isEditNilaiModalOpen = ref(false)
const editNilaiId = ref(null)
const editNilaiMhsName = ref('')
const editNilaiData = ref([])
const mkBaruDitambahkan = ref([])
const tabEditMode = ref('revisi')
const formMKBaru = ref({ kode: '', nama_mk: '', sks: 2, kategori: 'Wajib', nilai: '' })

const isModalNilaiOpen = ref(false)
const selectedDataNilaiWithRevisi = ref([])
const selectedMhsName = ref('')
const selectedMhsNim = ref('')

const isTolakModalOpen = ref(false)
const tolakMhsId = ref(null)
const catatanTolak = ref('')

const isModalOpen = ref(false)
const selectedMahasiswa = ref(null)
const riwayatMahasiswa = ref([])

// ========== PENDAFTARAN YUDISIUM ==========
const daftarPendaftaranYudisium = ref([])
const searchPendaftaran = ref('')
const currentPagePendaftaran = ref(1)
const rowsPerPagePendaftaran = ref(10)

// ========== KOMENTAR ==========
const isKomentarPendaftaranModalOpen = ref(false)
const komentarPendaftaranData = ref(null)
const catatanKomentarPendaftaran = ref('')
const isLoadingKomentar = ref(false)

// ========== HELPER FUNCTIONS ==========
const getStatus = (item) => {
  if (!item) return 'MENUNGGU'
  let status = item.status || item.status_transkrip || 'MENUNGGU'
  if (status === 'DISETUJU') return 'DISETUJUI'
  if (status === 'SETUJU') return 'DISETUJUI'
  if (status === 'TOLAK') return 'DITOLAK'
  return status
}

const getStatusText = (status) => {
  const statusMap = {
    'DISETUJUI': '✅ Disetujui',
    'DITOLAK': '❌ Ditolak',
    'MENUNGGU': '⏳ Menunggu',
    'BELUM': '⚪ Belum',
    'PROSES': '🔄 Proses'
  }
  return statusMap[status] || status || '⚪ Belum'
}

const getBadgeClass = (status) => {
  const s = getStatus({ status })
  if (s === 'DISETUJUI') return 'bg-green-100 text-green-700 px-2 py-0.5 rounded-full text-[10px] font-bold'
  if (s === 'DITOLAK') return 'bg-red-100 text-red-700 px-2 py-0.5 rounded-full text-[10px] font-bold'
  if (s === 'MENUNGGU') return 'bg-orange-100 text-orange-700 px-2 py-0.5 rounded-full text-[10px] font-bold'
  return 'bg-gray-100 text-gray-500 px-2 py-0.5 rounded-full text-[10px] font-bold'
}

const getFileUrl = (item) => {
  if (!item) return null
  let fileUrl = item.file_transkrip || item.berkas || item.file || item.file_url
  if (!fileUrl) return null
  if (fileUrl.startsWith('http')) return fileUrl
  if (fileUrl.startsWith('/media/') || fileUrl.startsWith('media/')) {
    const cleanUrl = fileUrl.startsWith('/') ? fileUrl : `/${fileUrl}`
    return `http://127.0.0.1:8000${cleanUrl}`
  }
  return `http://127.0.0.1:8000/media/${fileUrl}`
}

const formatTanggal = (dateString) => {
  if (!dateString) return '-'
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return '-'
    return date.toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
  } catch {
    return '-'
  }
}

// Format tanggal untuk Indonesia (tanpa jam)
const formatTanggalIndonesia = (dateString) => {
  if (!dateString) return '-'
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return '-'
    return date.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' })
  } catch {
    return '-'
  }
}

// ========== FUNGSI EXPORT EXCEL UNTUK PENDAFTARAN YUDISIUM ==========
const exportPendaftaranToExcel = () => {
  try {
    // Ambil semua data pendaftaran (tanpa filter pagination)
    const dataToExport = filteredPendaftaran.value
    
    if (dataToExport.length === 0) {
      alert('Tidak ada data untuk diekspor!')
      return
    }
    
    // Mapping data ke format Excel yang rapi
    const excelData = dataToExport.map((item, index) => ({
      'No': index + 1,
      'Nama Mahasiswa': item.mahasiswa_nama || item.nama_lengkap || '-',
      'NIM': item.nim || '-',
      'Tempat Lahir': item.tempat_lahir || '-',
      'Tanggal Lahir': formatTanggalIndonesia(item.tanggal_lahir),
      'NIK': item.nik || '-',
      'Nama Ibu Kandung': item.nama_ibu_kandung || '-',
      'Nama Bapak Kandung': item.nama_bapak_kandung || '-',
      'Status': getStatusText(item.status),
      'Catatan BAAK': item.catatan_baak || '-',
      'Tanggal Pendaftaran': formatTanggalIndonesia(item.created_at || item.tanggal_daftar),
   
    }))
    
    // Buat worksheet
    const ws = XLSX.utils.json_to_sheet(excelData)
    
    // Atur lebar kolom
    const colWidths = [
      { wch: 5 },   // No
      { wch: 25 },  // Nama Mahasiswa
      { wch: 15 },  // NIM
      { wch: 15 },  // Tempat Lahir
      { wch: 15 },  // Tanggal Lahir
      { wch: 18 },  // NIK
      { wch: 20 },  // Nama Ibu
      { wch: 20 },  // Nama Bapak
      { wch: 12 },  // Status
      { wch: 30 },  // Catatan BAAK
      { wch: 15 },  // Tanggal Pendaftaran
     
    ]
    ws['!cols'] = colWidths
    
    // Buat workbook
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, 'Pendaftaran_Yudisium')
    
    // Generate nama file dengan tanggal
    const today = new Date()
    const dateStr = `${today.getFullYear()}-${(today.getMonth()+1).toString().padStart(2,'0')}-${today.getDate().toString().padStart(2,'0')}`
    const fileName = `Pendaftaran_Yudisium_${dateStr}.xlsx`
    
    // Download file
    XLSX.writeFile(wb, fileName)
    
    alert(`✅ Berhasil mengeksport ${dataToExport.length} data pendaftaran yudisium ke file Excel!`)
    
  } catch (error) {
    console.error('Error export Excel:', error)
    alert('Gagal mengeksport data: ' + error.message)
  }
}

// Format tanggal untuk Excel
const formatTanggalExcel = (dateString) => {
  if (!dateString) return '-'
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return '-'
    return date.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' })
  } catch {
    return '-'
  }
}

const resetPendaftaranFilter = () => {
  searchPendaftaran.value = ''
  currentPagePendaftaran.value = 1
}

// ========== COMPUTED ==========
const headerTitle = computed(() => {
  if (activeMenu.value === 'matakuliah') return 'Kelola Daftar Mata Kuliah'
  if (activeMenu.value === 'antrian') return 'Verifikasi Transkrip Nilai'
  if (activeMenu.value === 'riwayat') return 'Riwayat Validasi Transkrip'
  if (activeMenu.value === 'pendaftaran') return 'Verifikasi Pendaftaran Yudisium'
  return 'Monitoring Seluruh Mahasiswa'
})

// Statistik untuk riwayat
const totalDataDenganBerkas = computed(() => {
  return semuaRiwayatBerkas.value.filter(item => 
    item.file_transkrip || item.berkas || item.file || item.file_url
  ).length
})

const totalDisetujui = computed(() => {
  return semuaRiwayatBerkas.value.filter(item => getStatus(item) === 'DISETUJUI').length
})

const totalDitolak = computed(() => {
  return semuaRiwayatBerkas.value.filter(item => getStatus(item) === 'DITOLAK').length
})

const totalMenunggu = computed(() => {
  return semuaRiwayatBerkas.value.filter(item => getStatus(item) === 'MENUNGGU').length
})

// Filter untuk mata kuliah
const filteredMataKuliah = computed(() => {
  return daftarMataKuliahData.value.filter(mk => {
    const matchSearch = !searchMatakuliah.value || mk.kode.toLowerCase().includes(searchMatakuliah.value.toLowerCase()) || mk.nama.toLowerCase().includes(searchMatakuliah.value.toLowerCase())
    const matchJurusan = !filterJurusan.value || mk.jurusan === 'Semua Jurusan' || mk.jurusan === filterJurusan.value
    const matchKategori = !filterKategori.value || mk.kategori === filterKategori.value
    const matchKelompok = !filterKelompok.value || (mk.kelompok && mk.kelompok.toLowerCase().includes(filterKelompok.value.toLowerCase()))
    return matchSearch && matchJurusan && matchKategori && matchKelompok
  })
})

const totalPagesMatakuliah = computed(() => Math.ceil(filteredMataKuliah.value.length / rowsPerPageMatakuliah.value))
const paginatedMatakuliah = computed(() => {
  const start = (currentPageMatakuliah.value - 1) * rowsPerPageMatakuliah.value
  return filteredMataKuliah.value.slice(start, start + rowsPerPageMatakuliah.value)
})

// Filter untuk antrian
const filteredAntrian = computed(() => antrian.value.filter(item => {
  const nama = item.full_name || item.mahasiswa_nama || ''
  const nim = item.nim || item.mahasiswa_nim || ''
  return !searchAntrian.value || nama.toLowerCase().includes(searchAntrian.value.toLowerCase()) || nim.toLowerCase().includes(searchAntrian.value.toLowerCase())
}))

const totalPagesAntrian = computed(() => Math.ceil(filteredAntrian.value.length / rowsPerPageAntrian.value))
const paginatedAntrian = computed(() => {
  const start = (currentPageAntrian.value - 1) * rowsPerPageAntrian.value
  return filteredAntrian.value.slice(start, start + rowsPerPageAntrian.value)
})

// Filter untuk riwayat
const filteredRiwayat = computed(() => {
  return semuaRiwayatBerkas.value.filter(item => {
    const status = getStatus(item)
    const matchStatus = !filterStatusRiwayat.value || status === filterStatusRiwayat.value
    const nama = item.full_name || item.mahasiswa_nama || ''
    const nim = item.nim || item.mahasiswa_nim || ''
    const matchSearch = !searchRiwayat.value || 
      nama.toLowerCase().includes(searchRiwayat.value.toLowerCase()) || 
      nim.toLowerCase().includes(searchRiwayat.value.toLowerCase())
    return matchStatus && matchSearch
  })
})

const totalPagesRiwayat = computed(() => Math.ceil(filteredRiwayat.value.length / rowsPerPageRiwayat.value))
const paginatedRiwayat = computed(() => {
  const start = (currentPageRiwayat.value - 1) * rowsPerPageRiwayat.value
  return filteredRiwayat.value.slice(start, start + rowsPerPageRiwayat.value)
})

// Filter untuk monitoring
const filteredMonitoring = computed(() => daftarMahasiswa.value.filter(mhs => {
  const matchSearch = !searchMonitoring.value || (mhs.full_name || '').toLowerCase().includes(searchMonitoring.value.toLowerCase()) || (mhs.nim || '').toLowerCase().includes(searchMonitoring.value.toLowerCase())
  const matchStatus = !filterStatusTranskrip.value || getStatus(mhs) === filterStatusTranskrip.value
  return matchSearch && matchStatus
}))

const totalPagesMonitoring = computed(() => Math.ceil(filteredMonitoring.value.length / rowsPerPageMonitoring.value))
const paginatedMonitoring = computed(() => {
  const start = (currentPageMonitoring.value - 1) * rowsPerPageMonitoring.value
  return filteredMonitoring.value.slice(start, start + rowsPerPageMonitoring.value)
})

// Filter untuk pendaftaran
const filteredPendaftaran = computed(() => {
  return daftarPendaftaranYudisium.value.filter(item => {
    const matchSearch = !searchPendaftaran.value || 
      (item.mahasiswa_nama || item.nama_lengkap || '').toLowerCase().includes(searchPendaftaran.value.toLowerCase()) ||
      (item.nim || '').toLowerCase().includes(searchPendaftaran.value.toLowerCase())
    return matchSearch
  })
})

const pendaftaranMenungguCount = computed(() => filteredPendaftaran.value.filter(i => i.status === 'MENUNGGU').length)
const totalPagesPendaftaran = computed(() => Math.ceil(filteredPendaftaran.value.length / rowsPerPagePendaftaran.value))
const paginatedPendaftaran = computed(() => {
  const start = (currentPagePendaftaran.value - 1) * rowsPerPagePendaftaran.value
  return filteredPendaftaran.value.slice(start, start + rowsPerPagePendaftaran.value)
})

// ========== FUNCTIONS ==========
const resetPagination = () => {
  currentPageMatakuliah.value = 1
  currentPageAntrian.value = 1
  currentPageRiwayat.value = 1
  currentPageMonitoring.value = 1
  currentPagePendaftaran.value = 1
}

const resetRiwayatFilter = () => {
  searchRiwayat.value = ''
  filterStatusRiwayat.value = ''
  currentPageRiwayat.value = 1
}

const prevPageMatakuliah = () => { if (currentPageMatakuliah.value > 1) currentPageMatakuliah.value-- }
const nextPageMatakuliah = () => { if (currentPageMatakuliah.value < totalPagesMatakuliah.value) currentPageMatakuliah.value++ }
const prevPageAntrian = () => { if (currentPageAntrian.value > 1) currentPageAntrian.value-- }
const nextPageAntrian = () => { if (currentPageAntrian.value < totalPagesAntrian.value) currentPageAntrian.value++ }
const prevPageRiwayat = () => { if (currentPageRiwayat.value > 1) currentPageRiwayat.value-- }
const nextPageRiwayat = () => { if (currentPageRiwayat.value < totalPagesRiwayat.value) currentPageRiwayat.value++ }
const prevPageMonitoring = () => { if (currentPageMonitoring.value > 1) currentPageMonitoring.value-- }
const nextPageMonitoring = () => { if (currentPageMonitoring.value < totalPagesMonitoring.value) currentPageMonitoring.value++ }
const prevPagePendaftaran = () => { if (currentPagePendaftaran.value > 1) currentPagePendaftaran.value-- }
const nextPagePendaftaran = () => { if (currentPagePendaftaran.value < totalPagesPendaftaran.value) currentPagePendaftaran.value++ }

// ========== MATA KULIAH CRUD ==========
const bukaModalFormMk = (mk = null) => {
  if (mk) {
    isEditMode.value = true
    formMk.value = { ...mk }
  } else {
    isEditMode.value = false
    formMk.value = { kode: '', nama: '', sks: 2, jurusan: 'Semua Jurusan', kategori: 'Wajib', kelompok: '' }
  }
  isModalFormMkOpen.value = true
}

const simpanMataKuliah = async () => {
  try {
    if (isEditMode.value) {
      await api.put(`matakuliah/${formMk.value.kode}/`, formMk.value)
    } else {
      await api.post('matakuliah/', formMk.value)
    }
    alert('Mata kuliah berhasil disimpan')
    isModalFormMkOpen.value = false
    await fetchData()
  } catch (err) {
    alert('Gagal menyimpan mata kuliah')
  }
}

const hapusMataKuliah = async (kode) => {
  if (confirm('Hapus mata kuliah ini?')) {
    try {
      await api.delete(`matakuliah/${kode}/`)
      alert('Mata kuliah dihapus')
      await fetchData()
    } catch (err) {
      alert('Gagal menghapus')
    }
  }
}

// ========== EDIT NILAI ==========
const openEditNilaiModal = (id, nama, dataNilai) => {
  editNilaiId.value = id
  editNilaiMhsName.value = nama
  const dataArray = Array.isArray(dataNilai) ? dataNilai : []
  editNilaiData.value = dataArray.map(item => ({
    kode_mk: item.kode_mk || item.kode,
    nama_mk: item.nama_mk || item.nama,
    sks: item.sks,
    nilai_asli: item.nilai || item.huruf || '',
    nilai_revisi: item.nilai_revisi || ''
  }))
  mkBaruDitambahkan.value = []
  tabEditMode.value = 'revisi'
  isEditNilaiModalOpen.value = true
}

const tutupEditNilaiModal = () => {
  isEditNilaiModalOpen.value = false
  editNilaiId.value = null
  editNilaiMhsName.value = ''
  editNilaiData.value = []
  mkBaruDitambahkan.value = []
}

const tambahMataKuliahKeNilai = () => {
  if (!formMKBaru.value.kode || !formMKBaru.value.nama_mk) {
    alert('Kode MK dan Nama Mata Kuliah wajib diisi!')
    return
  }
  mkBaruDitambahkan.value.push({
    kode_mk: formMKBaru.value.kode,
    nama_mk: formMKBaru.value.nama_mk,
    sks: formMKBaru.value.sks,
    nilai: formMKBaru.value.nilai || '',
    nilai_revisi: formMKBaru.value.nilai || ''
  })
  formMKBaru.value = { kode: '', nama_mk: '', sks: 2, kategori: 'Wajib', nilai: '' }
}

const hapusMKBaru = (index) => {
  if (confirm('Hapus?')) mkBaruDitambahkan.value.splice(index, 1)
}

const simpanPerubahanNilai = async () => {
  try {
    const originalResponse = await api.get(`transkrip-nilai/${editNilaiId.value}/`)
    const originalData = originalResponse.data
    const savedDataNilai = []
    
    for (const item of editNilaiData.value) {
      savedDataNilai.push({
        kode_mk: item.kode_mk,
        nama_mk: item.nama_mk,
        sks: parseInt(item.sks) || 2,
        nilai: item.nilai_asli,
        nilai_revisi: item.nilai_revisi || ''
      })
    }
    
    for (const item of mkBaruDitambahkan.value) {
      savedDataNilai.push({
        kode_mk: item.kode_mk,
        nama_mk: item.nama_mk,
        sks: parseInt(item.sks) || 2,
        nilai: item.nilai || '',
        nilai_revisi: item.nilai || ''
      })
    }
    
    await api.put(`transkrip-nilai/${editNilaiId.value}/`, {
      pendaftaran: originalData.pendaftaran,
      data_nilai: savedDataNilai,
      status: 'MENUNGGU'
    })
    
    alert('Perubahan nilai berhasil disimpan!')
    tutupEditNilaiModal()
    await fetchData()
  } catch (err) {
    console.error(err)
    alert('Gagal menyimpan: ' + JSON.stringify(err.response?.data))
  }
}

// ========== LIHAT NILAI ==========
const bukaModalNilai = (data, nama, nim) => {
  const dataArray = Array.isArray(data) ? data : []
  selectedDataNilaiWithRevisi.value = dataArray.map(item => ({
    kode_mk: item.kode_mk || item.kode,
    nama_mk: item.nama_mk || item.nama,
    sks: item.sks,
    nilai_asli: item.nilai || item.huruf || '',
    nilai_revisi: item.nilai_revisi || ''
  }))
  selectedMhsName.value = nama
  selectedMhsNim.value = nim
  isModalNilaiOpen.value = true
}

const tutupModalNilai = () => {
  isModalNilaiOpen.value = false
  selectedDataNilaiWithRevisi.value = []
}

// ========== VERIFIKASI TRANSKRIP ==========
const openTolakTranskripModal = (id, nama) => {
  tolakMhsId.value = id
  catatanTolak.value = ''
  isTolakModalOpen.value = true
}

const confirmTolak = async () => {
  if (!catatanTolak.value.trim()) {
    alert('Alasan penolakan wajib diisi!')
    return
  }
  await verifikasiTranskrip(tolakMhsId.value, 'DITOLAK', catatanTolak.value)
  isTolakModalOpen.value = false
}

const verifikasiTranskrip = async (id, status, catatan = null) => {
  try {
    // Gunakan endpoint yang baru
    const response = await api.patch(`transkrip-nilai/${id}/verifikasi/`, {
      status: status,
      catatan_baak: status === 'DISETUJUI' ? 'Data transkrip valid dan sesuai' : catatan,
    })
    
    console.log('Verifikasi berhasil:', response.data)
    alert(`Berhasil ${status === 'DISETUJUI' ? 'menyetujui' : 'menolak'} transkrip`)
    await fetchData()
  } catch (err) {
    console.error('Error:', err)
    alert('Gagal melakukan verifikasi: ' + (err.response?.data?.error || err.message))
  }
}

// ========== PENDAFTARAN YUDISIUM ==========
const fetchPendaftaranYudisium = async () => {
  try {
    const res = await api.get('pendaftaran-yudisium/')
    daftarPendaftaranYudisium.value = res.data
    console.log('Data pendaftaran yudisium:', daftarPendaftaranYudisium.value)
  } catch (err) {
    console.error('Gagal fetch pendaftaran yudisium:', err)
  }
}

const refreshPendaftaranData = async () => {
  console.log('🔄 Memulai refresh data pendaftaran...')
  await fetchPendaftaranYudisium()
  await fetchData()
  console.log('✅ Refresh selesai. Menunggu:', pendaftaranMenungguCount.value)
}

const manualRefresh = async () => {
  await refreshPendaftaranData()
  alert('Data berhasil di-refresh!')
}

// ========== RIWAYAT VALIDASI ==========
const refreshRiwayatData = async () => {
  try {
    console.log('🔄 Mengambil data riwayat validasi...')
    const resBerkas = await api.get('baak/berkas-masuk/')
    
    semuaRiwayatBerkas.value = resBerkas.data.map(item => ({
      ...item,
      file_transkrip: item.file_transkrip || item.berkas || item.file,
      status: item.status || item.status_transkrip || 'MENUNGGU',
      full_name: item.full_name || item.mahasiswa_nama,
      nim: item.nim || item.mahasiswa_nim
    }))
    
    console.log('✅ Data riwayat berhasil di-refresh:', semuaRiwayatBerkas.value.length, 'data')
    
    antrian.value = semuaRiwayatBerkas.value.filter(i => getStatus(i) === 'MENUNGGU')
    currentPageRiwayat.value = 1
    
  } catch (err) {
    console.error('❌ Gagal refresh data riwayat:', err)
    alert('Gagal mengambil data riwayat.')
  }
}

// ========== MONITORING ==========
const lihatRiwayat = (mhs) => {
  selectedMahasiswa.value = mhs
  riwayatMahasiswa.value = semuaRiwayatBerkas.value.filter(item => 
    (item.nim === mhs.nim) || (item.mahasiswa_nim === mhs.nim)
  )
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
  selectedMahasiswa.value = null
  riwayatMahasiswa.value = []
}

// ========== KOMENTAR PENDAFTARAN ==========
const openKomentarPendaftaranModal = (item) => {
  komentarPendaftaranData.value = item
  
  if (item.status === 'MENUNGGU') {
    catatanKomentarPendaftaran.value = 'Pendaftaran berhasil, silakan lanjutkan ke proses yudisium.'
  } else {
    catatanKomentarPendaftaran.value = item.catatan_baak || ''
  }
  
  isKomentarPendaftaranModalOpen.value = true
}

const closeKomentarModal = () => {
  isKomentarPendaftaranModalOpen.value = false
  komentarPendaftaranData.value = null
  catatanKomentarPendaftaran.value = ''
}

const kirimKomentarPendaftaran = async () => {
  if (!catatanKomentarPendaftaran.value.trim()) {
    alert('Komentar wajib diisi!')
    return
  }
  
  isLoadingKomentar.value = true
  
  try {
    console.log('📤 Mengirim verifikasi ke ID:', komentarPendaftaranData.value.id)
    console.log('📤 Data:', {
      catatan_baak: catatanKomentarPendaftaran.value,
      status: 'DISETUJUI'
    })
    
    const response = await api.patch(`pendaftaran-yudisium/${komentarPendaftaranData.value.id}/verifikasi/`, {
      catatan_baak: catatanKomentarPendaftaran.value,
      status: 'DISETUJUI'
    })
    
    console.log('✅ Response:', response.data)
    alert('✅ Pendaftaran berhasil diverifikasi!')
    closeKomentarModal()
    await refreshPendaftaranData()
    
  } catch (err) {
    console.error('❌ Error:', err)
    alert('Gagal: ' + (err.response?.data?.error || err.message))
  } finally {
    isLoadingKomentar.value = false
  }
}
// ========== FETCH DATA ==========
const fetchData = async () => {
  try {
    const [resUser, resMk, resBerkas, resDaftar] = await Promise.all([
      api.get('users/me/'),
      api.get('matakuliah/').catch(() => ({ data: [] })),
      api.get('baak/berkas-masuk/').catch(() => ({ data: [] })),
      api.get('baak/daftar-mahasiswa/').catch(() => ({ data: [] }))
    ])
    
    user.value = resUser.data
    daftarMataKuliahData.value = resMk.data
    
    semuaRiwayatBerkas.value = resBerkas.data.map(item => ({
      ...item,
      file_transkrip: item.file_transkrip || item.berkas || item.file,
      status: item.status || item.status_transkrip || 'MENUNGGU',
      full_name: item.full_name || item.mahasiswa_nama,
      nim: item.nim || item.mahasiswa_nim
    }))
    
    console.log('📊 Data berkas dari API:', semuaRiwayatBerkas.value.length, 'data')
    
    antrian.value = semuaRiwayatBerkas.value.filter(i => getStatus(i) === 'MENUNGGU')
    daftarMahasiswa.value = resDaftar.data
    
    resetPagination()
  } catch (err) {
    console.error('Error fetch data:', err)
    if (err.response?.status === 401) router.push('/login')
  }
}

const handleLogout = () => {
  localStorage.clear()
  router.push('/login')
}

// ========== WATCHERS ==========
watch([searchMatakuliah, filterJurusan, filterKategori, filterKelompok], () => currentPageMatakuliah.value = 1)
watch(searchAntrian, () => currentPageAntrian.value = 1)
watch([searchRiwayat, filterStatusRiwayat], () => currentPageRiwayat.value = 1)
watch([searchMonitoring, filterStatusTranskrip], () => currentPageMonitoring.value = 1)
watch(searchPendaftaran, () => currentPagePendaftaran.value = 1)

// ========== MOUNTED ==========
onMounted(async () => {
  await fetchData()
  await fetchPendaftaranYudisium()
})
</script>