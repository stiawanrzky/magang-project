<template>
  <div class="flex h-screen bg-gray-50 overflow-x-hidden">
    <!-- SIDEBAR -->
    <aside class="w-64 bg-slate-900 text-white hidden md:flex flex-col shadow-xl">
      <div class="p-6 text-xl font-bold border-b border-slate-800 flex items-center gap-2">
        <span class="p-2 bg-indigo-600 rounded-lg text-white text-sm">🏛️</span>
        Sistem Akademik
      </div>
      <nav class="flex-1 p-4 space-y-1">
        <p class="text-xs text-slate-500 font-bold px-4 mb-2 uppercase tracking-widest">Manajemen</p>
        
        <button @click="activeTab = 'antrian'; resetPagination()" 
                :class="['w-full text-left flex items-center space-x-3 py-3 px-4 rounded-lg transition-all', 
                         activeTab === 'antrian' ? 'bg-slate-800 shadow-inner text-white' : 'hover:bg-slate-800 text-slate-400']">
          <span>📋 Antrian Verifikasi</span>
          <span v-if="antrianCount > 0" class="ml-auto bg-red-500 text-white text-[10px] rounded-full px-2 py-0.5">{{ antrianCount }}</span>
        </button>
        
        <button @click="activeTab = 'riwayat'; resetPagination()" 
                :class="['w-full text-left flex items-center space-x-3 py-3 px-4 rounded-lg transition-all', 
                         activeTab === 'riwayat' ? 'bg-slate-800 shadow-inner text-white' : 'hover:bg-slate-800 text-slate-400']">
          <span>🗂️ Riwayat Mahasiswa</span>
        </button>

        <!-- TOMBOL PERIODE YUDISIUM (BARU) -->
        <button @click="activeTab = 'periode'; resetPagination(); fetchPeriode()" 
                :class="['w-full text-left flex items-center space-x-3 py-3 px-4 rounded-lg transition-all', 
                         activeTab === 'periode' ? 'bg-slate-800 shadow-inner text-white' : 'hover:bg-slate-800 text-slate-400']">
          <span>📅 Periode Yudisium</span>
        </button>
      </nav>
      <div class="p-4 border-t border-slate-800">
        <button @click="handleLogout" class="w-full bg-red-500/10 text-red-500 hover:bg-red-500 hover:text-white py-2.5 rounded-lg text-sm font-bold transition-all">
          Keluar Sistem
        </button>
      </div>
    </aside>

    <!-- MAIN CONTENT -->
   <main class="flex-1 flex flex-col overflow-hidden relative max-w-full">
      <header class="bg-white border-b border-gray-200 py-4 px-8 flex justify-between items-center z-10">
        <div>
          <h1 class="text-lg font-bold text-gray-800">Panel Kontrol Akademik</h1>
          <p class="text-xs text-gray-500">Petugas: {{ user.full_name }}</p>
        </div>
        <div class="flex items-center gap-3">
          <div class="text-right">
            <p class="text-sm font-bold text-gray-800">{{ user.username }}</p>
            <span class="text-[10px] bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded font-black uppercase">{{ user.role || 'Akademik' }}</span>
          </div>
        </div>
      </header>

      <section class="flex-1 overflow-y-auto p-6 md:p-8">
        <!-- ===================== TAB ANTRIAN ===================== -->
        <div v-if="activeTab === 'antrian'">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
              <p class="text-xs font-bold text-gray-400 uppercase">Total Pengajuan</p>
              <h3 class="text-2xl font-black text-gray-800">{{ listMahasiswa.length }}</h3>
            </div>
            <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
              <p class="text-xs font-bold text-gray-400 uppercase text-orange-500">Antrian Menunggu</p>
              <h3 class="text-2xl font-black text-orange-600">{{ countStatus('MENUNGGU') }}</h3>
            </div>
            <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
              <p class="text-xs font-bold text-gray-400 uppercase text-green-500">Selesai Diverifikasi</p>
              <h3 class="text-2xl font-black text-green-600">{{ countStatus('DISETUJUI') }}</h3>
            </div>
            <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
              <p class="text-xs font-bold text-gray-400 uppercase text-red-500">Ditolak / Revisi</p>
              <h3 class="text-2xl font-black text-red-600">{{ countStatus('DITOLAK') }}</h3>
            </div>
          </div>

          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div class="p-6 border-b border-gray-50 flex justify-between items-center bg-gray-50">
              <h3 class="font-bold text-gray-800 text-lg">Daftar Antrian Verifikasi Yudisium</h3>
              <input v-model="search" @input="resetPagination()" type="text" placeholder="Cari Nama/NIM..." 
                     class="text-sm border border-gray-200 rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-indigo-500 w-64" />
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead class="bg-gray-100 text-gray-500 text-[11px] uppercase font-bold tracking-tighter">
                  <tr>
                    <th class="px-6 py-4">Mahasiswa</th>
                    <th class="px-6 py-4">NIM</th>
                    <th class="px-6 py-4 text-center">Status</th>
                    <th class="px-6 py-4 text-center">Aksi</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 text-sm">
                  <tr v-for="mhs in paginatedAntrian" :key="mhs.mahasiswa_id" class="hover:bg-indigo-50/30 transition">
                    <td class="px-6 py-4 font-bold text-gray-700 cursor-pointer hover:text-indigo-600" 
                        @click="bukaModalVerifikasi(mhs)">{{ mhs.full_name }}</td>
                    <td class="px-6 py-4 text-gray-500 font-mono">{{ mhs.nim }}</td>
                    <td class="px-6 py-4 text-center">
                      <span :class="{
                        'bg-orange-100 text-orange-700': mhs.status_akademik === 'MENUNGGU',
                        'bg-green-100 text-green-700': mhs.status_akademik === 'DISETUJUI',
                        'bg-red-100 text-red-700': mhs.status_akademik === 'DITOLAK'
                      }" class="px-2 py-1 rounded text-[10px] font-bold uppercase">
                        {{ mhs.status_akademik || 'MENUNGGU' }}
                      </span>
                    </td>
                    <td class="px-6 py-4 flex justify-center gap-2">
                      <button @click="bukaModalVerifikasi(mhs)" class="bg-indigo-600 hover:bg-indigo-700 text-white px-3 py-1.5 rounded-lg text-xs font-bold transition shadow-sm">
                        Verifikasi
                      </button>
                    </td>
                  </tr>
                  <tr v-if="paginatedAntrian.length === 0">
                    <td colspan="4" class="px-6 py-10 text-center text-gray-400 italic">Tidak ada antrian verifikasi saat ini.</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <!-- Pagination Antrian -->
            <div class="px-6 py-4 border-t border-gray-100 flex flex-col md:flex-row justify-between items-center gap-3 bg-gray-50">
              <div class="text-sm text-gray-500">
                Menampilkan {{ ((currentPageAntrian - 1) * rowsPerPageAntrian) + 1 }} - {{ Math.min(currentPageAntrian * rowsPerPageAntrian, filteredAntrian.length) }} dari {{ filteredAntrian.length }} data
              </div>
              <div class="flex gap-2 items-center">
                <button @click="prevPageAntrian" :disabled="currentPageAntrian === 1" class="px-3 py-1 border rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 transition">← Prev</button>
                <span class="px-3 py-1 text-sm">Halaman {{ currentPageAntrian }} dari {{ totalPagesAntrian }}</span>
                <button @click="nextPageAntrian" :disabled="currentPageAntrian === totalPagesAntrian" class="px-3 py-1 border rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 transition">Next →</button>
                <select v-model="rowsPerPageAntrian" @change="currentPageAntrian = 1" class="ml-2 border rounded px-2 py-1 text-sm">
                  <option :value="5">5</option>
                  <option :value="10">10</option>
                  <option :value="25">25</option>
                  <option :value="50">50</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- ===================== TAB RIWAYAT ===================== -->
        <div v-if="activeTab === 'riwayat'">
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div class="p-6 border-b border-gray-50 flex justify-between items-center bg-gray-50">
              <h3 class="font-bold text-gray-800 text-lg">Riwayat Verifikasi Mahasiswa</h3>
              <input v-model="search" @input="resetPagination()" type="text" placeholder="Cari Nama/NIM..." 
                     class="text-sm border border-gray-200 rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-indigo-500 w-64" />
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead class="bg-gray-100 text-gray-500 text-[11px] uppercase font-bold tracking-tighter">
                  <tr>
                    <th class="px-6 py-4">Mahasiswa</th>
                    <th class="px-6 py-4">NIM</th>
                    <th class="px-6 py-4 text-center">Total Pengajuan</th>
                    <th class="px-6 py-4 text-center">Status Terakhir</th>
                    <th class="px-6 py-4 text-center">Aksi</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 text-sm">
                  <tr v-for="mhs in paginatedRiwayat" :key="mhs.nim" class="hover:bg-gray-50 transition">
                    <td class="px-6 py-4 font-bold text-gray-700 cursor-pointer hover:text-indigo-600" 
                        @click="bukaModalRiwayat(mhs)">{{ mhs.full_name }}</td>
                    <td class="px-6 py-4 text-gray-500 font-mono">{{ mhs.nim }}</td>
                    <td class="px-6 py-4 text-center">
                      <span class="bg-indigo-100 text-indigo-700 px-2 py-1 rounded-full text-xs font-bold">{{ mhs.history.length }} Berkas</span>
                    </td>
                    <td class="px-6 py-4 text-center">
                      <span :class="{
                        'bg-green-100 text-green-700': mhs.status_terakhir === 'DISETUJUI',
                        'bg-red-100 text-red-700': mhs.status_terakhir === 'DITOLAK',
                        'bg-orange-100 text-orange-700': mhs.status_terakhir !== 'DISETUJUI' && mhs.status_terakhir !== 'DITOLAK'
                      }" class="px-2 py-1 rounded text-[10px] font-bold uppercase">
                        {{ mhs.status_terakhir || 'MENUNGGU' }}
                      </span>
                    </td>
                    <td class="px-6 py-4 text-center">
                      <button @click="bukaModalRiwayat(mhs)" class="bg-slate-800 hover:bg-slate-900 text-white px-4 py-2 rounded-lg text-xs font-bold transition shadow-sm flex items-center justify-center gap-2 mx-auto">
                        🔍 Lihat Riwayat
                      </button>
                    </td>
                  </tr>
                  <tr v-if="paginatedRiwayat.length === 0">
                    <td colspan="5" class="px-6 py-10 text-center text-gray-400 italic">Belum ada data riwayat mahasiswa.</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <!-- Pagination Riwayat -->
            <div class="px-6 py-4 border-t border-gray-100 flex flex-col md:flex-row justify-between items-center gap-3 bg-gray-50">
              <div class="text-sm text-gray-500">
                Menampilkan {{ ((currentPageRiwayat - 1) * rowsPerPageRiwayat) + 1 }} - {{ Math.min(currentPageRiwayat * rowsPerPageRiwayat, filteredRiwayat.length) }} dari {{ filteredRiwayat.length }} data
              </div>
              <div class="flex gap-2 items-center">
                <button @click="prevPageRiwayat" :disabled="currentPageRiwayat === 1" class="px-3 py-1 border rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 transition">← Prev</button>
                <span class="px-3 py-1 text-sm">Halaman {{ currentPageRiwayat }} dari {{ totalPagesRiwayat }}</span>
                <button @click="nextPageRiwayat" :disabled="currentPageRiwayat === totalPagesRiwayat" class="px-3 py-1 border rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 transition">Next →</button>
                <select v-model="rowsPerPageRiwayat" @change="currentPageRiwayat = 1" class="ml-2 border rounded px-2 py-1 text-sm">
                  <option :value="5">5</option>
                  <option :value="10">10</option>
                  <option :value="25">25</option>
                  <option :value="50">50</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- ===================== TAB PERIODE YUDISIUM (BARU) ===================== -->
        <div v-if="activeTab === 'periode'">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-bold text-gray-800">📅 Kelola Periode Yudisium</h2>
            <button @click="bukaFormPeriode()" 
                    class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-bold shadow-md transition flex items-center gap-2">
              <span>➕</span> Tambah Periode
            </button>
          </div>

          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead class="bg-gray-100 text-gray-500 text-[11px] uppercase font-bold tracking-tighter">
                  <tr>
                    <th class="px-6 py-4">Nama Periode</th>
                    <th class="px-6 py-4">Tanggal Mulai</th>
                    <th class="px-6 py-4">Tanggal Selesai</th>
                    <th class="px-6 py-4 text-center">Status</th>
                    <th class="px-6 py-4 text-center">Aksi</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 text-sm">
                  <tr v-for="periode in listPeriode" :key="periode.id" class="hover:bg-gray-50 transition">
                    <td class="px-6 py-4 font-bold text-gray-700">{{ periode.nama_periode }}</td>
                    <td class="px-6 py-4">{{ formatDate(periode.tanggal_mulai) }}</td>
                    <td class="px-6 py-4">{{ formatDate(periode.tanggal_selesai) }}</td>
                    <td class="px-6 py-4 text-center">
                      <span :class="periode.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'"
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
                                class="bg-indigo-500 hover:bg-indigo-600 text-white px-3 py-1.5 rounded-lg text-xs font-bold transition shadow-sm">
                          ✏️ Edit
                        </button>
                        <button @click="hapusPeriode(periode.id)" 
                                class="bg-red-500 hover:bg-red-600 text-white px-3 py-1.5 rounded-lg text-xs font-bold transition shadow-sm">
                          🗑️ Hapus
                        </button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="listPeriode.length === 0">
                    <td colspan="5" class="px-6 py-10 text-center text-gray-400 italic">Belum ada periode yudisium.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- ===================== MODAL VERIFIKASI (SAMA) ===================== -->
    <div v-if="showVerifikasiModal" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm flex justify-center items-center z-50 p-4" @click.self="showVerifikasiModal = false">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-lg overflow-hidden flex flex-col transform transition-all">
        <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50">
          <h2 class="font-bold text-gray-800 text-lg">Verifikasi Berkas Akademik</h2>
          <button @click="showVerifikasiModal = false" class="text-gray-400 hover:text-red-500 transition font-bold text-xl">&times;</button>
        </div>
        <div class="p-6 space-y-4 flex-1 overflow-y-auto">
          <div class="bg-slate-50 p-4 rounded-lg border border-slate-100">
            <p class="text-xs text-slate-500 uppercase font-bold">Informasi Mahasiswa</p>
            <p class="font-bold text-slate-800">{{ selectedMhs?.full_name }}</p>
            <p class="text-sm text-slate-500 font-mono">{{ selectedMhs?.nim }}</p>
            <p class="text-xs text-slate-500 uppercase font-bold mt-4 mb-2">Daftar Berkas Terkirim</p>
            <div class="grid grid-cols-2 gap-3">
              <div v-for="doc in documentRequirements" :key="doc.key" class="p-3 border border-gray-200 rounded-lg bg-white flex justify-between items-center shadow-sm">
                <div class="flex items-center gap-2">
                  <span class="text-lg">📄</span>
                  <span class="text-[10px] font-bold text-slate-700">{{ doc.name }}</span>
                </div>
                <a v-if="selectedMhs && selectedMhs[doc.key]" :href="selectedMhs[doc.key]" target="_blank" class="text-indigo-600 bg-indigo-50 px-2 py-1 rounded text-[10px] font-bold">Buka</a>
                <span v-else class="text-[10px] font-bold text-red-500 bg-red-50 px-2 py-1 rounded">KOSONG</span>
              </div>
            </div>
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Catatan (Opsional / Wajib jika ditolak)</label>
            <textarea v-model="formCatatan" rows="3" class="w-full border border-gray-200 rounded-lg p-3 text-sm outline-none focus:ring-2 focus:ring-indigo-500"
                      placeholder="Masukkan catatan revisi jika ada..."></textarea>
          </div>
        </div>
        <div class="p-6 border-t border-gray-100 flex justify-end gap-3 bg-gray-50">
          <button @click="showVerifikasiModal = false" class="px-4 py-2 text-sm font-bold text-gray-500 hover:text-gray-700">Batal</button>
          <button @click="submitVerifikasi('DITOLAK')" class="px-4 py-2 bg-red-100 text-red-600 hover:bg-red-200 rounded-lg text-sm font-bold transition">Tolak / Revisi</button>
          <button @click="submitVerifikasi('DISETUJUI')" class="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg text-sm font-bold shadow-md transition">Setujui</button>
        </div>
      </div>
    </div>

    <!-- ===================== MODAL RIWAYAT (SAMA) ===================== -->
    <div v-if="showRiwayatModal" class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4 transition-opacity" @click.self="showRiwayatModal = false">
      <div class="bg-white rounded-2xl w-full max-w-4xl max-h-[85vh] flex flex-col shadow-2xl">
        <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50 rounded-t-2xl">
          <div>
            <h2 class="text-xl font-bold text-slate-900">Riwayat Pengajuan Yudisium</h2>
            <p class="text-sm text-slate-600 font-medium mt-1">{{ selectedRiwayatMhs?.full_name }} ({{ selectedRiwayatMhs?.nim }})</p>
          </div>
          <button @click="showRiwayatModal = false" class="text-gray-400 hover:text-red-500 hover:bg-red-50 p-2 rounded-lg transition font-bold text-xl">✕</button>
        </div>
        <div class="p-6 overflow-y-auto flex-1">
          <div class="border border-gray-100 rounded-xl overflow-hidden">
            <table class="w-full text-left border-collapse">
              <thead class="bg-gray-50 text-gray-500 text-[11px] uppercase font-bold">
                <tr>
                  <th class="px-6 py-4 text-center w-16">NO</th>
                  <th class="px-6 py-4">BERKAS YUDISIUM</th>
                  <th class="px-6 py-4 text-center">STATUS</th>
                  <th class="px-6 py-4">CATATAN PETUGAS</th>
                  <th class="px-6 py-4 text-center">TANGGAL</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="(hist, index) in sortedHistory" :key="index" class="hover:bg-gray-50 transition-colors">
                  <td class="px-6 py-4 text-sm text-gray-600 font-medium text-center">{{ index + 1 }}</td>
                  <td class="px-6 py-4">
                    <div class="flex flex-col gap-1">
                      <a v-if="hist.foto_ijazah" :href="hist.foto_ijazah" target="_blank" class="text-indigo-600 hover:text-indigo-800 text-sm font-semibold">📄 Ijazah Akhir</a>
                      <a v-if="hist.foto_akte" :href="hist.foto_akte" target="_blank" class="text-indigo-600 hover:text-indigo-800 text-sm font-semibold">📄 Akte Kelahiran</a>
                      <a v-if="hist.foto_ktp" :href="hist.foto_ktp" target="_blank" class="text-indigo-600 hover:text-indigo-800 text-sm font-semibold">📄 KTP</a>
                      <a v-if="hist.foto_3x4" :href="hist.foto_3x4" target="_blank" class="text-indigo-600 hover:text-indigo-800 text-sm font-semibold">📄 Foto 3x4</a>
                      <span v-if="!hist.foto_ijazah && !hist.foto_akte && !hist.foto_ktp && !hist.foto_3x4" class="text-gray-400 text-xs italic">Tidak ada file</span>
                    </div>
                  </td>
                  <td class="px-6 py-4 text-center">
                    <span :class="[
                      'px-2 py-1 rounded-md text-[9px] font-black uppercase tracking-wider',
                      hist.status_akademik === 'DISETUJUI' ? 'bg-green-100 text-green-700' : 
                      hist.status_akademik === 'DITOLAK' ? 'bg-red-100 text-red-700' : 
                      'bg-orange-100 text-orange-700'
                    ]">
                      {{ hist.status_akademik || 'MENUNGGU' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-600">{{ hist.catatan_akademik || '-' }}</td>
                  <td class="px-6 py-4 text-center text-sm text-gray-500">{{ formatDate(hist.validated_at || hist.updated_at || hist.created_at) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- ===================== MODAL FORM PERIODE (BARU) ===================== -->
    <div v-if="showModalPeriode" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex justify-center items-center z-50 p-4" @click.self="showModalPeriode = false">
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
import { ref, onMounted, computed, watch, defineComponent } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const router = useRouter();
const user = ref({ username: '', full_name: '', role: '' });
const listMahasiswa = ref([]);
const search = ref('');

// ========== KOMPONEN STATUS BADGE ==========
const StatusBadge = defineComponent({
  props: ['status'],
  template: `
    <span :class="[
      'px-2 py-1 rounded-md text-[9px] font-black uppercase tracking-wider',
      status === 'DISETUJUI' ? 'bg-green-100 text-green-700' : 
      status === 'DITOLAK' ? 'bg-red-100 text-red-700' : 
      'bg-orange-100 text-orange-700'
    ]">
      {{ status === 'DISETUJUI' ? 'DISETUJUI' : status === 'DITOLAK' ? 'DITOLAK' : 'MENUNGGU' }}
    </span>
  `
});

// ========== KONFIGURASI BERKAS ==========
const documentRequirements = [
  { name: 'Ijazah Akhir', key: 'foto_ijazah' },
  { name: 'Akte Kelahiran', key: 'foto_akte' },
  { name: 'KTP', key: 'foto_ktp' },
  { name: 'Foto 3x4', key: 'foto_3x4' }
];

// ========== STATE TAB ==========
const activeTab = ref('antrian');

// ========== STATE MODAL VERIFIKASI & RIWAYAT ==========
const showVerifikasiModal = ref(false);
const selectedMhs = ref(null);
const formCatatan = ref('');
const showRiwayatModal = ref(false);
const selectedRiwayatMhs = ref(null);

// ========== STATE PAGINATION ==========
const currentPageAntrian = ref(1);
const rowsPerPageAntrian = ref(10);
const currentPageRiwayat = ref(1);
const rowsPerPageRiwayat = ref(10);

// ========== STATE PERIODE ==========
const listPeriode = ref([]);
const showModalPeriode = ref(false);
const isEditPeriode = ref(false);
const formPeriode = ref({ nama_periode: '', tanggal_mulai: '', tanggal_selesai: '' });
const editPeriodeId = ref(null);

// ========== FUNGSI FORMAT TANGGAL ==========
const formatDate = (dateString) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleDateString('id-ID', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  });
};

// ========== RESET PAGINATION ==========
const resetPagination = () => {
  currentPageAntrian.value = 1;
  currentPageRiwayat.value = 1;
};

// ========== FETCH DATA ==========
const fetchData = async () => {
  console.log("[LOG] Memulai fetchData...");
  try {
    const resUser = await api.get('users/me/');
    user.value = resUser.data;
    const resMhs = await api.get('akademik/list-mahasiswa/');
    listMahasiswa.value = resMhs.data;
    listMahasiswa.value.sort((a, b) => new Date(b.updated_at || b.created_at) - new Date(a.updated_at || a.created_at));
    console.log("[LOG] Mahasiswa data:", listMahasiswa.value.length, "data");
  } catch (err) {
    console.error("[ERROR] Gagal load data akademik", err);
    if (err.response?.status === 401) {
      alert("Sesi berakhir, silakan login ulang.");
      handleLogout();
    }
  }
};

// ========== FETCH PERIODE ==========
const fetchPeriode = async () => {
  try {
    const res = await api.get('periode-yudisium/');
    listPeriode.value = res.data;
    console.log("[LOG] Periode data:", listPeriode.value.length, "data");
  } catch (err) {
    console.error("[ERROR] Gagal ambil periode:", err);
  }
};

// ========== CRUD PERIODE ==========
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
    console.error("[ERROR] Gagal simpan periode:", err);
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
    console.error("[ERROR] Gagal hapus periode:", err);
    alert('Gagal menghapus periode.');
  }
};

const toggleAktif = async (periode) => {
  const newStatus = !periode.is_active;
  try {
    await api.patch(`periode-yudisium/${periode.id}/`, { is_active: newStatus });
    alert(`Periode berhasil ${newStatus ? 'diaktifkan' : 'dinonaktifkan'}.`);
    await fetchPeriode();
    // Jika mengaktifkan, pastikan yang lain nonaktif (backend seharusnya menangani)
  } catch (err) {
    console.error("[ERROR] Gagal toggle status:", err);
    alert('Gagal mengubah status periode.');
  }
};

// ========== FUNGSI UNTUK TAB ANTRIAN & RIWAYAT ==========
const countStatus = (s) => listMahasiswa.value.filter(m => (m.status_akademik || m.status_akhir) === s).length;

const antrianCount = computed(() => {
  return listMahasiswa.value.filter(m => {
    const status = m.status_akademik || m.status_akhir;
    return status === 'MENUNGGU' || status === 'BELUM DAFTAR' || !status;
  }).length;
});

// Filter Antrian
const filteredAntrian = computed(() => {
  const query = search.value.toLowerCase();
  return listMahasiswa.value.filter(m => {
    const status = m.status_akademik || m.status_akhir;
    const isAntrian = (status === 'MENUNGGU' || status === 'BELUM DAFTAR' || !status) &&
                      (m.foto_ijazah || m.foto_akte || m.foto_ktp || m.foto_3x4);
    const matchSearch = (m.full_name || '').toLowerCase().includes(query) ||
                        (m.nim || '').toLowerCase().includes(query);
    return isAntrian && matchSearch;
  });
});

const totalPagesAntrian = computed(() => Math.ceil(filteredAntrian.value.length / rowsPerPageAntrian.value));
const paginatedAntrian = computed(() => {
  const start = (currentPageAntrian.value - 1) * rowsPerPageAntrian.value;
  return filteredAntrian.value.slice(start, start + rowsPerPageAntrian.value);
});

const prevPageAntrian = () => { if (currentPageAntrian.value > 1) currentPageAntrian.value--; };
const nextPageAntrian = () => { if (currentPageAntrian.value < totalPagesAntrian.value) currentPageAntrian.value++; };

// Filter Riwayat
const filteredRiwayat = computed(() => {
  const groups = {};
  listMahasiswa.value.forEach(item => {
    const nim = item.nim || 'NIM_UNKNOWN';
    if (!groups[nim]) {
      groups[nim] = { 
        nim: nim, 
        full_name: item.full_name || 'NAMA TIDAK DITEMUKAN', 
        history: [],
        status_terakhir: item.status_akademik || item.status_akhir,
        last_updated: item.updated_at || item.created_at
      };
    }
    groups[nim].history.push(item);
    const itemDate = item.updated_at || item.created_at;
    if (itemDate && (!groups[nim].last_updated || new Date(itemDate) > new Date(groups[nim].last_updated))) {
      groups[nim].last_updated = itemDate;
    }
    if (item.status_akademik && item.status_akademik !== 'MENUNGGU') {
      groups[nim].status_terakhir = item.status_akademik;
    }
  });
  Object.values(groups).forEach(group => {
    group.history.sort((a, b) => new Date(b.created_at || b.updated_at) - new Date(a.created_at || a.updated_at));
  });
  const riwayatArray = Object.values(groups);
  riwayatArray.sort((a, b) => new Date(b.last_updated) - new Date(a.last_updated));
  if (!search.value) return riwayatArray;
  return riwayatArray.filter(mhs => {
    const nama = mhs.full_name.toLowerCase();
    const nim = mhs.nim.toLowerCase();
    const query = search.value.toLowerCase();
    return nama.includes(query) || nim.includes(query);
  });
});

const totalPagesRiwayat = computed(() => Math.ceil(filteredRiwayat.value.length / rowsPerPageRiwayat.value));
const paginatedRiwayat = computed(() => {
  const start = (currentPageRiwayat.value - 1) * rowsPerPageRiwayat.value;
  return filteredRiwayat.value.slice(start, start + rowsPerPageRiwayat.value);
});

const prevPageRiwayat = () => { if (currentPageRiwayat.value > 1) currentPageRiwayat.value--; };
const nextPageRiwayat = () => { if (currentPageRiwayat.value < totalPagesRiwayat.value) currentPageRiwayat.value++; };

const sortedHistory = computed(() => {
  if (!selectedRiwayatMhs.value?.history) return [];
  return [...selectedRiwayatMhs.value.history].sort((a, b) => 
    new Date(b.created_at || b.updated_at) - new Date(a.created_at || a.updated_at)
  );
});

// ========== MODAL VERIFIKASI ==========
const bukaModalVerifikasi = (mhs) => {
  selectedMhs.value = mhs;
  formCatatan.value = mhs.catatan_akademik || '';
  showVerifikasiModal.value = true;
};

const submitVerifikasi = async (statusKeputusan) => {
  if (selectedMhs.value.status_akademik === 'BELUM DAFTAR') {
    alert("Mahasiswa ini belum mengunggah berkas. Tidak ada data untuk diverifikasi.");
    return;
  }
  if (statusKeputusan === 'DITOLAK' && !formCatatan.value.trim()) {
    alert("Harap berikan catatan alasan penolakan!");
    return;
  }
  const payload = {
    mahasiswa_id: selectedMhs.value.mahasiswa_id || selectedMhs.value.id,
    status: statusKeputusan,
    catatan: formCatatan.value
  };
  try {
    await api.post('akademik/verifikasi-berkas/', payload);
    alert(`Sukses! Berkas telah ${statusKeputusan === 'DISETUJUI' ? 'disetujui' : 'ditolak'}.`);
    showVerifikasiModal.value = false;
    await fetchData();
  } catch (err) {
    const msg = err.response?.data?.error || "Gagal menghubungi server";
    alert("Gagal Verifikasi: " + msg);
  }
};

// ========== MODAL RIWAYAT ==========
const bukaModalRiwayat = (mhsGroup) => {
  selectedRiwayatMhs.value = mhsGroup;
  showRiwayatModal.value = true;
};

// ========== LOGOUT ==========
const handleLogout = () => {
  localStorage.clear();
  router.replace({ name: 'login' });
};

// ========== WATCHER ==========
watch(search, () => resetPagination());
watch(rowsPerPageAntrian, () => currentPageAntrian.value = 1);
watch(rowsPerPageRiwayat, () => currentPageRiwayat.value = 1);

// ========== MOUNTED ==========
onMounted(async () => {
  await fetchData();
  await fetchPeriode();
});
</script>
