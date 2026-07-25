<template>
  <div class="flex h-screen bg-slate-50">
    <aside class="w-64 bg-slate-900 text-white hidden md:flex flex-col shadow-xl">
      <div class="p-6 text-xl font-bold border-b border-indigo-900 flex items-center gap-2">
        <span class="p-2 bg-indigo-500 rounded-lg text-white text-sm">📚</span>
        Library Center
      </div>
      <nav class="flex-1 p-4 space-y-1">
        <p class="text-xs text-indigo-400 font-bold px-4 mb-2 uppercase tracking-widest">Layanan</p>
        
        <button @click="activeTab = 'antrian'; resetPagination()" :class="['w-full text-left flex items-center space-x-3 py-3 px-4 rounded-lg transition-all', activeTab === 'antrian' ? 'bg-indigo-800 shadow-inner' : 'hover:bg-indigo-800/50']">
          <span>📋 Antrian Verifikasi</span>
          <span v-if="antrianCount > 0" class="ml-auto bg-red-500 text-white text-[10px] rounded-full px-2 py-0.5">{{ antrianCount }}</span>
        </button>
        
        <button @click="activeTab = 'riwayat'; resetPagination()" :class="['w-full text-left flex items-center space-x-3 py-3 px-4 rounded-lg transition-all', activeTab === 'riwayat' ? 'bg-indigo-800 shadow-inner' : 'hover:bg-indigo-800/50']">
          <span>🗂️ Riwayat Mahasiswa</span>
        </button>

        <button @click="openTemplateModal" class="w-full text-left flex items-center space-x-3 py-3 px-4 rounded-lg transition-all hover:bg-indigo-800/50">
          <span>📝 Edit Template Surat</span>
        </button>

        <button @click="openTtdModal" class="w-full text-left flex items-center space-x-3 py-3 px-4 rounded-lg transition-all hover:bg-indigo-800/50">
          <span>✍️ Atur Tanda Tangan</span>
        </button>
      </nav>
      <div class="p-4 border-t border-indigo-900">
        <button @click="handleLogout" class="w-full bg-red-500/10 text-red-400 hover:bg-red-500 hover:text-white py-2.5 rounded-lg text-sm font-bold transition-all">
          Keluar Sistem
        </button>
      </div>
    </aside>

    <main class="flex-1 flex flex-col overflow-hidden relative">
      <header class="bg-white border-b border-gray-200 py-4 px-8 flex justify-between items-center z-10">
        <div>
          <h1 class="text-lg font-bold text-gray-800">Verifikasi Bebas Perpustakaan</h1>
          <p class="text-xs text-gray-500">Petugas: {{ user.full_name }}</p>
        </div>
        <div class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-[10px] font-black uppercase">
          {{ user.role || 'PERPUS' }}
        </div>
      </header>

      <section class="flex-1 overflow-y-auto p-6 md:p-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div class="bg-white p-6 rounded-2xl shadow-sm border-l-4 border-orange-500">
            <p class="text-xs font-bold text-gray-400 uppercase">Belum Validasi</p>
            <h3 class="text-3xl font-black text-gray-800">{{ countStatus('MENUNGGU') }}</h3>
          </div>
          <div class="bg-white p-6 rounded-2xl shadow-sm border-l-4 border-green-500">
            <p class="text-xs font-bold text-gray-400 uppercase">Sudah Disetujui</p>
            <h3 class="text-3xl font-black text-gray-800">{{ countStatus('DISETUJUI') }}</h3>
          </div>
          <div class="bg-white p-6 rounded-2xl shadow-sm border-l-4 border-red-500">
            <p class="text-xs font-bold text-gray-400 uppercase">Ditolak</p>
            <h3 class="text-3xl font-black text-gray-800">{{ countStatus('DITOLAK') }}</h3>
          </div>
        </div>

        <div class="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="p-4 border-b border-gray-100 bg-gray-50 flex flex-col md:flex-row justify-between items-center gap-3">
            <h3 class="font-bold text-gray-800 text-sm">
              {{ activeTab === 'antrian' ? '📋 Daftar Antrian Validasi' : '🗂️ Daftar Riwayat Mahasiswa' }}
            </h3>
            <div class="flex gap-3 w-full md:w-auto">
              <input 
                v-model="search" 
                @input="resetPagination()"
                type="text" 
                placeholder="🔍 Cari Nama/NIM..." 
                class="text-sm border border-gray-200 rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-indigo-500 w-full md:w-64"
              />
            </div>
          </div>
          
          <div v-if="activeTab === 'antrian'">
            <div class="overflow-x-auto">
              <table class="w-full text-left">
                <thead class="bg-gray-50 text-gray-400 text-[10px] uppercase font-bold">
                  <tr>
                    <th class="px-6 py-4">Mahasiswa</th>
                    <th class="px-6 py-4 text-center">Status Perpus</th>
                    <th class="px-6 py-4 text-center">Berkas Perpustakaan</th>
                    <th class="px-6 py-4 text-center">Aksi</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 text-sm">
                  <tr v-for="mhs in paginatedAntrian" :key="mhs.id" class="hover:bg-indigo-50/20 transition">
                    <td class="px-6 py-4">
                      <p class="font-bold text-gray-800">{{ mhs.full_name || 'NAMA TIDAK DITEMUKAN' }}</p>
                      <p class="text-[10px] text-gray-400 font-mono">{{ mhs.nim || 'NIM TIDAK DITEMUKAN' }}</p>
                      <p class="text-[10px] text-gray-400 mt-1">Email: {{ mhs.email || '-' }}</p>
                      <p class="text-[10px] text-gray-400">Upload: {{ formatDate(mhs.created_at) }}</p>
                    </td>
                    <td class="px-6 py-4 text-center">
                      <span :class="{
                        'bg-orange-100 text-orange-700': mhs.status === 'MENUNGGU',
                        'bg-green-100 text-green-700': mhs.status === 'DISETUJUI',
                        'bg-red-100 text-red-700': mhs.status === 'DITOLAK'
                      }" class="px-3 py-1 rounded text-[9px] font-black uppercase">
                        {{ mhs.status }}
                      </span>
                    </td>
                    <td class="px-6 py-4">
                      <button 
                        @click="openBerkasModal(mhs)"
                        class="bg-indigo-100 text-indigo-700 px-4 py-2 rounded-lg text-xs font-bold hover:bg-indigo-200 transition inline-flex items-center gap-2"
                      >
                        📂 Lihat Semua Berkas ({{ getAllFilesCount(mhs) }})
                      </button>
                    </td>
                    <td class="px-6 py-4">
                      <div class="flex justify-center gap-2 flex-wrap">
                        <template v-if="mhs.status === 'MENUNGGU'">
                          <button @click="setujuiBerkas(mhs)" class="bg-indigo-600 text-white px-3 py-1.5 rounded-lg text-xs font-bold hover:shadow-lg transition">
                            ✔ Setujui & Buat Surat
                          </button>
                          <button @click="openTolakModal(mhs.id, mhs.full_name)" class="bg-white border border-red-200 text-red-500 px-3 py-1.5 rounded-lg text-xs font-bold hover:bg-red-50 transition">
                            ❌ Tolak
                          </button>
                        </template>
                        <template v-else-if="mhs.status === 'DISETUJUI'">
                          <button @click="bukaModalSurat(mhs)" class="bg-teal-600 text-white px-3 py-1.5 rounded-lg text-xs font-bold hover:shadow-lg transition">
                            👁️ Lihat/Edit Surat
                          </button>
                        </template>
                        <span v-else class="text-xs text-red-500 italic">Ditolak</span>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="paginatedAntrian.length === 0">
                    <td colspan="4" class="px-6 py-10 text-center text-gray-400 italic">Tidak ada antrian validasi saat ini.</td>
                  </tr>
                </tbody>
              </table>
            </div>
            
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

          <div v-if="activeTab === 'riwayat'">
            <div class="overflow-x-auto">
              <table class="w-full text-left">
                <thead class="bg-gray-50 text-gray-400 text-[10px] uppercase font-bold">
                  <tr>
                    <th class="px-6 py-4">Mahasiswa</th>
                    <th class="px-6 py-4 text-center">Total Pengajuan</th>
                    <th class="px-6 py-4 text-center">Berkas</th>
                    <th class="px-6 py-4 text-center">Surat Bebas Pustaka</th>
                    <th class="px-6 py-4 text-center">Aksi</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 text-sm">
                  <tr v-for="mhs in paginatedRiwayat" :key="mhs.nim" class="hover:bg-indigo-50/20 transition">
                    <td class="px-6 py-4">
                      <p class="font-bold text-gray-800">{{ mhs.full_name }}</p>
                      <p class="text-[10px] text-gray-400 font-mono">{{ mhs.nim }}</p>
                      <p class="text-[10px] text-gray-400">Email: {{ mhs.email || '-' }}</p>
                    </td>
                    <td class="px-6 py-4 text-center">
                      <span class="bg-indigo-50 border border-indigo-100 text-indigo-700 px-2 py-1 rounded-full text-xs font-bold">
                        {{ mhs.history.length }} Pengajuan
                      </span>
                      <p class="text-[10px] text-gray-500 mt-1">Update: {{ formatDate(mhs.last_updated) }}</p>
                    </td>
                    <td class="px-6 py-4 text-center">
                      <button 
                        v-if="getAllFilesCount(mhs.history[0]) > 0"
                        @click="openBerkasModal(mhs.history[0])"
                        class="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-lg text-[10px] font-bold hover:bg-indigo-200 transition inline-flex items-center gap-1"
                      >
                        📂 Lihat Semua Berkas ({{ getAllFilesCount(mhs.history[0]) }})
                      </button>
                      <span v-else class="text-xs text-gray-400 italic">Tidak ada</span>
                    </td>
                    <td class="px-6 py-4 text-center">
                      <button 
                        v-if="mhs.history[0]?.status === 'DISETUJUI'" 
                        @click="bukaModalSurat(mhs.history[0])" 
                        class="bg-indigo-100 text-indigo-700 px-4 py-1.5 rounded-full text-xs font-bold hover:bg-indigo-200 hover:shadow transition flex items-center justify-center gap-1 mx-auto"
                      >
                        👁️ Lihat/Edit Surat
                      </button>
                      <span v-else class="text-gray-400 italic text-xs">Belum Tersedia</span>
                    </td>
                    <td class="px-6 py-4 text-center">
                      <button @click="bukaModalDetail(mhs)" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-xs font-bold transition shadow-sm mx-auto flex items-center justify-center gap-2">
                        🔍 Lihat Detail Lengkap
                      </button>
                    </td>
                  </tr>
                  <tr v-if="paginatedRiwayat.length === 0">
                    <td colspan="5" class="px-6 py-10 text-center text-gray-400 italic">Belum ada data riwayat mahasiswa.</td>
                  </tr>
                </tbody>
              </table>
            </div>
            
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
      </section>

      <!-- MODAL TEMPLATE SURAT -->
      <div v-if="showTemplateModal" class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-4xl flex flex-col max-h-[90vh] overflow-hidden">
          <div class="bg-indigo-950 text-white p-4 flex justify-between items-center">
            <div>
              <h3 class="font-bold text-lg">📝 Edit Template Surat Bebas Perpustakaan</h3>
              <p class="text-xs text-indigo-200 mt-1">Template ini akan digunakan untuk semua surat. Gunakan placeholder: [NAMA], [NIM], [JURUSAN], [TANGGAL], [PETUGAS]</p>
            </div>
            <button @click="showTemplateModal = false" class="text-white hover:text-red-400 font-bold text-xl">&times;</button>
          </div>
          
          <div class="p-6 overflow-y-auto flex-1 bg-gray-100">
            <div class="bg-white p-6 shadow-sm border border-gray-200 rounded">
              <textarea 
                v-model="templateSurat" 
                class="w-full h-[400px] p-4 border border-gray-300 bg-gray-50 focus:bg-white focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none resize-none font-mono text-sm leading-relaxed rounded"
                placeholder="Tulis template surat di sini..."
              ></textarea>
              
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
          
          <div class="p-4 bg-white border-t border-gray-200 flex justify-end gap-3">
            <button @click="showTemplateModal = false" class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 text-sm font-bold">Batal</button>
            <button @click="simpanTemplateSurat" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg shadow text-sm font-bold">
              💾 Simpan Template
            </button>
          </div>
        </div>
      </div>

      <!-- MODAL SURAT -->
      <div v-if="showSuratModal" class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-6xl flex flex-col max-h-[90vh] overflow-hidden">
          <div class="bg-indigo-950 text-white p-4 flex justify-between items-center">
            <div>
              <h3 class="font-bold text-lg">📄 Dokumen Surat Bebas Perpustakaan</h3>
              <p class="text-xs text-indigo-200 mt-1">Edit surat dan atur posisi tanda tangan sesuai keinginan</p>
            </div>
            <button @click="showSuratModal = false" class="text-white hover:text-red-400 font-bold text-xl">&times;</button>
          </div>
          
          <div class="flex flex-1 overflow-hidden min-h-[500px]">
            <!-- Panel Kiri: Editor -->
            <div class="w-1/2 p-4 bg-gray-100 border-r border-gray-200 flex flex-col overflow-y-auto">
              <label class="text-xs font-bold text-gray-600 mb-2">✏️ Edit Isi Surat:</label>
              <textarea 
                v-model="isiSurat" 
                class="flex-1 min-h-[200px] p-4 border border-gray-300 bg-white focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none resize-none font-mono text-sm leading-relaxed rounded"
                placeholder="Isi surat akan digenerate dari template..."
              ></textarea>
              
              <div class="mt-3 flex justify-between items-center">
                <button @click="resetKeTemplate" class="text-xs text-indigo-600 hover:text-indigo-800">
                  ↺ Reset ke Template
                </button>
                <span class="text-xs text-gray-400">Karakter: {{ isiSurat.length }}</span>
              </div>

              <div class="mt-4 p-4 bg-white rounded-lg border border-gray-200">
                <p class="text-xs font-bold text-gray-700 mb-3">✍️ Atur Posisi Tanda Tangan:</p>
                
                <div class="flex gap-4 items-start">
                  <div class="flex-shrink-0">
                    <div v-if="ttdImage" class="border-2 border-dashed border-indigo-300 p-2 rounded-lg bg-gray-50">
                      <img :src="ttdImage" class="w-32 h-20 object-contain" />
                    </div>
                    <div v-else class="w-32 h-20 bg-gray-200 rounded-lg flex items-center justify-center text-xs text-gray-400">
                      Belum ada TTD
                    </div>
                    <button @click="openTtdModal" class="mt-2 text-[10px] text-indigo-600 hover:text-indigo-800 underline">
                      Ganti Tanda Tangan
                    </button>
                  </div>

                  <div class="flex-1">
                    <!-- Posisi Horizontal -->
                    <div class="mb-4">
                      <div class="flex justify-between items-center mb-1">
                        <p class="text-[10px] font-bold text-gray-600">Posisi Horizontal (Kiri - Kanan):</p>
                        <p class="text-[10px] font-bold text-indigo-600">{{ ttdPositionX }}%</p>
                      </div>
                      <input 
                        type="range" 
                        v-model="ttdPositionX" 
                        min="0" 
                        max="100" 
                        step="1"
                        class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                      />
                      <div class="flex justify-between text-[10px] text-gray-400 mt-1">
                        <span>◀ Kiri (0%)</span>
                        <span>Tengah (50%)</span>
                        <span>Kanan (100%) ▶</span>
                      </div>
                    </div>
                    
                    <!-- Posisi Vertikal -->
                    <div class="mb-4">
                      <div class="flex justify-between items-center mb-1">
                        <p class="text-[10px] font-bold text-gray-600">Posisi Vertikal (Atas - Bawah):</p>
                        <p class="text-[10px] font-bold text-indigo-600">{{ ttdPositionY }}%</p>
                      </div>
                      <input 
                        type="range" 
                        v-model="ttdPositionY" 
                        min="0" 
                        max="100" 
                        step="1"
                        class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                      />
                      <div class="flex justify-between text-[10px] text-gray-400 mt-1">
                        <span>▲ Atas (0%)</span>
                        <span>Tengah (50%)</span>
                        <span>Bawah (100%) ▼</span>
                      </div>
                      <p class="text-[9px] text-gray-400 mt-1">Geser ke atas (0%) untuk TTD di atas, ke bawah (100%) untuk TTD di bawah</p>
                    </div>

                    <!-- Preview posisi TTD -->
                    <div class="mt-3 p-3 bg-indigo-50 rounded-lg text-center">
                      <p class="text-[10px] font-semibold text-indigo-700 mb-2">🎯 Preview Posisi TTD:</p>
                      <div class="relative border-2 border-dashed border-indigo-300 rounded-lg h-24 bg-white overflow-hidden">
                        <div class="absolute inset-0 flex items-center justify-center">
                          <span class="text-[9px] text-gray-400">Area Surat</span>
                        </div>
                        <div 
                          class="absolute w-14 h-10 bg-indigo-500/70 border-2 border-indigo-700 rounded flex items-center justify-center text-[8px] font-bold text-white transition-all duration-150"
                          :style="{ 
                            left: `${ttdPositionX}%`, 
                            top: `${ttdPositionY}%`,
                            transform: 'translate(-50%, -50%)'
                          }"
                        >
                          TTD
                        </div>
                      </div>
                      <p class="text-[9px] text-gray-500 mt-2">Kotak biru = perkiraan posisi TTD</p>
                    </div>
                  </div>
                </div>

                <div class="mt-3">
                  <label class="text-[10px] font-bold text-gray-600">Nama Pustakawan:</label>
                  <input 
                    v-model="petugasName" 
                    type="text" 
                    class="w-full mt-1 px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
                    placeholder="Masukkan nama pustakawan"
                  />
                </div>

                <div class="mt-3">
                  <label class="text-[10px] font-bold text-gray-600">📝 Catatan Tambahan (opsional):</label>
                  <textarea 
                    v-model="catatanTambahan" 
                    class="w-full mt-1 px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 outline-none resize-none"
                    rows="2"
                    placeholder="Tambahkan catatan khusus untuk mahasiswa..."
                  ></textarea>
                </div>
              </div>
            </div>
            
            <!-- Panel Kanan: Preview Surat -->
            <div class="w-1/2 p-4 bg-gray-100 flex flex-col">
              <div class="flex justify-between items-center mb-2">
                <label class="text-xs font-bold text-gray-600">👁️ Preview Surat (akan menjadi PDF):</label>
              </div>
              
              <div id="suratPreview" class="flex-1 bg-white p-8 border border-gray-200 rounded overflow-y-auto shadow-inner" style="font-family: 'Times New Roman', serif; color: black;">
                <div class="max-w-2xl mx-auto">
                  
                  <div class="flex items-center justify-center border-b-[3px] border-black pb-4 mb-6">
                    <!-- Logo dari backend -->
                    <img 
                      v-if="logoUrl" 
                      :src="logoUrl" 
                      alt="Logo STIE SBI" 
                      class="w-20 h-20 object-contain mr-10" 
                      crossorigin="anonymous"
                      @error="console.log('Logo gagal dimuat:', $event)"
                    />
                    <div class="text-center flex-1 pr-12">
                      <h2 class="text-lg font-bold uppercase m-0 leading-tight">PERPUSTAKAAN</h2>
                      <h1 class="text-2xl font-black uppercase m-0 leading-tight">STIE SOLUSI BISNIS INDONESIA YOGYAKARTA</h1>
                      <p class="text-sm m-0 mt-2">Jl. Ring Road Utara No. 17, Condongcatur, Depok, Sleman, Yogyakarta 55283</p>
                      <p class="text-xs m-0">Telp. (0274) 887984 | Email: perpustakaan@stie-sbi.ac.id</p>
                    </div>
                  </div>
                  
                  <!-- ISI SURAT -->
                  <div class="whitespace-pre-wrap text-sm leading-relaxed space-y-3" style="font-family: 'Times New Roman', serif;">
                    <div class="text-center mb-4">
                      <span class="font-bold underline text-base">SURAT BEBAS PINJAMAN PUSTAKA</span>
                    </div>
                    
                    <p>Surat ini diberikan untuk permohonan mahasiswa yang sudah menyelesaikan semua biaya administrasi/denda :</p>
                    
                    <p>Identitas pemohon surat bebas pinjam pustaka ini :</p>
                    
                    <div class="ml-8 space-y-1">
                      <p>Nama &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : {{ selectedMhsForSurat?.full_name || '[NAMA]' }}</p>
                      <p>No. Mahasiswa &nbsp;&nbsp;&nbsp; : {{ selectedMhsForSurat?.nim || '[NIM]' }}</p>
                      <p>Jurusan &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : {{ selectedMhsForSurat?.jurusan || 'Akuntansi' }}</p>
                    </div>
                    
                    <p>Semoga surat ini dapat memenuhi keperluan diatas.</p>
                    
                    <div class="mt-10">
                      <p class="text-right">Yogyakarta, {{ tanggalSurat }}</p>
                      <p class="text-right mt-4">Pustakawan,</p>
                    </div>
                  </div>
                  
                  <!-- TTD dengan posisi absolute -->
                  <div style="position: relative; min-height: 150px; margin-top: 10px;">
                    <div 
                      v-if="ttdImage" 
                      class="absolute" 
                      :style="{ 
                        left: ttdPositionX + '%', 
                        top: ttdPositionY + '%',
                        transform: 'translate(-50%, -50%)',
                        textAlign: 'center',
                        whiteSpace: 'nowrap',
                        zIndex: 10
                      }"
                    >
                      <img :src="ttdImage" class="h-14 object-contain" crossorigin="anonymous" />
                      <p class="text-xs font-bold mt-1">{{ petugasName || user.full_name }}</p>
                      <p class="text-[10px] text-gray-500">Pustakawan</p>
                    </div>
                    <div v-else class="text-red-500 text-xs italic text-center py-4">
                      (Tanda tangan belum diatur. Silakan atur di menu "Atur Tanda Tangan")
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="p-4 bg-white border-t border-gray-200 flex justify-end gap-3">
            <button @click="showSuratModal = false" class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 text-sm font-bold">Batal</button>
            <button @click="generateAndSendPDF" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg shadow text-sm font-bold">
              📎 Generate PDF & Kirim ke Mahasiswa
            </button>
          </div>
        </div>
      </div>

      <!-- MODAL TANDA TANGAN -->
      <div v-if="showTtdModal" class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-md flex flex-col overflow-hidden animate-fade-in">
          <div class="bg-indigo-950 text-white p-4 flex justify-between items-center">
            <div>
              <h3 class="font-bold text-lg">✍️ Atur Tanda Tangan Digital</h3>
              <p class="text-xs text-indigo-200 mt-1">Upload foto tanda tangan berformat PNG atau JPG</p>
            </div>
            <button @click="showTtdModal = false" class="text-white hover:text-red-400 font-bold text-xl">&times;</button>
          </div>
          
          <div class="p-6 bg-gray-50 flex flex-col items-center justify-center gap-4">
            <div class="w-full border-2 border-dashed border-gray-300 rounded-xl p-4 bg-white flex flex-col items-center justify-center min-h-[160px]">
              <div v-if="ttdPreview" class="flex flex-col items-center gap-2">
                <img :src="ttdPreview" class="max-h-28 object-contain rounded" alt="Preview Tanda Tangan" />
                <p class="text-[11px] text-gray-400 italic">Pratinjau tanda tangan pustakawan saat ini</p>
              </div>
              <div v-else class="text-center py-4">
                <span class="text-3xl">🖋️</span>
                <p class="text-sm text-gray-500 mt-2 font-semibold">Belum Ada Tanda Tangan</p>
                <p class="text-xs text-gray-400 mt-1">Silakan pilih file gambar untuk mulai mengupload</p>
              </div>
            </div>

            <div class="w-full">
              <label class="block text-xs font-bold text-gray-600 mb-2">Pilih File Tanda Tangan:</label>
              <input 
                type="file" 
                @change="uploadTtdToServer" 
                accept="image/png, image/jpeg, image/jpg"
                class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-bold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 border border-gray-200 rounded-lg p-1 bg-white cursor-pointer"
              />
            </div>
          </div>

          <div class="p-4 bg-white border-t border-gray-200 flex justify-between items-center">
            <button 
              v-if="ttdPreview"
              @click="hapusTtdDariServer" 
              class="px-4 py-2 bg-red-50 hover:bg-red-100 text-red-600 rounded-lg text-sm font-bold transition-all"
            >
              🗑️ Hapus TTD
            </button>
            <div v-else></div>
            <button @click="showTtdModal = false" class="px-4 py-2 bg-gray-800 hover:bg-gray-900 text-white rounded-lg text-sm font-bold transition-all">
              Selesai & Tutup
            </button>
          </div>
        </div>
      </div>
      
      <!-- MODAL TOLAK -->
      <div v-if="isTolakModalOpen" class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-md flex flex-col overflow-hidden">
          <div class="bg-red-950 text-white p-4 flex justify-between items-center">
            <div>
              <h3 class="font-bold text-lg">❌ Tolak Pengajuan Validasi</h3>
              <p class="text-xs text-red-200 mt-1">Mahasiswa: {{ tolakMhsName }}</p>
            </div>
            <button @click="isTolakModalOpen = false" class="text-white hover:text-red-400 font-bold text-xl">&times;</button>
          </div>
          
          <div class="p-6 bg-gray-50 flex flex-col gap-4">
            <div>
              <label class="block text-xs font-bold text-gray-600 mb-2">Alasan Penolakan (Wajib diisi):</label>
              <textarea 
                v-model="catatanTolak" 
                rows="4"
                class="w-full p-3 text-sm border border-gray-300 rounded-lg focus:ring-1 focus:ring-red-500 focus:border-red-500 outline-none resize-none bg-white"
                placeholder="Contoh: Berkas belum lengkap..."
              ></textarea>
            </div>
          </div>

          <div class="p-4 bg-white border-t border-gray-200 flex justify-end gap-3">
            <button @click="isTolakModalOpen = false" class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 text-sm font-bold">
              Batal
            </button>
            <button @click="confirmTolak" class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg shadow text-sm font-bold">
              Konfirmasi Tolak
            </button>
          </div>
        </div>
      </div>

      <!-- MODAL DETAIL LOG MAHASISWA -->
      <div v-if="showModal" class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-6xl flex flex-col max-h-[85vh] overflow-hidden">
          <div class="bg-gray-800 text-white p-4 flex justify-between items-center">
            <div>
              <h3 class="font-bold text-lg flex items-center gap-2">
                📋 Log Detail Mahasiswa
              </h3>
              <p class="text-xs text-gray-300 mt-1">{{ selectedMhs?.full_name }} ({{ selectedMhs?.nim }}) - {{ selectedMhs?.email }}</p>
            </div>
            <button @click="showModal = false" class="text-white hover:text-red-400 font-bold text-xl">&times;</button>
          </div>
          
          <div class="overflow-y-auto flex-1 p-5 bg-gray-50">
            <div v-if="selectedMhs?.history?.length > 1" class="flex gap-2 mb-5 border-b border-gray-200 pb-2 overflow-x-auto">
              <button 
                v-for="(item, idx) in selectedMhs.history" 
                :key="item.id"
                @click="selectedHistoryIndex = idx"
                :class="[
                  'px-4 py-2 rounded-lg text-xs font-bold transition whitespace-nowrap',
                  selectedHistoryIndex === idx 
                    ? 'bg-indigo-600 text-white shadow-md' 
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                ]"
              >
                Pengajuan #{{ idx + 1 }} - {{ formatDate(item.created_at) }}
                <span :class="{
                  'ml-2 px-1.5 py-0.5 rounded-full text-[9px]': true,
                  'bg-green-500 text-white': item.status === 'DISETUJUI',
                  'bg-red-500 text-white': item.status === 'DITOLAK',
                  'bg-orange-500 text-white': item.status === 'MENUNGGU'
                }">
                  {{ item.status }}
                </span>
              </button>
            </div>
            
            <div v-if="selectedHistoryItem" class="mb-6">
              <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5 mb-5">
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-xs text-gray-400 uppercase tracking-wide">Status Validasi</p>
                    <p class="text-xl font-bold" :class="{
                      'text-green-600': selectedHistoryItem.status === 'DISETUJUI',
                      'text-red-600': selectedHistoryItem.status === 'DITOLAK',
                      'text-orange-600': selectedHistoryItem.status === 'MENUNGGU'
                    }">
                      {{ selectedHistoryItem.status === 'DISETUJUI' ? '✅ DISETUJUI' : 
                         selectedHistoryItem.status === 'DITOLAK' ? '❌ DITOLAK' : 
                         '⏳ MENUNGGU VERIFIKASI' }}
                    </p>
                  </div>
                  <div class="text-right">
                    <p class="text-xs text-gray-400">Tanggal Pengajuan</p>
                    <p class="text-sm font-medium">{{ formatDate(selectedHistoryItem.created_at) }}</p>
                    <p v-if="selectedHistoryItem.validated_at" class="text-xs text-gray-500 mt-1">
                      Diverifikasi: {{ formatDate(selectedHistoryItem.validated_at) }}
                    </p>
                  </div>
                </div>
                <div v-if="selectedHistoryItem.catatan_perpus" class="mt-4 p-3 bg-gray-50 rounded-lg border-l-4 border-red-400">
                  <p class="text-xs font-bold text-gray-500">📝 Catatan Petugas:</p>
                  <p class="text-sm text-gray-700">{{ selectedHistoryItem.catatan_perpus }}</p>
                </div>
              </div>
              
              <h4 class="font-bold text-gray-700 mb-3 flex items-center gap-2">
                <span class="w-6 h-6 bg-indigo-100 rounded-lg flex items-center justify-center text-sm">📁</span>
                Semua Berkas Perpustakaan
                <span class="text-xs bg-gray-200 px-2 py-0.5 rounded-full">{{ getAllFilesCount(selectedHistoryItem) }} berkas</span>
              </h4>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div v-for="(fileInfo, fileKey) in getAllFilesList(selectedHistoryItem)" :key="fileKey" class="bg-white rounded-lg border border-gray-200 p-3 hover:shadow-md transition hover:border-indigo-300">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center">
                        <span class="text-indigo-600">📄</span>
                      </div>
                      <div>
                        <p class="text-sm font-medium text-gray-800 capitalize">{{ fileInfo.label }}</p>
                        <p class="text-[10px] text-gray-400">PDF Document</p>
                      </div>
                    </div>
                    <div class="flex gap-1">
                      <a 
                        :href="getFullImageUrl(fileInfo.url)" 
                        target="_blank" 
                        class="bg-indigo-600 text-white px-2 py-1 rounded text-[10px] font-bold hover:bg-indigo-700 transition"
                      >
                        📄 Buka PDF
                      </a>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-if="selectedHistoryItem.link_surat_pdf" class="mt-6">
                <h4 class="font-bold text-gray-700 mb-3 flex items-center gap-2">
                  <span class="w-6 h-6 bg-green-100 rounded-lg flex items-center justify-center text-sm">📜</span>
                  Surat Bebas Perpustakaan
                </h4>
                <div class="bg-green-50 rounded-lg border border-green-200 p-4">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-3">
                      <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                        <span class="text-green-600 text-xl">📜</span>
                      </div>
                      <div>
                        <p class="text-sm font-semibold text-green-800">Surat Keterangan Bebas Perpustakaan</p>
                        <p class="text-[10px] text-green-600">Dokumen Resmi</p>
                      </div>
                    </div>
                    <div class="flex gap-2">
                      <a 
                        :href="getFullImageUrl(selectedHistoryItem.link_surat_pdf)" 
                        target="_blank" 
                        class="bg-green-600 text-white px-4 py-2 rounded-lg text-xs font-bold hover:bg-green-700 transition flex items-center gap-1"
                      >
                        📄 Buka Surat PDF
                      </a>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-if="getAllFilesCount(selectedHistoryItem) === 0 && !selectedHistoryItem.link_surat_pdf" class="text-center py-10 text-gray-400">
                <span class="text-5xl block mb-3">📭</span>
                <p>Belum ada berkas yang diupload</p>
              </div>
            </div>
          </div>
          
          <div class="p-4 bg-gray-100 border-t border-gray-200 flex justify-end gap-3">
            <button 
              v-if="selectedHistoryItem?.status === 'MENUNGGU'"
              @click="showModal = false; bukaModalSurat(selectedHistoryItem)" 
              class="px-5 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-bold transition flex items-center gap-2"
            >
              ✔ Setujui & Buat Surat
            </button>
            <button 
              v-if="selectedHistoryItem?.status === 'MENUNGGU'"
              @click="showModal = false; openTolakModal(selectedHistoryItem.id, selectedMhs?.full_name)" 
              class="px-5 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm font-bold transition flex items-center gap-2"
            >
              ❌ Tolak
            </button>
            <button @click="showModal = false" class="px-5 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg text-sm font-bold transition">
              Tutup
            </button>
          </div>
        </div>
      </div>

      <!-- MODAL LIHAT SEMUA BERKAS -->
      <div v-if="showBerkasModal" class="fixed inset-0 bg-black/80 z-[100] flex items-center justify-center p-4" @click.self="showBerkasModal = false">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-5xl h-[85vh] flex flex-col overflow-hidden animate-fadeIn">
          <div class="bg-indigo-950 text-white p-4 flex justify-between items-center">
            <div>
              <h3 class="font-bold text-lg flex items-center gap-2">
                📂 Semua Berkas Perpustakaan - {{ selectedBerkasMhs?.full_name }}
              </h3>
              <p class="text-xs text-indigo-200">NIM: {{ selectedBerkasMhs?.nim }} | Email: {{ selectedBerkasMhs?.email }}</p>
            </div>
            <button @click="showBerkasModal = false" class="text-white hover:text-red-400 font-bold text-2xl">&times;</button>
          </div>
          
          <div class="flex-1 overflow-y-auto p-6 bg-gray-100">
            <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-6">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-xs text-gray-400">Status Validasi</p>
                  <p class="text-lg font-bold" :class="{
                    'text-green-600': selectedBerkasMhs?.status === 'DISETUJUI',
                    'text-red-600': selectedBerkasMhs?.status === 'DITOLAK',
                    'text-orange-600': selectedBerkasMhs?.status === 'MENUNGGU'
                  }">
                    {{ selectedBerkasMhs?.status === 'DISETUJUI' ? '✅ DISETUJUI' : 
                       selectedBerkasMhs?.status === 'DITOLAK' ? '❌ DITOLAK' : 
                       '⏳ MENUNGGU VERIFIKASI' }}
                  </p>
                </div>
                <div class="text-right">
                  <p class="text-xs text-gray-400">Tanggal Upload</p>
                  <p class="text-sm font-medium">{{ formatDate(selectedBerkasMhs?.created_at) }}</p>
                </div>
              </div>
              <div v-if="selectedBerkasMhs?.catatan_perpus" class="mt-3 p-2 bg-gray-50 rounded-lg text-xs text-gray-600">
                <span class="font-bold">Catatan:</span> {{ selectedBerkasMhs.catatan_perpus }}
              </div>
            </div>
            
            <h4 class="font-bold text-gray-700 mb-4 flex items-center gap-2">
              <span class="text-xl">📁</span> Semua Berkas
              <span class="text-xs bg-gray-200 px-2 py-0.5 rounded-full">{{ getAllFilesCount(selectedBerkasMhs) }} berkas</span>
            </h4>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="(fileInfo, fileKey) in getAllFilesList(selectedBerkasMhs)" :key="fileKey" class="bg-white rounded-xl border border-gray-200 p-4 hover:shadow-md transition hover:border-indigo-300">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center">
                      <span class="text-indigo-600 text-xl">📄</span>
                    </div>
                    <div>
                      <p class="text-sm font-semibold text-gray-800 capitalize">{{ fileInfo.label }}</p>
                      <p class="text-[10px] text-gray-400">PDF Document</p>
                    </div>
                  </div>
                  <div class="flex gap-2">
                    <a 
                      :href="getFullImageUrl(fileInfo.url)" 
                      target="_blank" 
                      class="bg-indigo-600 text-white px-3 py-1.5 rounded-lg text-xs font-bold hover:bg-indigo-700 transition flex items-center gap-1"
                    >
                      📄 Buka PDF
                    </a>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="selectedBerkasMhs?.link_surat_pdf" class="mt-6">
              <div class="bg-green-50 rounded-xl border border-green-200 p-4">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                      <span class="text-green-600 text-xl">📜</span>
                    </div>
                    <div>
                      <p class="text-sm font-semibold text-green-800">Surat Keterangan Bebas Perpustakaan</p>
                      <p class="text-[10px] text-green-600">Dokumen Resmi</p>
                    </div>
                  </div>
                  <div class="flex gap-2">
                    <a 
                      :href="getFullImageUrl(selectedBerkasMhs.link_surat_pdf)" 
                      target="_blank" 
                      class="bg-green-600 text-white px-4 py-2 rounded-lg text-xs font-bold hover:bg-green-700 transition flex items-center gap-1"
                    >
                      📄 Buka Surat PDF
                    </a>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="getAllFilesCount(selectedBerkasMhs) === 0 && !selectedBerkasMhs?.link_surat_pdf" class="text-center py-16 text-gray-400">
              <span class="text-5xl block mb-3">📭</span>
              <p class="text-sm">Belum ada berkas yang diupload</p>
            </div>
          </div>
          
          <div class="p-4 bg-white border-t border-gray-200 flex justify-end gap-3">
            <button @click="showBerkasModal = false" class="px-5 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg text-sm font-bold transition">
              Tutup
            </button>
            <button v-if="selectedBerkasMhs?.status === 'MENUNGGU'" @click="showBerkasModal = false; bukaModalSurat(selectedBerkasMhs)" class="px-5 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-bold transition">
              ✔ Setujui Sekarang
            </button>
          </div>
        </div>
      </div>
      
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const router = useRouter();
const user = ref({ full_name: '', role: '' });
const listMahasiswa = ref([]); 
const search = ref('');
const catatanTambahan = ref('');
const tanggalSurat = ref('');

// State UI untuk Tab dan Modal
const activeTab = ref('antrian');
const showModal = ref(false); 
const selectedMhs = ref(null);
const selectedHistoryIndex = ref(0);

// State Template Surat
const showTemplateModal = ref(false);
const templateSurat = ref(`SURAT BEBAS PINJAMAN PUSTAKA

Surat ini diberikan untuk permohonan mahasiswa yang sudah menyelesaikan semua biaya administrasi/denda :

Identitas pemohon surat bebas pinjam pustaka ini :

Nama : [NAMA]
No. Mahasiswa : [NIM]
Jurusan : [JURUSAN]

Semoga surat ini dapat memenuhi keperluan diatas.

[TANGGAL]
Pustakawan,

[PETUGAS]`);

// State Surat Bebas Perpus
const showSuratModal = ref(false);
const isiSurat = ref('');
const selectedMhsForSurat = ref(null);
const petugasName = ref('');

// State Posisi TTD - Default di kanan bawah (85%, 85%)
const ttdPositionX = ref(85);
const ttdPositionY = ref(85);

// State Atur Tanda Tangan
const showTtdModal = ref(false);
const ttdImage = ref(null);
const ttdPreview = ref(null);
const ttdUrl = ref(null);

// State Modal Tolak
const isTolakModalOpen = ref(false);
const tolakMhsId = ref(null);
const tolakMhsName = ref('');
const catatanTolak = ref('');

// State Pagination
const currentPageAntrian = ref(1);
const rowsPerPageAntrian = ref(10);
const currentPageRiwayat = ref(1);
const rowsPerPageRiwayat = ref(10);

// State Modal Berkas
const showBerkasModal = ref(false);
const selectedBerkasMhs = ref(null);
const logoUrl = ref('');
// ============================================================
// COMPUTED PROPERTIES
// ============================================================
const selectedHistoryItem = computed(() => {
  if (!selectedMhs.value?.history || selectedMhs.value.history.length === 0) return null;
  return selectedMhs.value.history[selectedHistoryIndex.value] || selectedMhs.value.history[0];
});

// ============================================================
// HELPER FUNCTIONS
// ============================================================
const getAllFilesCount = (item) => {
  if (!item) return 0;
  let count = item.file_abstrak ? 1 : 0;
  const fileFields = [
    'bagian_awal', 'bab1', 'bab2', 'bab3', 'bab4', 'bab5',
    'daftar_pustaka', 'lampiran', 'jurnal_publikasi', 'lampiran_cetak',
    'cek_plagiasi_jurnal'
  ];
  count += fileFields.filter(field => item[field]).length;
  return count;
};

const getAllFilesList = (item) => {
  if (!item) return [];
  const files = [];
  
  if (item.file_abstrak) {
    files.push({
      key: 'file_abstrak',
      url: item.file_abstrak,
      label: 'File Abstrak PDF'
    });
  }
  
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
      files.push({
        key: field.key,
        url: item[field.key],
        label: field.label
      });
    }
  });
  
  return files;
};

const formatDate = (dateString) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleDateString('id-ID', {
    day: 'numeric', month: 'long', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  });
};

const resetPagination = () => {
  currentPageAntrian.value = 1;
  currentPageRiwayat.value = 1;
};

const getFullImageUrl = (path) => {
  if (!path) return '';
  if (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('data:image')) {
    return path;
  }
  const backendBaseUrl = api.defaults.baseURL ? api.defaults.baseURL.replace(/\/api\/?$/, '') : 'http://localhost:8000';
  return `${backendBaseUrl}${path.startsWith('/') ? path : '/' + path}`;
};

// ============================================================
// GENERATE SURAT DARI TEMPLATE
// ============================================================
const getTanggalIndonesia = () => {
  const date = new Date();
  const bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'];
  return `${date.getDate()} ${bulan[date.getMonth()]} ${date.getFullYear()}`;
};

const generateSuratFromTemplate = (mhs) => {
  if (!mhs) return '';
  
  let surat = templateSurat.value;
  surat = surat.replace(/\[NAMA\]/g, mhs.full_name || '-');
  surat = surat.replace(/\[NIM\]/g, mhs.nim || '-');
  surat = surat.replace(/\[JURUSAN\]/g, mhs.jurusan || 'Akuntansi');
  surat = surat.replace(/\[TANGGAL\]/g, tanggalSurat.value);
  surat = surat.replace(/\[PETUGAS\]/g, petugasName.value || user.value.full_name || 'Petugas Perpustakaan');
  
  return surat;
};

// ============================================================
// GENERATE DAN KIRIM PDF (BACKEND ONLY)
// ============================================================
const generateAndSendPDF = async () => {
  if (!selectedMhsForSurat.value) {
    alert('Error: Tidak ada mahasiswa yang dipilih!');
    return;
  }
  
  console.log('📤 Data mahasiswa untuk PDF:', selectedMhsForSurat.value);
  
  const loadingToast = document.createElement('div');
  loadingToast.className = 'fixed bottom-4 right-4 bg-indigo-600 text-white px-4 py-2 rounded-lg shadow-lg z-50';
  loadingToast.innerHTML = '⏳ Sedang memproses surat...';
  document.body.appendChild(loadingToast);
  
  try {
    // Kirim data ke backend - PASTIKAN DATA LENGKAP
    const formData = new FormData();
    formData.append('pengajuan_id', selectedMhsForSurat.value.id || '');
    formData.append('nim', selectedMhsForSurat.value.nim || '');
    formData.append('email', selectedMhsForSurat.value.email || '');
    
    // ========== PERBAIKAN: Ambil data dari selectedMhsForSurat ==========
    // Coba ambil dari berbagai kemungkinan sumber data
    let namaMahasiswa = '';
    let prodiMahasiswa = '';
    
    if (selectedMhsForSurat.value.full_name) {
      namaMahasiswa = selectedMhsForSurat.value.full_name;
    } else if (selectedMhsForSurat.value.mahasiswa_nama) {
      namaMahasiswa = selectedMhsForSurat.value.mahasiswa_nama;
    } else if (selectedMhsForSurat.value.nama) {
      namaMahasiswa = selectedMhsForSurat.value.nama;
    } else {
      namaMahasiswa = selectedMhsForSurat.value.nim || 'Mahasiswa';
    }
    
    if (selectedMhsForSurat.value.jurusan) {
      prodiMahasiswa = selectedMhsForSurat.value.jurusan;
    } else if (selectedMhsForSurat.value.program_studi) {
      prodiMahasiswa = selectedMhsForSurat.value.program_studi;
    } else if (selectedMhsForSurat.value.prodi) {
      prodiMahasiswa = selectedMhsForSurat.value.prodi;
    } else {
      prodiMahasiswa = 'Akuntansi';
    }
    
    formData.append('full_name', namaMahasiswa);
    formData.append('prodi', prodiMahasiswa);
    formData.append('catatan_perpus', catatanTambahan.value || '');
    formData.append('ttd_position_x', String(ttdPositionX.value));
    formData.append('ttd_position_y', String(ttdPositionY.value));
    
    console.log('📝 Data yang dikirim:', {
      nim: selectedMhsForSurat.value.nim,
      full_name: namaMahasiswa,
      prodi: prodiMahasiswa,
      catatan: catatanTambahan.value
    });
    
    // Kirim gambar TTD jika ada
    if (ttdImage.value && ttdImage.value.startsWith('data:image')) {
      formData.append('ttd_base64', ttdImage.value);
    } else if (ttdUrl.value) {
      formData.append('ttd_petugas', ttdUrl.value);
    }
    
    // Panggil API backend untuk generate PDF
    const response = await api.post('generate-surat-pdf/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 60000
    });
    
    loadingToast.remove();
    
    if (response.data.success) {
      alert(`✅ Surat PDF berhasil dibuat untuk ${namaMahasiswa}!\n📄 Surat tersedia di dashboard mahasiswa.`);
      showSuratModal.value = false;
      catatanTambahan.value = '';
      await fetchData();
    } else {
      alert('❌ Gagal: ' + (response.data.error || 'Unknown error'));
    }
  } catch (err) {
    loadingToast.remove();
    console.error('Error detail:', err);
    alert(`❌ Gagal generate PDF: ${err.response?.data?.error || err.message}`);
  }
};

// ============================================================
// FITUR TEMPLATE SURAT
// ============================================================
const loadTemplateFromStorage = () => {
  const savedTemplate = localStorage.getItem('template_surat_perpus');
  if (savedTemplate) {
    templateSurat.value = savedTemplate;
  }
};

const openTemplateModal = () => {
  showTemplateModal.value = true;
};

const simpanTemplateSurat = () => {
  localStorage.setItem('template_surat_perpus', templateSurat.value);
  alert('Template surat berhasil disimpan!');
  showTemplateModal.value = false;
};
const fetchLogo = async () => {
  try {
    const response = await api.get('get-logo/');
    if (response.data.success && response.data.logo_url) {
      logoUrl.value = response.data.logo_url;
      console.log('✅ Logo loaded from backend');
    } else {
      logoUrl.value = '/stie-sbilogo.png'; // fallback
    }
  } catch (err) {
    console.error('Failed to load logo:', err);
    logoUrl.value = '/stie-sbilogo.png'; // fallback
  }
};

const loadTtdFromServer = async () => {
  try {
    const response = await api.get('ttd-perpus/');
    console.log('📥 Response TTD dari server:', response.data);
    
    if (response.data.ttd_url) {
      ttdUrl.value = response.data.ttd_url;
      // Simpan path relatif untuk dikirim ke backend
      const fullUrl = getFullImageUrl(response.data.ttd_url);
      ttdImage.value = fullUrl;
      ttdPreview.value = fullUrl;
      console.log('✅ TTD loaded dari server, path:', ttdUrl.value);
    } else {
      console.log('⚠️ Tidak ada TTD di server');
      const savedTtd = localStorage.getItem('ttd_perpus');
      if (savedTtd) {
        ttdImage.value = savedTtd;
        ttdPreview.value = savedTtd;
        console.log('✅ TTD loaded dari localStorage');
      }
    }
  } catch (err) {
    console.error('❌ Gagal load TTD:', err);
    const savedTtd = localStorage.getItem('ttd_perpus');
    if (savedTtd) {
      ttdImage.value = savedTtd;
      ttdPreview.value = savedTtd;
      console.log('✅ TTD loaded dari localStorage (fallback)');
    }
  }
};

const openTtdModal = () => {
  showTtdModal.value = true;
};

const uploadTtdToServer = async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  
  if (!file.type.match('image/png') && !file.type.match('image/jpeg')) {
    alert('Hanya file berformat PNG atau JPG yang diperbolehkan!');
    return;
  }
  
  const localPreviewUrl = URL.createObjectURL(file);
  ttdPreview.value = localPreviewUrl;
  ttdImage.value = localPreviewUrl;
  
  const formData = new FormData();
  formData.append('ttd', file);
  
  try {
    const response = await api.post('upload-ttd/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    
    console.log('📥 Response upload TTD:', response.data);
    
    if (response.data.ttd_url) {
      ttdUrl.value = response.data.ttd_url;
      const fullUrl = getFullImageUrl(response.data.ttd_url);
      ttdImage.value = fullUrl;
      ttdPreview.value = fullUrl;
      console.log('✅ TTD tersimpan di server, path:', ttdUrl.value);
      alert('Tanda tangan berhasil disimpan ke server!');
      showTtdModal.value = false;
    } else {
      throw new Error('No ttd_url in response');
    }
  } catch (err) {
    console.error('❌ Upload gagal:', err);
    localStorage.setItem('ttd_perpus', localPreviewUrl);
    alert('Tanda tangan disimpan di browser (local fallback). Server error: ' + (err.response?.data?.error || err.message));
    showTtdModal.value = false;
  }
};

const hapusTtdDariServer = async () => {
  try {
    await api.delete('ttd-perpus/');
    ttdImage.value = null;
    ttdPreview.value = null;
    ttdUrl.value = null;
    localStorage.removeItem('ttd_perpus');
    alert('Tanda tangan berhasil dihapus dari server!');
    showTtdModal.value = false;
  } catch (err) {
    localStorage.removeItem('ttd_perpus');
    ttdImage.value = null;
    ttdPreview.value = null;
    alert('Tanda tangan dihapus dari browser (fallback).');
    showTtdModal.value = false;
  }
};

// ============================================================
// FITUR BUKA MODAL SURAT
// ============================================================
const resetKeTemplate = () => {
  if (selectedMhsForSurat.value) {
    isiSurat.value = generateSuratFromTemplate(selectedMhsForSurat.value);
  }
};

const bukaModalSurat = (mhs) => {
  selectedMhsForSurat.value = mhs;
  petugasName.value = user.value.full_name || '';
  tanggalSurat.value = getTanggalIndonesia();
  
  if (mhs.status === 'DISETUJUI' && mhs.catatan_perpus) {
    isiSurat.value = mhs.catatan_perpus;
  } else {
    isiSurat.value = generateSuratFromTemplate(mhs);
  }
  
  if (mhs.ttd_position_x) ttdPositionX.value = mhs.ttd_position_x;
  if (mhs.ttd_position_y) ttdPositionY.value = mhs.ttd_position_y;
  
  showSuratModal.value = true;
};

// ============================================================
// FITUR MODAL BERKAS
// ============================================================
const openBerkasModal = (mhs) => {
  selectedBerkasMhs.value = mhs;
  showBerkasModal.value = true;
};

// ============================================================
// LOGIKA TOLAK DAN DETAIL LAINNYA
// ============================================================
const openTolakModal = (id, nama) => {
  tolakMhsId.value = id;
  tolakMhsName.value = nama;
  catatanTolak.value = '';
  isTolakModalOpen.value = true;
};

const confirmTolak = async () => {
  if (!catatanTolak.value.trim()) {
    alert("Alasan penolakan wajib diisi!");
    return;
  }
  try {
    console.log('📤 Menolak berkas ID:', tolakMhsId.value);
    console.log('📝 Catatan:', catatanTolak.value);
    
    // Gunakan endpoint verifikasi yang baru (dengan notifikasi)
    const response = await api.post(`bebas-perpus/${tolakMhsId.value}/verifikasi/`, {
      status: 'DITOLAK',
      catatan_perpus: catatanTolak.value
    });
    
    console.log('✅ Response:', response.data);
    
    if (response.data.success) {
      alert(`✅ Berkas ditolak! Notifikasi telah dikirim ke mahasiswa.\n\nCatatan: ${catatanTolak.value}`);
      isTolakModalOpen.value = false;
      catatanTolak.value = '';
      await fetchData(); // Refresh data
    } else {
      alert('❌ Gagal: ' + (response.data.error || 'Unknown error'));
    }
  } catch (err) {
    console.error('❌ Error detail:', err);
    alert(`Gagal update status: ${err.response?.data?.error || err.message}`);
  }
};
const setujuiBerkas = async (mhs) => {
  if (!confirm(`Setujui berkas mahasiswa ${mhs.full_name || mhs.nim}?`)) {
    return;
  }
  
  try {
    console.log('📤 Menyetujui berkas ID:', mhs.id);
    
    const response = await api.post(`bebas-perpus/${mhs.id}/verifikasi/`, {
      status: 'DISETUJUI',
      catatan_perpus: ''
    });
    
    console.log('✅ Response:', response.data);
    
    if (response.data.success) {
      alert(`✅ Berkas disetujui! Notifikasi telah dikirim ke mahasiswa.`);
      await fetchData(); // Refresh data
      // Buka modal surat untuk generate PDF
      bukaModalSurat(mhs);
    } else {
      alert('❌ Gagal: ' + (response.data.error || 'Unknown error'));
    }
  } catch (err) {
    console.error('❌ Error detail:', err);
    alert(`Gagal menyetujui: ${err.response?.data?.error || err.message}`);
  }
};
const bukaModalDetail = (mahasiswaGroup) => {
  selectedMhs.value = mahasiswaGroup;
  selectedHistoryIndex.value = 0;
  showModal.value = true;
};

// ============================================================
// FETCH DATA & COMPUTED PROPERTIES
// ============================================================
const fetchData = async () => {
  try {
    const [resUser, resPerpus] = await Promise.all([
      api.get('users/me/'),
      api.get('bebas-perpus/')
    ]);
    
    user.value = resUser.data;
    petugasName.value = user.value.full_name || '';
    
    listMahasiswa.value = resPerpus.data.map(m => ({
      ...m,
      jurusan: m.jurusan || 'Akuntansi'
    }));
    
    listMahasiswa.value.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  } catch (err) {
    console.error('Gagal load data:', err);
  }
};

const countStatus = (status) => {
  return listMahasiswa.value.filter(m => m.status === status).length;
};

const antrianCount = computed(() => {
  return listMahasiswa.value.filter(m => m.status === 'MENUNGGU').length;
});

const filteredAntrian = computed(() => {
  return listMahasiswa.value.filter(m => {
    const isMenunggu = m.status === 'MENUNGGU';
    const nama = (m.full_name || '').toLowerCase();
    const nim = (m.nim || '').toLowerCase();
    const query = search.value.toLowerCase();
    return isMenunggu && (nama.includes(query) || nim.includes(query));
  });
});

const totalPagesAntrian = computed(() => Math.ceil(filteredAntrian.value.length / rowsPerPageAntrian.value));
const paginatedAntrian = computed(() => {
  const start = (currentPageAntrian.value - 1) * rowsPerPageAntrian.value;
  return filteredAntrian.value.slice(start, start + rowsPerPageAntrian.value);
});

const filteredRiwayat = computed(() => {
  const groups = {};
  listMahasiswa.value.forEach(item => {
    const nim = item.nim || 'NIM_KOSONG';
    if (!groups[nim]) {
      groups[nim] = {
        nim: nim,
        full_name: item.full_name || 'NAMA TIDAK DITEMUKAN',
        email: item.email || '',
        last_updated: item.updated_at || item.created_at,
        history: []
      };
    }
    groups[nim].history.push(item);
    const itemDate = item.updated_at || item.created_at;
    if (itemDate && (!groups[nim].last_updated || new Date(itemDate) > new Date(groups[nim].last_updated))) {
      groups[nim].last_updated = itemDate;
    }
  });

  Object.values(groups).forEach(group => {
    group.history.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  });

  const riwayatArray = Object.values(groups).sort((a, b) => new Date(b.last_updated) - new Date(a.last_updated));
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

const prevPageAntrian = () => { if (currentPageAntrian.value > 1) currentPageAntrian.value--; };
const nextPageAntrian = () => { if (currentPageAntrian.value < totalPagesAntrian.value) currentPageAntrian.value++; };
const prevPageRiwayat = () => { if (currentPageRiwayat.value > 1) currentPageRiwayat.value--; };
const nextPageRiwayat = () => { if (currentPageRiwayat.value < totalPagesRiwayat.value) currentPageRiwayat.value++; };

const handleLogout = () => {
  localStorage.clear();
  router.replace({ name: 'login' });
};

// ============================================================
// WATCHERS
// ============================================================
watch(search, () => { resetPagination(); });
watch(rowsPerPageAntrian, () => { currentPageAntrian.value = 1; });
watch(rowsPerPageRiwayat, () => { currentPageRiwayat.value = 1; });

// ============================================================
// ON MOUNTED
// ============================================================
onMounted(() => {
  fetchData();
  loadTemplateFromStorage();
  loadTtdFromServer();
  fetchLogo(); // ← TAMBAHKAN INI
  tanggalSurat.value = getTanggalIndonesia();
});
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
details summary {
  list-style: none;
  cursor: pointer;
}
details summary::-webkit-details-marker {
  display: none;
}
#suratPreview {
  font-family: 'Times New Roman', Times, serif;
}
#suratPreview h1, #suratPreview h2, #suratPreview h3 {
  text-align: center;
}
.animate-fadeIn {
  animation: fadeIn 0.3s ease-in-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>