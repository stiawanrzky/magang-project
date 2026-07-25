<template>
  <div class="min-h-screen bg-gray-50 flex flex-col md:flex-row">
    <!-- SIDEBAR -->
    <aside class="w-64 bg-slate-900 text-white hidden md:flex flex-col shadow-xl">
      <div class="p-6 text-xl font-bold border-b border-indigo-800 flex items-center gap-3">
        <span class="bg-white p-1 rounded text-indigo-900 text-sm">🎓</span>
        Sistem Yudisium
      </div>

      <nav class="flex-1 p-4 space-y-2">
        <button @click="currentView = 'dashboard'" :class="['w-full text-left p-3 rounded-lg flex items-center gap-3 transition', currentView === 'dashboard' ? 'bg-indigo-700 font-bold shadow-inner' : 'hover:bg-indigo-800']">
          📊 Dashboard Upload
        </button>
        
        <button @click="currentView = 'riwayat'" :class="['w-full text-left p-3 rounded-lg flex items-center gap-3 transition', currentView === 'riwayat' ? 'bg-indigo-700 font-bold shadow-inner' : 'hover:bg-indigo-800']">
          📜 Riwayat & Catatan
        </button>

        <button @click="bukaModalProfil" class="w-full text-left p-3 rounded-lg flex items-center gap-3 transition hover:bg-indigo-800">
          👤 Profil Saya
        </button>

        <div class="relative">
          <button @click="toggleNotifikasi" class="w-full text-left p-3 rounded-lg flex items-center gap-3 transition hover:bg-indigo-800 relative">
            🔔 Notifikasi
            <span v-if="unreadCount > 0" class="absolute right-3 top-1/2 -translate-y-1/2 bg-red-500 text-white text-[10px] font-bold rounded-full min-w-[20px] h-5 px-1 flex items-center justify-center">
              {{ unreadCount > 99 ? '99+' : unreadCount }}
            </span>
          </button>
          
          <!-- DROPDOWN NOTIFIKASI -->
          <div v-if="showNotifikasiDropdown" class="absolute left-0 mt-2 w-80 bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden z-50">
            <div class="p-3 border-b border-gray-100 flex justify-between items-center bg-indigo-50">
              <h3 class="font-bold text-sm text-indigo-800">Notifikasi</h3>
              <button @click="bacaSemuaNotifikasi" class="text-xs text-indigo-600 hover:text-indigo-800">Tandai semua dibaca</button>
            </div>
            
            <div class="max-h-96 overflow-y-auto">
              <div v-for="notif in notifikasiList" :key="notif.id" 
                   @click="bukaNotifikasi(notif)"
                   :class="['p-3 border-b border-gray-100 cursor-pointer hover:bg-gray-50 transition', !notif.is_read ? 'bg-indigo-50' : '']">
                <div class="flex items-start gap-2">
                  <span class="text-lg">{{ getIconNotif(notif.tipe) }}</span>
                  <div class="flex-1">
                    <p class="text-xs font-semibold" :class="!notif.is_read ? 'text-indigo-700' : 'text-gray-700'">
                      {{ notif.judul }}
                    </p>
                    <p class="text-[11px] text-gray-500 mt-1 line-clamp-2">{{ notif.pesan }}</p>
                    <p class="text-[10px] text-gray-400 mt-1">{{ formatWaktu(notif.created_at) }}</p>
                  </div>
                  <div v-if="!notif.is_read" class="w-2 h-2 bg-indigo-500 rounded-full"></div>
                </div>
              </div>
              
              <div v-if="notifikasiList.length === 0" class="p-6 text-center text-gray-400 text-sm">
                Tidak ada notifikasi
              </div>
            </div>
            
            <div class="p-2 border-t border-gray-100 text-center">
              <button @click="lihatSemuaNotifikasi" class="text-xs text-indigo-600 hover:text-indigo-800">Lihat semua notifikasi</button>
            </div>
          </div>
        </div>

        <button @click="bukaPanduanModal" class="w-full text-left p-3 rounded-lg flex items-center gap-3 transition hover:bg-indigo-800">
          📖 Panduan Berkas
        </button>
      </nav>

      <div class="p-4 border-t border-indigo-800">
        <button @click="logout" class="w-full py-2 bg-red-500 hover:bg-red-600 rounded-lg text-sm font-bold transition">
          🚪 Keluar
        </button>
      </div>
    </aside>

    <main class="flex-1 p-6 md:p-10 overflow-y-auto relative">
      <!-- LOADING & ERROR STATE -->
      <div v-if="loading && !user.full_name" class="flex flex-col items-center justify-center py-20 text-gray-500">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600 mb-4"></div>
        Memuat data sistem...
      </div>

      <div v-else-if="error" class="bg-red-100 text-red-600 p-6 rounded-2xl border border-red-200">
        <h3 class="font-bold">Gagal Mengambil Data</h3>
        <p class="text-sm">Server tidak merespon atau sesi Anda telah berakhir.</p>
        <button @click="fetchStatus" class="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-bold">Coba Lagi</button>
      </div>

      <div v-else>
        <!-- DASHBOARD VIEW -->
        <div v-if="currentView === 'dashboard'">
          <!-- Tombol Refresh -->
          <div class="flex justify-end mb-4">
            <button @click="refreshAllData" class="bg-indigo-500 hover:bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm flex items-center gap-2 shadow-md">
              <span class="animate-spin" v-if="loadingRefresh">⟳</span>
              <span v-else>🔄</span>
              Refresh Status
            </button>
          </div>

          <header class="mb-8">
            <h1 class="text-2xl font-extrabold text-gray-800">
              Halo, {{ user.full_name || 'Mahasiswa' }}
            </h1>
            <p class="text-gray-500 mt-1">Status Prodi: <span class="font-bold text-indigo-600">{{ user.prodi || 'Pilih Prodi di Profil' }}</span></p>
          </header>

          <!-- Cards Status -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5 mb-8">
            <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition">
              <div class="p-4 flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                    <span class="text-blue-600 text-lg">📚</span>
                  </div>
                  <div>
                    <p class="text-xs text-gray-400 font-medium uppercase tracking-wide">Transkrip</p>
                    <p class="text-xl font-bold" :class="{
                      'text-green-600': verifikasi.transkrip.status === 'DISETUJUI',
                      'text-orange-600': verifikasi.transkrip.status === 'MENUNGGU',
                      'text-red-600': verifikasi.transkrip.status === 'DITOLAK'
                    }">{{ verifikasi.transkrip.status }}</p>
                  </div>
                </div>
                <div :class="indicatorClass(verifikasi.transkrip.status)" class="w-2 h-2 rounded-full"></div>
              </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition">
              <div class="p-4 flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-lg bg-purple-100 flex items-center justify-center">
                    <span class="text-purple-600 text-lg">📖</span>
                  </div>
                  <div>
                    <p class="text-xs text-gray-400 font-medium uppercase tracking-wide">Bebas Perpustakaan</p>
                    <p class="text-xl font-bold" :class="{
                      'text-green-600': verifikasi.perpus.status === 'DISETUJUI',
                      'text-orange-600': verifikasi.perpus.status === 'MENUNGGU',
                      'text-red-600': verifikasi.perpus.status === 'DITOLAK'
                    }">{{ verifikasi.perpus.status }}</p>
                  </div>
                </div>
                <div :class="indicatorClass(verifikasi.perpus.status)" class="w-2 h-2 rounded-full"></div>
              </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition">
              <div class="p-4 flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-lg bg-rose-100 flex items-center justify-center">
                    <span class="text-rose-600 text-lg">🎓</span>
                  </div>
                  <div>
                    <p class="text-xs text-gray-400 font-medium uppercase tracking-wide">Akademik</p>
                    <p class="text-xl font-bold" :class="{
                      'text-green-600': verifikasi.akademik.status === 'DISETUJUI',
                      'text-orange-600': verifikasi.akademik.status === 'MENUNGGU',
                      'text-red-600': verifikasi.akademik.status === 'DITOLAK'
                    }">{{ verifikasi.akademik.status }}</p>
                  </div>
                </div>
                <div :class="indicatorClass(verifikasi.akademik.status)" class="w-2 h-2 rounded-full"></div>
              </div>
            </div>
          </div>

          <!-- Progress Bar - MENGGUNAKAN statusAkhirDisplay -->
          <div class="bg-gradient-to-r from-indigo-600 to-indigo-700 rounded-xl p-6 mb-10 text-white shadow-lg">
            <div class="flex justify-between items-start mb-4">
              <div>
                <p class="text-xs uppercase tracking-wider opacity-80 font-semibold">Status Akhir Kelulusan</p>
                <h2 class="text-2xl font-bold mt-1">
                  <span v-if="statusAkhirDisplay === 'LULUS'" class="text-green-300 flex items-center gap-2"> LULUS</span>
                  <span v-else-if="statusAkhirDisplay === 'MENUNGGU_VERIFIKASI'" class="text-yellow-300 flex items-center gap-2"> MENUNGGU VERIFIKASI BAAK</span>
                  <span v-else-if="statusAkhirDisplay === 'SILAKAN_DAFTAR'" class="text-blue-300 flex items-center gap-2"> SILAKAN DAFTAR YUDISIUM</span>
                  <span v-else-if="statusAkhirDisplay === 'PENDAFTARAN_DITOLAK'" class="text-red-300 flex items-center gap-2"> PENDAFTARAN DITOLAK</span>
                  <span v-else-if="statusAkhirDisplay === 'PROSES'" class="flex items-center gap-2"> PROSES PENGISIAN BERKAS</span>
                  <span v-else>{{ statusAkhirDisplay }}</span>
                </h2>
              </div>
              <div class="text-right">
                <p class="text-2xl font-bold">{{ progress }}%</p>
                <p class="text-xs opacity-80">{{ totalSelesai }} dari 3 Selesai</p>
              </div>
            </div>
            <div class="w-full bg-indigo-400/30 h-2 rounded-full overflow-hidden">
              <div class="bg-white h-full rounded-full transition-all duration-700" :style="{ width: progress + '%' }"></div>
            </div>
            
            <!-- Pesan informatif -->
            <div v-if="progress === 100 && statusAkhirDisplay !== 'LULUS'" class="mt-4 p-3 bg-white/20 rounded-lg text-sm">
              <p v-if="!statusPendaftaran" class="flex items-center gap-2">
                ⚠️ <strong>Semua berkas sudah disetujui!</strong> Silakan klik tombol "Daftar Yudisium Sekarang" di bawah untuk melanjutkan.
              </p>
              <p v-else-if="statusPendaftaran === 'MENUNGGU'" class="flex items-center gap-2">
                ⏳ <strong>Pendaftaran yudisium sedang menunggu verifikasi dari BAAK.</strong> Mohon bersabar.
              </p>
              <p v-else-if="statusPendaftaran === 'DITOLAK'" class="flex items-center gap-2">
                ❌ <strong>Pendaftaran yudisium ditolak.</strong> Silakan cek catatan BAAK dan hubungi bagian akademik.
              </p>
            </div>
          </div>

          <!-- Tombol Daftar Yudisium -->
          <div v-if="bisaDaftarYudisium" class="mt-6">
            <button @click="bukaModalPendaftaran" 
                    class="w-full md:w-auto bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-xl shadow-lg transition flex items-center justify-center gap-3 text-lg">
              <span class="text-2xl">📝</span>
              Daftar Yudisium Sekarang
              <span class="bg-green-500 text-white text-xs px-2 py-1 rounded-full">Semua Berkas Selesai!</span>
            </button>
          </div>

          <!-- Tampilkan status pendaftaran jika sudah daftar -->
          <div v-else-if="statusPendaftaran" class="mt-6 bg-white rounded-xl shadow-sm border p-5">
            <div class="flex items-center gap-3">
              <span class="text-2xl">📋</span>
              <div>
                <h3 class="font-bold text-gray-800">Status Pendaftaran Yudisium</h3>
                <p class="text-sm" :class="{
                  'text-green-600': statusPendaftaran === 'DISETUJUI',
                  'text-orange-600': statusPendaftaran === 'MENUNGGU',
                  'text-red-600': statusPendaftaran === 'DITOLAK'
                }">
                  {{ statusPendaftaran === 'DISETUJUI' ? '✅ Telah Diverifikasi BAAK' : 
                     statusPendaftaran === 'MENUNGGU' ? '⏳ Menunggu Verifikasi BAAK' : 
                     statusPendaftaran === 'DITOLAK' ? '❌ Ditolak - Silakan hubungi BAAK' : statusPendaftaran }}
                </p>
                <p v-if="catatanBAAK" class="text-xs text-gray-600 mt-2 p-2 bg-gray-100 rounded-lg">
                  <span class="font-semibold">📝 Catatan BAAK:</span> {{ catatanBAAK }}
                </p>
                <p v-if="tanggalDaftar" class="text-xs text-gray-400 mt-1">📅 Tanggal Daftar: {{ formatTanggal(tanggalDaftar) }}</p>
                <p v-if="tanggalVerifikasi" class="text-xs text-gray-400 mt-1">✅ Tanggal Verifikasi: {{ formatTanggal(tanggalVerifikasi) }}</p>
              </div>
            </div>
          </div>

          <!-- Upload Sections -->
          <section class="mt-8">
            <h2 class="text-lg font-bold text-gray-800 mb-5 flex items-center gap-2">
              <span class="w-6 h-6 bg-indigo-100 rounded-lg flex items-center justify-center text-xs">📤</span>
              Kirim Berkas Persyaratan
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
              <!-- Bagian BAAK -->
              <div class="bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition overflow-hidden">
                <div class="p-4 border-b border-gray-50 bg-blue-50/30">
                  <p class="text-xs font-bold text-blue-600 uppercase tracking-wide">📋 Bagian BAAK</p>
                </div>
                <div class="p-4">
                  <p class="text-sm font-medium text-gray-700 mb-3">Data Transkrip Nilai</p>
                  <div v-if="!verifikasi.transkrip.sudah_upload || verifikasi.transkrip.status === 'DITOLAK'">
                    <button @click="mulaiIsiTranskrip" class="w-full py-2.5 bg-blue-50 text-blue-700 font-semibold rounded-lg hover:bg-blue-100 transition text-sm flex items-center justify-center gap-2">
                      📝 Isi Nilai Transkrip
                    </button>
                  </div>
                  <div v-else class="space-y-3">
                    <div class="flex items-center gap-2 p-2 bg-green-50 rounded-lg">
                      <span class="text-green-600">✅</span>
                      <span class="text-xs font-medium text-green-700">Berkas Terkirim</span>
                    </div>
                    <button @click="mulaiIsiTranskrip" class="w-full py-2 bg-amber-50 text-amber-700 font-semibold rounded-lg hover:bg-amber-100 transition text-sm flex items-center justify-center gap-2">
                      ✏️ Ubah Data Transkrip
                    </button>
                  </div>
                </div>
              </div>

              <!-- Bagian Perpustakaan -->
              <div class="bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition overflow-hidden">
                <div class="p-4 border-b border-gray-50 bg-purple-50/30">
                  <p class="text-xs font-bold text-purple-600 uppercase tracking-wide">📖 Bagian Perpustakaan</p>
                </div>
                <div class="p-4">
                  <p class="text-sm font-medium text-gray-700 mb-3">Upload PDF + Abstrak</p>
                  <div v-if="!verifikasi.perpus.sudah_upload || verifikasi.perpus.status === 'DITOLAK'">
                    <button @click="bukaModalPerpus" class="w-full py-2.5 bg-purple-50 text-purple-700 font-semibold rounded-lg hover:bg-purple-100 transition text-sm flex items-center justify-center gap-2">
                      📄 Upload Berkas Perpustakaan
                    </button>
                  </div>
                  <div v-else class="space-y-3">
                    <div class="flex items-center gap-2 p-2 bg-green-50 rounded-lg">
                      <span class="text-green-600">✅</span>
                      <span class="text-xs font-medium text-green-700">Berkas Terkirim</span>
                    </div>
                    <button v-if="verifikasi.perpus.status === 'DISETUJUI'" @click="showSuratPerpusModal = true" class="w-full py-2 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 transition text-sm flex items-center justify-center gap-2 shadow-sm">
                      📑 Lihat Surat Bebas Perpus
                    </button>
                    <button v-else @click="bukaModalPerpus" class="w-full py-2 bg-amber-50 text-amber-700 font-semibold rounded-lg hover:bg-amber-100 transition text-sm flex items-center justify-center gap-2">
                      ✏️ Ubah Berkas Perpustakaan
                    </button>
                  </div>
                </div>
              </div>

              <!-- Bagian Akademik -->
              <div class="bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition overflow-hidden">
                <div class="p-4 border-b border-gray-50 bg-rose-50/30">
                  <p class="text-xs font-bold text-rose-600 uppercase tracking-wide">🎓 Bagian Akademik</p>
                </div>
                <div class="p-4">
                  <p class="text-sm font-medium text-gray-700 mb-3">Form Pendaftaran (4 Berkas)</p>
                  <div v-if="!verifikasi.akademik.sudah_upload || verifikasi.akademik.status === 'DITOLAK'">
                    <button @click="bukaModalAkademik" class="w-full py-2.5 bg-rose-50 text-rose-700 font-semibold rounded-lg hover:bg-rose-100 transition text-sm flex items-center justify-center gap-2">
                      📎 Isi Form Akademik
                    </button>
                  </div>
                  <div v-else class="space-y-3">
                    <div class="flex items-center gap-2 p-2 bg-green-50 rounded-lg">
                      <span class="text-green-600">✅</span>
                      <span class="text-xs font-medium text-green-700">Berkas Terkirim</span>
                    </div>
                    <button @click="bukaModalAkademik" class="w-full py-2 bg-amber-50 text-amber-700 font-semibold rounded-lg hover:bg-amber-100 transition text-sm flex items-center justify-center gap-2">
                      ✏️ Cek / Ubah Form
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- RIWAYAT VIEW -->
        <div v-else-if="currentView === 'riwayat'" class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
          <div class="p-5 border-b border-gray-100 bg-gray-50">
            <h2 class="font-bold text-gray-800">Detail Riwayat & Catatan Petugas</h2>
            <p class="text-xs text-gray-500 mt-0.5">Cek hasil validasi terbaru dan catatan revisi dari setiap bagian.</p>
          </div>
          
          <div class="overflow-x-auto">
            <table class="w-full text-left">
              <thead class="bg-gray-50 text-gray-400 text-[10px] uppercase font-semibold border-b border-gray-100">
                <tr>
                  <th class="px-5 py-3">Bagian / Berkas</th>
                  <th class="px-5 py-3 text-center w-28">Status</th>
                  <th class="px-5 py-3">Catatan Petugas</th>
                  <th class="px-5 py-3 text-center w-28">Aksi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 text-sm">
                <!-- Transkrip -->
                <tr class="hover:bg-slate-50 transition">
                  <td class="px-5 py-4">
                    <p class="font-semibold text-gray-800">📋 Bagian BAAK</p>
                    <p class="text-[10px] text-gray-400">Data Transkrip</p>
                  </td>
                  <td class="px-5 py-4 text-center">
                    <span :class="{
                      'bg-orange-100 text-orange-700': verifikasi.transkrip.status === 'MENUNGGU',
                      'bg-green-100 text-green-700': verifikasi.transkrip.status === 'DISETUJUI',
                      'bg-red-100 text-red-700': verifikasi.transkrip.status === 'DITOLAK'
                    }" class="px-2 py-1 rounded text-[9px] font-bold uppercase tracking-wide">
                      {{ verifikasi.transkrip.status }}
                    </span>
                  </td>
                  <td class="px-5 py-4">
                    <div class="bg-gray-50 p-2 rounded-lg border-l-3" :class="{
                      'border-l-orange-400': verifikasi.transkrip.status === 'MENUNGGU',
                      'border-l-green-400': verifikasi.transkrip.status === 'DISETUJUI',
                      'border-l-red-500': verifikasi.transkrip.status === 'DITOLAK'
                    }">
                      <p class="text-[9px] font-semibold text-gray-400 uppercase mb-0.5">Pesan Petugas:</p>
                      <p class="text-xs" :class="verifikasi.transkrip.catatan ? 'text-gray-700' : 'text-gray-400 italic'">
                        {{ verifikasi.transkrip.catatan || (verifikasi.transkrip.status === 'MENUNGGU' ? 'Menunggu verifikasi...' : 'Belum ada catatan.') }}
                      </p>
                    </div>
                  </td>
                  <td class="px-5 py-4 text-center">
                    <button v-if="verifikasi.transkrip.sudah_upload" @click="bukaModalDetail('transkrip')" class="bg-indigo-50 text-indigo-600 px-3 py-1.5 rounded-lg text-[10px] font-semibold hover:bg-indigo-100 transition">
                      🔍 Detail
                    </button>
                    <span v-else class="text-gray-300 text-[10px] italic">Belum kirim</span>
                  </td>
                </tr>

                <!-- Perpustakaan -->
                <tr class="hover:bg-slate-50 transition">
                  <td class="px-5 py-4">
                    <p class="font-semibold text-gray-800">📖 Bagian Perpustakaan</p>
                    <p class="text-[10px] text-gray-400">Upload PDF + Abstrak</p>
                  </td>
                  <td class="px-5 py-4 text-center">
                    <span :class="{
                      'bg-orange-100 text-orange-700': verifikasi.perpus.status === 'MENUNGGU',
                      'bg-green-100 text-green-700': verifikasi.perpus.status === 'DISETUJUI',
                      'bg-red-100 text-red-700': verifikasi.perpus.status === 'DITOLAK'
                    }" class="px-2 py-1 rounded text-[9px] font-bold uppercase tracking-wide">
                      {{ verifikasi.perpus.status }}
                    </span>
                  </td>
                  <td class="px-5 py-4">
                    <div class="bg-gray-50 p-2 rounded-lg border-l-3" :class="{
                      'border-l-orange-400': verifikasi.perpus.status === 'MENUNGGU',
                      'border-l-green-400': verifikasi.perpus.status === 'DISETUJUI',
                      'border-l-red-500': verifikasi.perpus.status === 'DITOLAK'
                    }">
                      <p class="text-[9px] font-semibold text-gray-400 uppercase mb-0.5">Pesan Petugas:</p>
                      <div v-if="verifikasi.perpus.status === 'DITOLAK'">
                        <p class="text-xs text-red-700">{{ verifikasi.perpus.catatan || 'Tidak ada alasan penolakan.' }}</p>
                      </div>
                      <div v-else-if="verifikasi.perpus.status === 'MENUNGGU'">
                        <p class="text-xs text-orange-600">{{ verifikasi.perpus.catatan || 'Menunggu verifikasi berkas...' }}</p>
                      </div>
                      <div v-else-if="verifikasi.perpus.status === 'DISETUJUI'">
                        <p class="text-xs text-green-700">{{ verifikasi.perpus.catatan || 'Berkas telah diverifikasi dan disetujui.' }}</p>
                      </div>
                    </div>
                    <div v-if="verifikasi.perpus.status === 'DISETUJUI'" class="mt-2">
                      <button @click="showSuratPerpusModal = true" class="text-xs bg-indigo-100 text-indigo-700 px-3 py-1.5 rounded hover:bg-indigo-200 transition flex items-center gap-1 justify-center w-full">
                        📑 Lihat Surat Bebas Perpustakaan
                      </button>
                    </div>
                  </td>
                  <td class="px-5 py-4 text-center">
                    <button v-if="verifikasi.perpus.sudah_upload" @click="bukaModalDetail('perpus')" class="bg-indigo-50 text-indigo-600 px-3 py-1.5 rounded-lg text-[10px] font-semibold hover:bg-indigo-100 transition">
                      🔍 Detail
                    </button>
                    <span v-else class="text-gray-300 text-[10px] italic">Belum kirim</span>
                  </td>
                </tr>

                <!-- Akademik -->
                <tr class="hover:bg-slate-50 transition">
                  <td class="px-5 py-4">
                    <p class="font-semibold text-gray-800">🎓 Bagian Akademik</p>
                    <p class="text-[10px] text-gray-400">Form Pendaftaran (4 Berkas)</p>
                  </td>
                  <td class="px-5 py-4 text-center">
                    <span :class="{
                      'bg-orange-100 text-orange-700': verifikasi.akademik.status === 'MENUNGGU',
                      'bg-green-100 text-green-700': verifikasi.akademik.status === 'DISETUJUI',
                      'bg-red-100 text-red-700': verifikasi.akademik.status === 'DITOLAK'
                    }" class="px-2 py-1 rounded text-[9px] font-bold uppercase tracking-wide">
                      {{ verifikasi.akademik.status }}
                    </span>
                  </td>
                  <td class="px-5 py-4">
                    <div class="bg-gray-50 p-2 rounded-lg border-l-3" :class="{
                      'border-l-orange-400': verifikasi.akademik.status === 'MENUNGGU',
                      'border-l-green-400': verifikasi.akademik.status === 'DISETUJUI',
                      'border-l-red-500': verifikasi.akademik.status === 'DITOLAK'
                    }">
                      <p class="text-[9px] font-semibold text-gray-400 uppercase mb-0.5">Pesan Petugas:</p>
                      <p class="text-xs" :class="verifikasi.akademik.catatan ? 'text-gray-700' : 'text-gray-400 italic'">
                        {{ verifikasi.akademik.catatan || (verifikasi.akademik.status === 'MENUNGGU' ? 'Menunggu verifikasi...' : 'Belum ada catatan.') }}
                      </p>
                    </div>
                  </td>
                  <td class="px-5 py-4 text-center">
                    <button v-if="verifikasi.akademik.sudah_upload" @click="bukaModalDetail('akademik')" class="bg-indigo-50 text-indigo-600 px-3 py-1.5 rounded-lg text-[10px] font-semibold hover:bg-indigo-100 transition">
                      🔍 Detail
                    </button>
                    <span v-else class="text-gray-300 text-[10px] italic">Belum kirim</span>
                  </td>
                </tr>

                <!-- Pendaftaran Yudisium -->
                <tr class="hover:bg-slate-50 transition">
                  <td class="px-5 py-4">
                    <p class="font-semibold text-gray-800">📋 Pendaftaran Yudisium</p>
                    <p class="text-[10px] text-gray-400">Pendaftaran ke BAAK</p>
                  </td>
                  <td class="px-5 py-4 text-center">
                    <span :class="{
                      'bg-orange-100 text-orange-700': statusPendaftaran === 'MENUNGGU',
                      'bg-green-100 text-green-700': statusPendaftaran === 'DISETUJUI',
                      'bg-red-100 text-red-700': statusPendaftaran === 'DITOLAK',
                      'bg-gray-100 text-gray-500': !statusPendaftaran
                    }" class="px-2 py-1 rounded text-[9px] font-bold uppercase tracking-wide">
                      {{ statusPendaftaran || 'BELUM DAFTAR' }}
                    </span>
                  </td>
                  <td class="px-5 py-4">
                    <div class="bg-gray-50 p-2 rounded-lg border-l-3" :class="{
                      'border-l-orange-400': statusPendaftaran === 'MENUNGGU',
                      'border-l-green-400': statusPendaftaran === 'DISETUJUI',
                      'border-l-red-500': statusPendaftaran === 'DITOLAK',
                      'border-l-gray-300': !statusPendaftaran
                    }">
                      <p class="text-[9px] font-semibold text-gray-400 uppercase mb-0.5">Pesan Petugas:</p>
                      <div v-if="statusPendaftaran === 'DITOLAK'">
                        <p class="text-xs text-red-700">{{ catatanBAAK || 'Tidak ada catatan.' }}</p>
                      </div>
                      <div v-else-if="statusPendaftaran === 'MENUNGGU'">
                        <p class="text-xs text-orange-600">{{ catatanBAAK || 'Menunggu verifikasi BAAK...' }}</p>
                      </div>
                      <div v-else-if="statusPendaftaran === 'DISETUJUI'">
                        <p class="text-xs text-green-700">{{ catatanBAAK || 'Pendaftaran yudisium telah diverifikasi.' }}</p>
                        <p v-if="tanggalVerifikasi" class="text-[10px] text-green-600 mt-1">✅ Diverifikasi: {{ formatTanggal(tanggalVerifikasi) }}</p>
                      </div>
                      <div v-else>
                        <p class="text-xs text-gray-400 italic">Belum melakukan pendaftaran yudisium</p>
                      </div>
                    </div>
                    <div v-if="statusPendaftaran === 'DISETUJUI'" class="mt-2">
                      <button @click="bukaDetailPendaftaranModal" class="text-xs bg-green-100 text-green-700 px-3 py-1.5 rounded hover:bg-green-200 transition flex items-center gap-1 justify-center w-full">
                        📋 Lihat Detail Pendaftaran
                      </button>
                    </div>
                    <div v-else-if="statusPendaftaran === 'MENUNGGU'" class="mt-2">
                      <button @click="bukaDetailPendaftaranModal" class="text-xs bg-orange-100 text-orange-700 px-3 py-1.5 rounded hover:bg-orange-200 transition flex items-center gap-1 justify-center w-full">
                        📋 Lihat Data Pendaftaran
                      </button>
                    </div>
                  </td>
                  <td class="px-5 py-4 text-center">
                    <span class="text-gray-300 text-[10px] italic">-</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- TRANSKRIP VIEW -->
        <div v-else-if="currentView === 'transkrip'" class="max-w-5xl mx-auto pb-10">
          <button @click="kembaliKeDashboard" class="mb-5 flex items-center gap-2 text-indigo-600 font-semibold hover:text-indigo-800 transition text-sm">
            ← Batal & Kembali ke Dashboard
          </button>
          
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="p-5 bg-indigo-700 text-white">
              <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <h2 class="text-xl font-bold">Input Nilai Mata Kuliah</h2>
                  <p class="text-indigo-200 text-sm mt-0.5">Jurusan: <span class="font-semibold text-white">{{ user.prodi || 'Belum diatur' }}</span></p>
                </div>
                <div class="flex gap-2">
                  <span :class="transkripStep >= 1 ? 'bg-white text-indigo-700' : 'bg-indigo-800 text-indigo-300'" class="w-7 h-7 flex items-center justify-center rounded-full text-xs font-bold shadow">1</span>
                  <span class="w-5 h-0.5 bg-indigo-400 self-center"></span>
                  <span :class="transkripStep >= 2 ? 'bg-white text-indigo-700' : 'bg-indigo-800 text-indigo-300'" class="w-7 h-7 flex items-center justify-center rounded-full text-xs font-bold shadow">2</span>
                  <span class="w-5 h-0.5 bg-indigo-400 self-center"></span>
                  <span :class="transkripStep === 3 ? 'bg-white text-indigo-700' : 'bg-indigo-800 text-indigo-300'" class="w-7 h-7 flex items-center justify-center rounded-full text-xs font-bold shadow">3</span>
                </div>
              </div>
            </div>

            <div class="p-6">
              <div v-if="transkripStep === 1">
                <h3 class="text-lg font-bold text-gray-800 mb-2">Langkah 1: Pilih Kelompok Mata Kuliah Pilihan</h3>
                <p class="text-gray-500 text-sm mb-5">Pilih peminatan Anda. Ini akan menentukan cabang mata kuliah pilihan apa saja yang akan muncul di formulir transkrip.</p>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div v-for="kel in availableKelompok" :key="kel" 
                       @click="selectedKelompokPilihan = kel"
                       :class="['p-4 rounded-xl border-2 cursor-pointer transition', selectedKelompokPilihan === kel ? 'border-indigo-600 bg-indigo-50' : 'border-gray-200 hover:border-indigo-300']">
                    <div class="flex items-center gap-2">
                      <div :class="['w-4 h-4 rounded-full border-2 flex items-center justify-center', selectedKelompokPilihan === kel ? 'border-indigo-600' : 'border-gray-300']">
                        <div v-if="selectedKelompokPilihan === kel" class="w-2 h-2 bg-indigo-600 rounded-full"></div>
                      </div>
                      <span class="font-semibold text-gray-800">{{ kel }}</span>
                    </div>
                  </div>
                </div>

                <div v-if="availableKelompok.length === 0" class="p-5 bg-orange-50 text-orange-700 rounded-xl border border-orange-200 text-center">
                  <span class="text-2xl block mb-1">ℹ️</span>
                  Program studi Anda belum memiliki daftar mata kuliah pilihan. Klik Lanjut.
                </div>
              </div>

              <div v-if="transkripStep === 2">
                <h3 class="text-lg font-bold text-gray-800 mb-2">Langkah 2: Pilih Jenis Tugas Akhir</h3>
                <p class="text-gray-500 text-sm mb-5">Pilih jalur kelulusan atau tugas akhir yang Anda ambil.</p>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div v-for="ta in availableTA" :key="ta" 
                       @click="selectedJenisTA = ta"
                       :class="['p-4 rounded-xl border-2 cursor-pointer transition', selectedJenisTA === ta ? 'border-blue-600 bg-blue-50' : 'border-gray-200 hover:border-blue-300']">
                    <div class="flex items-center gap-2">
                      <div :class="['w-4 h-4 rounded-full border-2 flex items-center justify-center', selectedJenisTA === ta ? 'border-blue-600' : 'border-gray-300']">
                        <div v-if="selectedJenisTA === ta" class="w-2 h-2 bg-blue-600 rounded-full"></div>
                      </div>
                      <span class="font-semibold text-gray-800">{{ ta }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="transkripStep === 3">
                <h3 class="text-lg font-bold text-gray-800 mb-2">Langkah 3: Isi Nilai Mata Kuliah</h3>
                <div class="bg-blue-50 border border-blue-200 p-4 mb-6 rounded-xl">
                  <p class="text-blue-800 text-sm">
                    📝 Isikan nilai huruf (<b>A, B, C, D, atau E</b>) pada kolom yang tersedia.<br>
                    <span class="inline-block mt-1 text-[10px] font-semibold text-blue-800 bg-blue-200 px-2 py-0.5 rounded">PENTING:</span> Untuk <b>Mata Kuliah Pilihan</b>, cukup isi yang Anda ambil saja.
                  </p>
                </div>
                
                <div class="overflow-x-auto border border-gray-200 rounded-xl">
                  <table class="w-full text-left text-sm">
                    <template v-for="kategori in ['Wajib', 'Pilihan', 'TA']" :key="kategori">
                      <tr v-if="tableData.filter(mk => mk.kategori === kategori).length > 0">
                        <td colspan="4" :class="[
                          kategori === 'Wajib' ? 'bg-indigo-100 text-indigo-800' : '',
                          kategori === 'Pilihan' ? 'bg-purple-100 text-purple-800' : '',
                          kategori === 'TA' ? 'bg-rose-100 text-rose-800' : ''
                        ]" class="p-3 font-bold uppercase text-[10px] tracking-wider">
                          📚 Mata Kuliah {{ kategori }}
                          <span v-if="kategori === 'Pilihan' && selectedKelompokPilihan" class="font-normal text-[9px] opacity-70"> - Peminatan: {{ selectedKelompokPilihan }}</span>
                          <span v-if="kategori === 'TA' && selectedJenisTA" class="font-normal text-[9px] opacity-70"> - Jalur: {{ selectedJenisTA }}</span>
                        </td>
                      </tr>
                      <tr v-for="row in tableData.filter(mk => mk.kategori === kategori)" :key="row.kode" class="border-b border-gray-100 hover:bg-gray-50">
                        <td class="p-3 w-24 font-mono text-[10px] text-gray-500">{{ row.kode }}</td>
                        <td class="p-3 font-medium text-gray-800">{{ row.nama_mk }}
                          <span v-if="kategori === 'Pilihan'" class="ml-1 bg-gray-200 text-gray-500 text-[8px] px-1 py-0.5 rounded">Opsional</span>
                        </td>
                        <td class="p-3 w-16 text-center font-semibold text-gray-500">{{ row.sks }} SKS</td>
                        <td class="p-2 w-32">
                          <input v-model="row.nilai" 
                                :class="[
                                  'w-full p-2 text-center font-bold uppercase rounded-lg border focus:ring-2 outline-none text-sm',
                                  kategori === 'Pilihan' ? 'bg-gray-100 border-gray-200 text-gray-700 focus:ring-gray-300' : 'bg-white border-indigo-200 text-indigo-700 focus:ring-indigo-300'
                                ]"
                                maxlength="2" 
                                :placeholder="kategori === 'Pilihan' ? '-' : 'Nilai'" />
                         </td>
                       </tr>
                    </template>
                  </table>
                </div>
              </div>
            </div>

            <div class="p-5 border-t border-gray-200 bg-gray-50 flex justify-between items-center">
              <button v-if="transkripStep > 1" @click="transkripStep--" class="px-5 py-2 text-gray-600 font-semibold hover:bg-gray-200 rounded-lg transition text-sm">
                ← Kembali
              </button>
              <div v-else></div>
              <button v-if="transkripStep < 3" @click="nextStep" class="px-6 py-2 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 transition shadow text-sm">
                Lanjut ke Langkah {{ transkripStep + 1 }} →
              </button>
              <button v-if="transkripStep === 3" @click="simpanTranskrip" :disabled="loadingSimpanTranskrip" class="px-6 py-2 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition shadow disabled:opacity-50 flex items-center gap-2 text-sm">
                <span v-if="loadingSimpanTranskrip" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
                💾 Simpan Semua Nilai
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- MODALS (disingkat karena panjang, sama seperti sebelumnya) -->
      <div v-if="showDetailModal" class="fixed inset-0 bg-gray-900/60 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="showDetailModal = false">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-lg max-h-[80vh] overflow-hidden flex flex-col">
          <div class="p-4 bg-indigo-700 text-white flex justify-between items-center">
            <h2 class="font-semibold">📄 Detail Pengiriman</h2>
            <button @click="showDetailModal = false" class="text-white hover:text-red-200 text-xl">✕</button>
          </div>
          <div class="p-5 overflow-y-auto flex-1">
            <div v-if="selectedDetailKey === 'akademik'" class="space-y-2">
              <div v-for="(url, name) in verifikasi.akademik.files" :key="name" class="flex justify-between items-center p-2 border rounded-lg bg-gray-50">
                <span class="text-xs font-semibold text-gray-600 uppercase">{{ name }}</span>
                <a v-if="url" :href="getFullImageUrl(url)" target="_blank" class="text-xs bg-indigo-600 text-white px-2 py-1 rounded font-semibold">👁️ Lihat</a>
                <span v-else class="text-xs text-red-400 italic">Kosong</span>
              </div>
            </div>
            <div v-else-if="selectedDetailKey === 'perpus'">
              <div class="space-y-3">
                <p class="text-xs font-semibold text-gray-700">📄 File Abstrak:</p>
                <div v-if="verifikasi.perpus.file_abstrak">
                  <a :href="getFullImageUrl(verifikasi.perpus.file_abstrak)" target="_blank" class="text-xs bg-purple-600 text-white px-2 py-1 rounded font-semibold inline-block">👁️ Lihat Abstrak PDF</a>
                </div>
                <p v-else class="text-xs text-gray-600 bg-gray-50 p-2 rounded-lg">Tidak ada file abstrak</p>
                <p class="text-xs font-semibold text-gray-700 mt-2">📚 File PDF:</p>
                <div class="space-y-1 max-h-60 overflow-y-auto">
                  <div v-for="(url, name) in verifikasi.perpus.files" :key="name" class="flex justify-between items-center p-2 border rounded-lg bg-gray-50">
                    <span class="text-[10px] font-semibold text-gray-600 capitalize">{{ name.replace(/_/g, ' ') }}</span>
                    <a v-if="url" :href="getFullImageUrl(url)" target="_blank" class="text-[10px] bg-purple-600 text-white px-2 py-1 rounded font-semibold">👁️ Lihat</a>
                  </div>
                </div>
              </div>
            </div>
            <div v-else-if="selectedDetailKey === 'transkrip'">
              <p class="text-sm text-gray-500 mb-3">Data nilai sudah tersimpan di sistem.</p>
              <button @click="mulaiIsiTranskrip(); showDetailModal = false" class="w-full bg-blue-600 text-white py-2 rounded-lg font-semibold text-sm">📝 Lihat & Edit Tabel Nilai</button>
            </div>
          </div>
          <div class="p-3 border-t bg-gray-50 text-right">
            <button @click="showDetailModal = false" class="px-4 py-1.5 text-gray-600 font-semibold hover:bg-gray-200 rounded-lg text-sm">Tutup</button>
          </div>
        </div>
      </div>

      <!-- MODAL SURAT BEBAS PERPUSTAKAAN -->
<div v-if="showSuratPerpusModal" class="fixed inset-0 bg-black/70 z-[60] flex items-center justify-center p-4 backdrop-blur-sm" @click.self="showSuratPerpusModal = false">
  <div class="bg-white rounded-xl shadow-2xl w-full max-w-md flex flex-col max-h-[90vh] overflow-hidden animate-fadeIn">
    <div class="bg-indigo-900 text-white p-4 md:p-5 flex justify-between items-center shadow-md">
      <div>
        <h3 class="font-bold text-lg flex items-center gap-2">
          <span class="text-2xl">📑</span> 
          Surat Keterangan Bebas Perpustakaan
        </h3>
        <p class="text-xs text-indigo-200 mt-0.5">Dokumen resmi yang diterbitkan oleh Bagian Perpustakaan</p>
      </div>
      <button @click="showSuratPerpusModal = false" class="text-white hover:text-red-400 font-bold text-3xl leading-none">&times;</button>
    </div>
    
    <div class="flex-1 overflow-y-auto p-6 bg-gray-100">
      <div v-if="verifikasi.perpus.link_surat_pdf" class="space-y-4">
        <div class="bg-green-50 border-l-4 border-green-500 p-4 rounded-lg shadow-sm">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
              <span class="text-green-600 text-xl">✅</span>
            </div>
            <div class="flex-1">
              <p class="font-bold text-green-800">Status: DISETUJUI</p>
              <p class="text-xs text-green-700">Surat ini telah ditandatangani secara digital dan SAH digunakan untuk keperluan yudisium.</p>
            </div>
          </div>
        </div>
        
        <!-- HANYA TOMBOL BUKA PDF -->
        <div class="bg-white rounded-lg shadow-lg p-6 text-center">
          <div class="flex flex-col items-center gap-4">
            <div class="w-20 h-20 bg-indigo-100 rounded-full flex items-center justify-center">
              <span class="text-indigo-600 text-4xl">📄</span>
            </div>
            <h4 class="font-bold text-gray-800 text-lg">Surat Bebas Perpustakaan</h4>
            <p class="text-gray-500 text-sm">Klik tombol di bawah untuk membuka surat.</p>
            <a :href="getFullImageUrl(verifikasi.perpus.link_surat_pdf)" 
               target="_blank" 
               class="w-full bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-3 rounded-lg transition flex items-center justify-center gap-2 font-semibold">
              <span class="text-lg">🔗</span>
              Buka Surat PDF
            </a>
          </div>
        </div>
      </div>
      <div v-else class="bg-white rounded-lg shadow-lg p-8 text-center">
        <div class="flex flex-col items-center">
          <div class="w-20 h-20 bg-yellow-100 rounded-full flex items-center justify-center mb-4">
            <span class="text-yellow-600 text-3xl">⏳</span>
          </div>
          <h4 class="font-bold text-gray-800 text-lg mb-2">Surat PDF Sedang Diproses</h4>
          <p class="text-gray-500 text-sm mb-4">Surat bebas perpustakaan Anda sedang dalam proses pembuatan oleh petugas perpustakaan.</p>
          <button @click="refreshStatusSurat" class="px-5 py-2 bg-indigo-600 text-white rounded-lg text-sm font-bold hover:bg-indigo-700 transition flex items-center gap-2">
            🔄 Refresh Status
          </button>
        </div>
      </div>
    </div>
    <div class="p-4 bg-white border-t border-gray-200 flex justify-end">
      <button @click="showSuratPerpusModal = false" class="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-bold transition">
        Tutup
      </button>
    </div>
  </div>
</div>

      <!-- MODAL DETAIL PENDAFTARAN YUDISIUM -->
      <div v-if="showDetailPendaftaranModal" class="fixed inset-0 bg-black/70 z-[60] flex items-center justify-center p-4 backdrop-blur-sm" @click.self="showDetailPendaftaranModal = false">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-md flex flex-col max-h-[90vh] overflow-hidden animate-fadeIn">
          <div class="bg-gradient-to-r from-green-600 to-green-700 text-white p-4 flex justify-between items-center">
            <div>
              <h3 class="font-bold text-lg flex items-center gap-2">📋 Detail Pendaftaran Yudisium</h3>
              <p class="text-xs text-green-100">Informasi lengkap pendaftaran Anda</p>
            </div>
            <div class="flex gap-2">
              <button @click="ambilDetailPendaftaranLengkap" class="text-white hover:text-green-200 text-lg" title="Refresh data">🔄</button>
              <button @click="showDetailPendaftaranModal = false" class="text-white hover:text-red-300 text-2xl">&times;</button>
            </div>
          </div>
          <div class="flex-1 overflow-y-auto p-5 space-y-3">
            <div class="bg-gray-50 p-3 rounded-lg"><p class="text-xs text-gray-500">Nama Lengkap</p><p class="font-semibold">{{ detailPendaftaran.nama_lengkap || user.full_name || '-' }}</p></div>
            <div class="bg-gray-50 p-3 rounded-lg"><p class="text-xs text-gray-500">NIM</p><p class="font-semibold">{{ detailPendaftaran.nim || user.username || '-' }}</p></div>
            <div class="bg-gray-50 p-3 rounded-lg"><p class="text-xs text-gray-500">Tempat, Tanggal Lahir</p><p class="font-semibold">{{ detailPendaftaran.tempat_lahir || '-' }}, {{ formatTanggal(detailPendaftaran.tanggal_lahir) }}</p></div>
            <div class="bg-gray-50 p-3 rounded-lg"><p class="text-xs text-gray-500">NIK</p><p class="font-semibold">{{ detailPendaftaran.nik || '-' }}</p></div>
            <div class="bg-gray-50 p-3 rounded-lg"><p class="text-xs text-gray-500">Nama Ibu Kandung</p><p class="font-semibold">{{ detailPendaftaran.nama_ibu_kandung || '-' }}</p></div>
            <div class="bg-gray-50 p-3 rounded-lg"><p class="text-xs text-gray-500">Nama Bapak Kandung</p><p class="font-semibold">{{ detailPendaftaran.nama_bapak_kandung || '-' }}</p></div>
            <div class="bg-gray-50 p-3 rounded-lg"><p class="text-xs text-gray-500">Tanggal Daftar</p><p class="font-semibold">{{ formatTanggal(detailPendaftaran.tanggal_daftar || tanggalDaftar) }}</p></div>
            <div v-if="detailPendaftaran.tanggal_verifikasi || tanggalVerifikasi" class="bg-gray-50 p-3 rounded-lg"><p class="text-xs text-gray-500">Tanggal Verifikasi</p><p class="font-semibold">{{ formatTanggal(detailPendaftaran.tanggal_verifikasi || tanggalVerifikasi) }}</p></div>
            <div v-if="detailPendaftaran.catatan_baak || catatanBAAK" class="bg-indigo-50 p-3 rounded-lg border-l-4 border-indigo-500">
              <p class="text-xs text-indigo-600 font-semibold">📝 Catatan BAAK</p>
              <p class="text-sm text-gray-700 mt-1">{{ detailPendaftaran.catatan_baak || catatanBAAK }}</p>
            </div>
          </div>
          <div class="p-4 bg-gray-50 border-t flex justify-between gap-2">
            <button @click="ambilDetailPendaftaranLengkap" class="px-4 py-2 bg-indigo-100 hover:bg-indigo-200 text-indigo-700 rounded-lg text-sm font-bold transition flex items-center gap-1">🔄 Refresh</button>
            <button @click="showDetailPendaftaranModal = false" class="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-bold transition">Tutup</button>
          </div>
        </div>
      </div>

      <!-- MODAL PANDUAN BERKAS -->
      <div v-if="showPanduanModal" class="fixed inset-0 bg-black/70 z-[60] flex items-center justify-center p-4 backdrop-blur-sm overflow-y-auto" @click.self="showPanduanModal = false">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-5xl my-8 flex flex-col max-h-[90vh] overflow-hidden animate-fadeIn relative">
          <div class="bg-gradient-to-r from-indigo-700 to-indigo-900 text-white p-4 md:p-5 flex justify-between items-center shadow-md z-20 sticky top-0">
            <div><h3 class="font-bold text-lg flex items-center gap-2">📖 Panduan Berkas Yudisium</h3><p class="text-xs text-indigo-200 mt-0.5">Daftar lengkap berkas yang harus diunggah untuk setiap bagian</p></div>
            <button @click="showPanduanModal = false" class="text-white hover:text-red-400 font-bold text-3xl leading-none">&times;</button>
          </div>
          <div class="flex-1 overflow-y-auto p-5 bg-gray-50">
            <!-- Panduan BAAK -->
            <div class="bg-white rounded-xl shadow-md mb-6 overflow-hidden border border-gray-200">
              <div class="bg-blue-600 text-white p-4"><div class="flex items-center gap-3"><span class="text-2xl">📋</span><div><h4 class="font-bold text-lg">Bagian BAAK</h4><p class="text-sm text-blue-100">Data Transkrip Nilai Mahasiswa</p></div></div></div>
              <div class="p-5"><div class="grid grid-cols-1 md:grid-cols-3 gap-4"><div class="bg-blue-50 rounded-lg p-4 border-l-4 border-blue-500"><div class="flex items-center gap-2 mb-2"><span class="text-xl">1️⃣</span><span class="font-bold text-blue-800">Pilih Jurusan</span></div><p class="text-sm text-gray-600">Mahasiswa memilih program studi/jurusan yang diambil.</p></div><div class="bg-blue-50 rounded-lg p-4 border-l-4 border-blue-500"><div class="flex items-center gap-2 mb-2"><span class="text-xl">2️⃣</span><span class="font-bold text-blue-800">Mata Kuliah Pilihan</span></div><p class="text-sm text-gray-600">Memilih kelompok peminatan mata kuliah pilihan yang diambil selama perkuliahan.</p></div><div class="bg-blue-50 rounded-lg p-4 border-l-4 border-blue-500"><div class="flex items-center gap-2 mb-2"><span class="text-xl">3️⃣</span><span class="font-bold text-blue-800">Jenis Tugas Akhir</span></div><p class="text-sm text-gray-600">Memilih jalur kelulusan/tugas akhir yang diambil (Skripsi, Tesis, dll).</p></div></div><div class="mt-4 bg-gray-50 p-3 rounded-lg"><p class="text-xs text-gray-500 flex items-center gap-1">📌 <span class="font-semibold">Catatan:</span> Setelah memilih ketiga poin di atas, mahasiswa mengisi nilai mata kuliah wajib, pilihan, dan TA.</p></div></div>
            </div>
            
            <!-- Panduan Perpustakaan -->
            <div class="bg-white rounded-xl shadow-md mb-6 overflow-hidden border border-gray-200">
              <div class="bg-purple-600 text-white p-4"><div class="flex items-center gap-3"><span class="text-2xl">📖</span><div><h4 class="font-bold text-lg">Bagian Perpustakaan</h4><p class="text-sm text-purple-100">Berkas Tugas Akhir / Skripsi Lengkap</p></div></div></div>
              <div class="p-5"><div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3"><div class="bg-purple-50 rounded-lg p-3 flex items-start gap-2"><span class="text-purple-600 text-lg">a.</span><div><p class="font-semibold text-purple-800 text-sm">Hal Awal</p><p class="text-xs text-gray-500">Halaman judul, lembar pengesahan, abstrak, kata pengantar</p></div></div><div class="bg-purple-50 rounded-lg p-3 flex items-start gap-2"><span class="text-purple-600 text-lg">b.</span><div><p class="font-semibold text-purple-800 text-sm">Abstrak</p><p class="text-xs text-gray-500">Ringkasan tugas akhir (format PDF)</p></div></div><div class="bg-purple-50 rounded-lg p-3 flex items-start gap-2"><span class="text-purple-600 text-lg">c.</span><div><p class="font-semibold text-purple-800 text-sm">Bab 1 - Pendahuluan</p><p class="text-xs text-gray-500">Latar belakang, rumusan masalah, tujuan penelitian</p></div></div><div class="bg-purple-50 rounded-lg p-3 flex items-start gap-2"><span class="text-purple-600 text-lg">d.</span><div><p class="font-semibold text-purple-800 text-sm">Bab 2 - Tinjauan Pustaka</p><p class="text-xs text-gray-500">Landasan teori dan penelitian terkait</p></div></div><div class="bg-purple-50 rounded-lg p-3 flex items-start gap-2"><span class="text-purple-600 text-lg">e.</span><div><p class="font-semibold text-purple-800 text-sm">Bab 3 - Metodologi</p><p class="text-xs text-gray-500">Metode penelitian yang digunakan</p></div></div><div class="bg-purple-50 rounded-lg p-3 flex items-start gap-2"><span class="text-purple-600 text-lg">f.</span><div><p class="font-semibold text-purple-800 text-sm">Bab 4 - Hasil & Pembahasan</p><p class="text-xs text-gray-500">Hasil penelitian dan analisis data</p></div></div><div class="bg-purple-50 rounded-lg p-3 flex items-start gap-2"><span class="text-purple-600 text-lg">g.</span><div><p class="font-semibold text-purple-800 text-sm">Bab 5 - Kesimpulan</p><p class="text-xs text-gray-500">Kesimpulan dan saran</p></div></div><div class="bg-purple-50 rounded-lg p-3 flex items-start gap-2"><span class="text-purple-600 text-lg">h.</span><div><p class="font-semibold text-purple-800 text-sm">Daftar Pustaka</p><p class="text-xs text-gray-500">Daftar referensi yang digunakan</p></div></div><div class="bg-purple-50 rounded-lg p-3 flex items-start gap-2"><span class="text-purple-600 text-lg">i.</span><div><p class="font-semibold text-purple-800 text-sm">Lampiran</p><p class="text-xs text-gray-500">Dokumen pendukung penelitian</p></div></div><div class="bg-purple-50 rounded-lg p-3 flex items-start gap-2"><span class="text-purple-600 text-lg">j.</span><div><p class="font-semibold text-purple-800 text-sm">Jurnal Publikasi</p><p class="text-xs text-gray-500">Jurnal hasil penelitian yang dipublikasikan</p></div></div><div class="bg-purple-50 rounded-lg p-3 flex items-start gap-2"><span class="text-purple-600 text-lg">k.</span><div><p class="font-semibold text-purple-800 text-sm">Lampiran Cetak</p><p class="text-xs text-gray-500">Dokumen cetak pendukung</p></div></div><div class="bg-purple-50 rounded-lg p-3 flex items-start gap-2"><span class="text-purple-600 text-lg">l.</span><div><p class="font-semibold text-purple-800 text-sm">Cek Plagiasi Jurnal</p><p class="text-xs text-gray-500">Hasil cek plagiasi jurnal/tugas akhir</p></div></div></div><div class="mt-4 bg-gray-50 p-3 rounded-lg"><p class="text-xs text-gray-500 flex items-center gap-1">📌 <span class="font-semibold">Catatan:</span> Semua file harus dalam format PDF, maksimal 5MB per file.</p></div></div>
            </div>

            <!-- Panduan Akademik -->
            <div class="bg-white rounded-xl shadow-md overflow-hidden border border-gray-200">
              <div class="bg-rose-600 text-white p-4"><div class="flex items-center gap-3"><span class="text-2xl">🎓</span><div><h4 class="font-bold text-lg">Bagian Akademik</h4><p class="text-sm text-rose-100">Dokumen Pendaftaran Yudisium</p></div></div></div>
              <div class="p-5"><div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"><div class="bg-rose-50 rounded-lg p-4 text-center border border-rose-200"><div class="w-12 h-12 bg-rose-200 rounded-full flex items-center justify-center mx-auto mb-2"><span class="text-rose-600 text-xl">🪪</span></div><p class="font-semibold text-rose-800">a. Foto KTP</p><p class="text-xs text-gray-500 mt-1">Kartu Tanda Penduduk yang masih berlaku</p></div><div class="bg-rose-50 rounded-lg p-4 text-center border border-rose-200"><div class="w-12 h-12 bg-rose-200 rounded-full flex items-center justify-center mx-auto mb-2"><span class="text-rose-600 text-xl">📄</span></div><p class="font-semibold text-rose-800">b. Foto Akta Kelahiran</p><p class="text-xs text-gray-500 mt-1">Dokumen akta kelahiran yang sah</p></div><div class="bg-rose-50 rounded-lg p-4 text-center border border-rose-200"><div class="w-12 h-12 bg-rose-200 rounded-full flex items-center justify-center mx-auto mb-2"><span class="text-rose-600 text-xl">📸</span></div><p class="font-semibold text-rose-800">c. Pas Foto 3x4</p><p class="text-xs text-gray-500 mt-1">Foto terbaru background merah/putih</p></div><div class="bg-rose-50 rounded-lg p-4 text-center border border-rose-200"><div class="w-12 h-12 bg-rose-200 rounded-full flex items-center justify-center mx-auto mb-2"><span class="text-rose-600 text-xl">🎓</span></div><p class="font-semibold text-rose-800">d. Foto Ijazah</p><p class="text-xs text-gray-500 mt-1">Ijazah terakhir (jika ada)</p></div></div><div class="mt-4 bg-gray-50 p-3 rounded-lg"><p class="text-xs text-gray-500 flex items-center gap-1">📌 <span class="font-semibold">Catatan:</span> Pastikan semua dokumen jelas terbaca dan tidak terpotong.</p></div></div>
            </div>
          </div>
          <div class="p-4 bg-white border-t border-gray-200 flex justify-end gap-2 z-20 sticky bottom-0">
            <button @click="showPanduanModal = false" class="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-bold transition shadow-md flex items-center gap-2">✕ Tutup Panduan</button>
          </div>
        </div>
      </div>

      <!-- MODAL PROFIL -->
      <div v-if="showProfilModal" class="fixed inset-0 bg-gray-900/60 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="showProfilModal = false">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-md overflow-hidden">
          <div class="p-4 bg-indigo-600 text-white flex justify-between items-center"><h2 class="font-semibold flex items-center gap-2">👤 Profil Saya</h2><button @click="showProfilModal = false" class="text-white hover:text-red-300 text-xl">✕</button></div>
          <div class="p-5 space-y-3">
            <div><label class="block text-[10px] font-bold text-gray-500 uppercase">Nama Lengkap</label><input type="text" :value="user.full_name" disabled class="w-full p-2 bg-gray-100 border rounded-lg text-gray-700 text-sm"></div>
            <div class="grid grid-cols-2 gap-3"><div><label class="block text-[10px] font-bold text-gray-500 uppercase">NIM</label><input type="text" :value="user.username" disabled class="w-full p-2 bg-gray-100 border rounded-lg text-gray-700 text-sm"></div><div><label class="block text-[10px] font-bold text-gray-500 uppercase">Angkatan</label><input type="text" :value="user.angkatan" disabled class="w-full p-2 bg-gray-100 border rounded-lg text-gray-700 text-sm"></div></div>
            <div><label class="block text-[10px] font-bold text-gray-500 uppercase">Program Studi</label><input type="text" :value="user.prodi" disabled class="w-full p-2 bg-gray-100 border rounded-lg text-gray-700 text-sm"></div>
            <div><label class="block text-[10px] font-bold text-gray-700 uppercase flex justify-between">Email <span class="text-indigo-500 text-[9px] normal-case">*Bisa diedit</span></label><input type="email" v-model="editForm.email" class="w-full p-2 border border-indigo-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none text-sm"></div>
          </div>
          <div class="p-4 border-t bg-gray-50 flex justify-end gap-2"><button @click="showProfilModal = false" class="px-4 py-1.5 text-gray-600 font-semibold rounded-lg hover:bg-gray-200 text-sm">Tutup</button><button @click="simpanEmail" :disabled="loadingUpdateProfil || editForm.email === user.email" class="px-4 py-1.5 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 text-sm flex items-center gap-1 shadow"><span v-if="loadingUpdateProfil" class="animate-spin h-3 w-3 border-2 border-white border-t-transparent rounded-full"></span>💾 Simpan</button></div>
        </div>
      </div>

      <!-- MODAL AKADEMIK -->
      <div v-if="showAkademikModal" class="fixed inset-0 bg-gray-900/60 flex items-center justify-center z-50 p-4 backdrop-blur-sm" @click.self="showAkademikModal = false">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-2xl flex flex-col max-h-[85vh]">
          <div class="p-4 border-b bg-rose-50 flex justify-between items-center"><div><h2 class="font-bold text-rose-800">{{ verifikasi.akademik.sudah_upload ? '📎 Berkas Akademik Terkirim' : '📎 Formulir Berkas Akademik' }}</h2><p class="text-[10px] text-rose-600">Unggah 4 dokumen (Max 2MB per file)</p></div><button @click="showAkademikModal = false" class="text-rose-400 hover:text-red-600 text-xl">✕</button></div>
          <div class="p-5 overflow-y-auto flex-1 space-y-4">
            <div v-for="(label, key) in {ijazah: '📄 Ijazah Akhir', akte: '📄 Akte Kelahiran', ktp: '🪪 KTP', foto3x4: '📸 Pas Foto 3x4'}" :key="key" class="bg-gray-50 p-3 rounded-lg border">
              <label class="block text-xs font-semibold text-gray-700 mb-1">{{ label }}</label>
              <div v-if="verifikasi.akademik.sudah_upload && !editAkademik[key]" class="flex items-center justify-between"><span class="text-xs text-green-600">✅ Berkas tersimpan</span><div class="flex gap-2"><a v-if="verifikasi.akademik.files[key]" :href="getFullImageUrl(verifikasi.akademik.files[key])" target="_blank" class="text-[10px] bg-indigo-100 text-indigo-700 px-2 py-1 rounded">👁️ Lihat</a><button @click="editAkademik[key] = true" class="text-[10px] bg-amber-100 text-amber-700 px-2 py-1 rounded">✏️ Ubah</button></div></div>
              <div v-else><input type="file" @change="e => handleFileAkademik(e, key)" accept=".jpg,.jpeg,.png,.pdf" class="block w-full text-xs text-gray-500 file:mr-2 file:py-1 file:px-3 file:rounded file:border-0 file:bg-rose-100 file:text-rose-700"/><button v-if="verifikasi.akademik.sudah_upload" @click="editAkademik[key] = false" class="mt-1 text-[9px] text-gray-500">Batal ganti</button></div>
            </div>
          </div>
          <div class="p-4 border-t bg-gray-50 flex justify-end gap-2"><button @click="showAkademikModal = false" class="px-4 py-1.5 text-gray-600 font-semibold rounded-lg hover:bg-gray-200 text-sm">Batal</button><button @click="simpanAkademik" :disabled="loadingAkademik" class="px-4 py-1.5 bg-rose-600 text-white font-semibold rounded-lg hover:bg-rose-700 text-sm flex items-center gap-1"><span v-if="loadingAkademik" class="animate-spin h-3 w-3 border-2 border-white border-t-transparent rounded-full"></span>{{ verifikasi.akademik.sudah_upload ? '💾 Simpan' : '📤 Kirim' }}</button></div>
        </div>
      </div>

      <!-- MODAL PERPUSTAKAAN -->
      <div v-if="showPerpusModal" class="fixed inset-0 bg-gray-900/60 flex items-center justify-center z-50 p-4 backdrop-blur-sm overflow-y-auto" @click.self="showPerpusModal = false">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-5xl my-8 flex flex-col max-h-[90vh]">
          <div class="p-4 border-b bg-purple-50 flex justify-between items-center sticky top-0"><div><h2 class="font-bold text-purple-800">📖 Upload Berkas Perpustakaan</h2><p class="text-[10px] text-purple-600">Unggah file PDF untuk abstrak dan 11 berkas lainnya</p></div><button @click="showPerpusModal = false" class="text-purple-400 hover:text-red-600 text-xl">✕</button></div>
          <div class="flex-1 overflow-y-auto p-5 space-y-5">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div v-for="(config, key) in perpusFileConfig" :key="key">
                <div class="bg-white p-3 rounded-lg border shadow-sm">
                  <label class="block text-xs font-semibold text-gray-700 mb-1">{{ config.label }} <span class="text-red-500">*</span></label>
                  <p class="text-[9px] text-gray-400 mb-1">PDF, max 5MB</p>
                  <div v-if="key === 'file_abstrak' ? (verifikasi.perpus.file_abstrak && !perpusForm.editFiles['file_abstrak']) : (verifikasi.perpus.files && verifikasi.perpus.files[key] && !perpusForm.editFiles[key])" class="flex items-center justify-between bg-green-50 p-2 rounded">
                    <span class="text-[10px] text-green-700 truncate">✅ {{ getFileName(key === 'file_abstrak' ? verifikasi.perpus.file_abstrak : verifikasi.perpus.files[key]) }}</span>
                    <div class="flex gap-1"><a :href="getFullImageUrl(key === 'file_abstrak' ? verifikasi.perpus.file_abstrak : verifikasi.perpus.files[key])" target="_blank" class="text-[9px] bg-purple-100 text-purple-700 px-2 py-0.5 rounded">👁️ Lihat</a><button @click="perpusForm.editFiles[key] = true" class="text-[9px] bg-amber-100 text-amber-700 px-2 py-0.5 rounded">✏️ Ganti</button></div>
                  </div>
                  <div v-else><input type="file" @change="key === 'file_abstrak' ? handleFileAbstrak($event) : handleFilePerpus($event, key)" accept=".pdf" class="block w-full text-xs text-gray-500 file:mr-2 file:py-1 file:px-3 file:rounded file:border-0 file:bg-purple-100 file:text-purple-700 file:font-semibold"/>
                  <div v-if="key === 'file_abstrak' && perpusForm.file_abstrak" class="mt-1 text-[9px] text-green-600 truncate">📄 {{ perpusForm.file_abstrak.name }}</div>
                  <div v-if="key !== 'file_abstrak' && perpusForm.files[key]" class="mt-1 text-[9px] text-green-600 truncate">📄 {{ perpusForm.files[key].name }}</div></div>
                </div>
              </div>
            </div>
          </div>
          <div class="p-4 border-t bg-gray-50 flex justify-end gap-2 sticky bottom-0"><button @click="showPerpusModal = false" class="px-4 py-1.5 text-gray-600 font-semibold rounded-lg hover:bg-gray-200 text-sm">Batal</button><button @click="simpanPerpus" :disabled="loadingPerpus || !isPerpusFormValid" class="px-4 py-1.5 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 text-sm flex items-center gap-1"><span v-if="loadingPerpus" class="animate-spin h-3 w-3 border-2 border-white border-t-transparent rounded-full"></span>💾 {{ verifikasi.perpus.sudah_upload ? 'Simpan Perubahan' : 'Kirim Semua Berkas' }}</button></div>
        </div>
      </div>

      <!-- MODAL PENDAFTARAN YUDISIUM -->
      <div v-if="showPendaftaranModal" class="fixed inset-0 bg-gray-900/60 flex items-center justify-center z-[70] p-4 backdrop-blur-sm overflow-y-auto" @click.self="showPendaftaranModal = false">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-2xl my-8 flex flex-col max-h-[90vh] animate-fadeIn">
          <div class="bg-gradient-to-r from-green-600 to-green-700 text-white p-5 flex justify-between items-center sticky top-0 rounded-t-xl">
            <div><h2 class="font-bold text-xl flex items-center gap-2">📝 Pendaftaran Yudisium</h2><p class="text-sm text-green-100 mt-1">Selamat! Semua berkas Anda telah divalidasi. Silakan lengkapi data berikut.</p></div>
            <button @click="showPendaftaranModal = false" class="text-white hover:text-red-300 text-2xl">&times;</button>
          </div>
          <div class="p-6 overflow-y-auto flex-1">
            <form @submit.prevent="daftarYudisium" class="space-y-4">
              <div class="bg-green-50 p-4 rounded-lg mb-4"><h3 class="font-bold text-green-800 mb-3 flex items-center gap-2">👤 Data Diri Mahasiswa</h3><div class="grid grid-cols-1 md:grid-cols-2 gap-4"><div><label class="block text-xs font-bold text-gray-600 uppercase mb-1">Nama Lengkap <span class="text-red-500">*</span></label><input type="text" v-model="formPendaftaran.nama_lengkap" required class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"></div><div><label class="block text-xs font-bold text-gray-600 uppercase mb-1">NIM <span class="text-red-500">*</span></label><input type="text" v-model="formPendaftaran.nim" required readonly class="w-full p-3 border border-gray-300 rounded-lg bg-gray-100 text-gray-600"></div></div></div>
              <div class="bg-blue-50 p-4 rounded-lg mb-4"><h3 class="font-bold text-blue-800 mb-3 flex items-center gap-2">🎂 Tempat & Tanggal Lahir</h3><div class="grid grid-cols-1 md:grid-cols-2 gap-4"><div><label class="block text-xs font-bold text-gray-600 uppercase mb-1">Tempat Lahir <span class="text-red-500">*</span></label><input type="text" v-model="formPendaftaran.tempat_lahir" required class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Contoh: Jakarta"></div><div><label class="block text-xs font-bold text-gray-600 uppercase mb-1">Tanggal Lahir <span class="text-red-500">*</span></label><input type="date" v-model="formPendaftaran.tanggal_lahir" required class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"></div></div></div>
              <div class="bg-purple-50 p-4 rounded-lg mb-4"><h3 class="font-bold text-purple-800 mb-3 flex items-center gap-2">🆔 Nomor Induk Kependudukan (NIK)</h3><div><label class="block text-xs font-bold text-gray-600 uppercase mb-1">NIK <span class="text-red-500">*</span></label><input type="text" v-model="formPendaftaran.nik" required maxlength="16" pattern="[0-9]{16}" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" placeholder="16 digit angka"><p class="text-[10px] text-gray-400 mt-1">Masukkan 16 digit angka NIK sesuai KTP</p></div></div>
              <div class="bg-amber-50 p-4 rounded-lg mb-4"><h3 class="font-bold text-amber-800 mb-3 flex items-center gap-2">👨‍👩‍👧 Nama Orang Tua</h3><div class="grid grid-cols-1 md:grid-cols-2 gap-4"><div><label class="block text-xs font-bold text-gray-600 uppercase mb-1">Nama Ibu Kandung <span class="text-red-500">*</span></label><input type="text" v-model="formPendaftaran.nama_ibu_kandung" required class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 outline-none"></div><div><label class="block text-xs font-bold text-gray-600 uppercase mb-1">Nama Bapak Kandung <span class="text-red-500">*</span></label><input type="text" v-model="formPendaftaran.nama_bapak_kandung" required class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 outline-none"></div></div></div>
              <div class="bg-gray-50 p-4 rounded-lg border border-gray-200"><div class="flex items-start gap-3"><input type="checkbox" v-model="formPendaftaran.disclaimer" required class="mt-1"><label class="text-sm text-gray-600">Saya menyatakan bahwa data yang saya isikan adalah benar dan sesuai dengan dokumen resmi. Saya siap menerima konsekuensi apabila terdapat data yang tidak sesuai.</label></div></div>
              <div class="flex justify-end gap-3 pt-4 border-t mt-4"><button type="button" @click="showPendaftaranModal = false" class="px-6 py-2.5 bg-gray-200 hover:bg-gray-300 rounded-lg font-semibold transition">Batal</button><button type="submit" :disabled="loadingPendaftaran" class="px-6 py-2.5 bg-green-600 hover:bg-green-700 text-white rounded-lg font-semibold transition flex items-center gap-2"><span v-if="loadingPendaftaran" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>📤 Kirim Pendaftaran</button></div>
            </form>
          </div>
        </div>
      </div>

      <!-- TOAST NOTIFIKASI -->
      <div class="fixed bottom-4 right-4 z-50 space-y-2 max-w-sm w-full pointer-events-none">
        <div v-for="toast in toastNotifikasi" :key="toast.id" @click="bukaNotifikasiFromToast(toast)" :class="['bg-white rounded-lg shadow-lg p-3 border-l-4 cursor-pointer pointer-events-auto transform transition-all animate-slide-in', getNotifClass(toast.tipe)]">
          <div class="flex justify-between items-start">
            <div class="flex-1"><div class="flex items-center gap-2"><span class="text-base">{{ getIconNotif(toast.tipe) }}</span><h4 class="font-semibold text-xs">{{ toast.judul }}</h4></div><p class="text-[10px] text-gray-600 mt-0.5 line-clamp-2">{{ toast.pesan }}</p><p class="text-[9px] text-gray-400 mt-1">{{ formatWaktu(toast.created_at) }}</p></div>
            <button @click.stop="hapusToast(toast.id)" class="text-gray-400 hover:text-gray-600 text-xs px-1">✕</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  headers: { 'Content-Type': 'application/json' }
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

const router = useRouter()

// ========== DATA STATE ==========
const currentView = ref('dashboard')
const loading = ref(false)
const error = ref(false)
const loadingRefresh = ref(false)
const showProfilModal = ref(false)
const loadingUpdateProfil = ref(false)
const editForm = ref({ email: '' })
const showDetailModal = ref(false)
const selectedDetailKey = ref('')
const loadingNotifikasi = ref(false)

const user = ref({ full_name: "", username: "", email: "", angkatan: "", prodi: "" })
const verifikasi = ref({
  transkrip: { status: "MENUNGGU", catatan: "", sudah_upload: false, data_nilai: [] },
  perpus: { 
    status: "MENUNGGU", 
    catatan: "", 
    sudah_upload: false, 
    file_abstrak: null,
    files: {}, 
    validated_at: null,
    link_surat_pdf: null,
    petugas_nama: null
  },
  akademik: { status: "MENUNGGU", catatan: "", sudah_upload: false, files: { ijazah: null, akte: null, ktp: null, foto3x4: null } },
  status_akhir: "PROSES"
})

// ========== COMPUTED STATUS AKHIR (DIPERBAIKI) ==========
const statusAkhirDisplay = computed(() => {
  // Cek apakah semua berkas sudah DISETUJUI
  const semuaBerkasDisetujui = 
    verifikasi.value.transkrip.status === 'DISETUJUI' &&
    verifikasi.value.perpus.status === 'DISETUJUI' &&
    verifikasi.value.akademik.status === 'DISETUJUI'
  
  console.log('Status Transkrip:', verifikasi.value.transkrip.status)
  console.log('Status Perpus:', verifikasi.value.perpus.status)
  console.log('Status Akademik:', verifikasi.value.akademik.status)
  console.log('Semua berkas disetujui:', semuaBerkasDisetujui)
  console.log('Status Pendaftaran:', statusPendaftaran.value)
  
  // Jika semua berkas sudah disetujui
  if (semuaBerkasDisetujui) {
    // Cek status pendaftaran yudisium
    if (statusPendaftaran.value === 'DISETUJUI') {
      return 'LULUS'
    } else if (statusPendaftaran.value === 'MENUNGGU') {
      return 'MENUNGGU_VERIFIKASI'
    } else if (statusPendaftaran.value === 'DITOLAK') {
      return 'PENDAFTARAN_DITOLAK'
    } else {
      // Belum daftar yudisium
      return 'SILAKAN_DAFTAR'
    }
  }
  
  // Jika belum semua berkas disetujui
  return 'PROSES'
})

// ========== SURAT PERPUS & DETAIL PENDAFTARAN ==========
const showSuratPerpusModal = ref(false)
const showDetailPendaftaranModal = ref(false)
const showPanduanModal = ref(false)

const detailPendaftaran = ref({
  nama_lengkap: '',
  nim: '',
  tempat_lahir: '',
  tanggal_lahir: '',
  nik: '',
  nama_ibu_kandung: '',
  nama_bapak_kandung: '',
  tanggal_daftar: '',
  tanggal_verifikasi: '',
  catatan_baak: ''
})

// ========== NOTIFIKASI STATE ==========
const notifikasiList = ref([])
const unreadCount = ref(0)
const showNotifikasiDropdown = ref(false)
const toastNotifikasi = ref([])
let intervalNotif = null

// ========== TRANSKRIP STATE ==========
const transkripStep = ref(1)
const selectedKelompokPilihan = ref('')
const selectedJenisTA = ref('')
const tableData = ref([])
const loadingSimpanTranskrip = ref(false)
const daftarMataKuliahBAAK = ref([])

// ========== MODAL AKADEMIK ==========
const showAkademikModal = ref(false)
const loadingAkademik = ref(false)
const akademikFiles = ref({ ijazah: null, akte: null, ktp: null, foto3x4: null })
const editAkademik = ref({ ijazah: false, akte: false, ktp: false, foto3x4: false })

// ========== MODAL PERPUS ==========
const perpusFileConfig = {
  file_abstrak: { label: '📄 File Abstrak PDF' },
  bagian_awal: { label: '📄 Bagian Awal' },
  bab1: { label: '📄 Bab 1 - Pendahuluan' },
  bab2: { label: '📄 Bab 2 - Tinjauan Pustaka' },
  bab3: { label: '📄 Bab 3 - Metodologi' },
  bab4: { label: '📄 Bab 4 - Hasil & Pembahasan' },
  bab5: { label: '📄 Bab 5 - Kesimpulan' },
  daftar_pustaka: { label: '📄 Daftar Pustaka' },
  lampiran: { label: '📄 Lampiran' },
  jurnal_publikasi: { label: '📄 Jurnal Publikasi' },
  lampiran_cetak: { label: '📄 Lampiran Cetak' },
  cek_plagiasi_jurnal: { label: '📄 Cek Plagiasi Jurnal' }
}

const showPerpusModal = ref(false)
const loadingPerpus = ref(false)
const perpusForm = ref({ file_abstrak: null, files: {}, editFiles: {} })

// ========== PENDAFTARAN YUDISIUM STATE ==========
const showPendaftaranModal = ref(false)
const loadingPendaftaran = ref(false)
const bisaDaftarYudisium = ref(false)
const statusPendaftaran = ref(null)
const tanggalDaftar = ref(null)
const tanggalVerifikasi = ref(null)
const catatanBAAK = ref(null)

const formPendaftaran = ref({
  nama_lengkap: '',
  nim: '',
  tempat_lahir: '',
  tanggal_lahir: '',
  nik: '',
  nama_ibu_kandung: '',
  nama_bapak_kandung: '',
  disclaimer: false
})

// ========== HELPER FUNCTIONS ==========
const indicatorClass = (status) => {
  if (status === 'DISETUJUI') return 'bg-green-500 shadow-green-500/50'
  if (status === 'DITOLAK') return 'bg-red-500 shadow-red-500/50'
  return 'bg-orange-500 shadow-orange-500/50'
}

const getFullImageUrl = (path) => {
  if (!path) return ''
  if (path.startsWith('http://') || path.startsWith('https://') || path.startsWith('data:image')) return path
  const backendBaseUrl = api.defaults.baseURL.replace(/\/api\/?$/, '')
  return `${backendBaseUrl}${path.startsWith('/') ? path : '/' + path}`
}

const formatTanggal = (date) => {
  if (!date) return '-'
  return new Intl.DateTimeFormat('id-ID', { day: 'numeric', month: 'long', year: 'numeric' }).format(new Date(date))
}

const formatWaktu = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const diff = Date.now() - date
  if (diff < 60000) return 'Baru saja'
  if (diff < 3600000) return `${Math.floor(diff / 60000)} menit lalu`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)} jam lalu`
  return date.toLocaleDateString('id-ID')
}

const getIconNotif = (tipe) => {
  switch(tipe) {
    case 'BERKAS_MASUK': return '📋'
    case 'VALIDASI_DITERIMA': return '✅'
    case 'VALIDASI_DITOLAK': return '❌'
    case 'SURAT_BEBAS_PERPUS': return '📄'
    case 'VERIFIKASI_YUDISIUM': return '✅'
    default: return '🔔'
  }
}

const getNotifClass = (tipe) => {
  switch(tipe) {
    case 'BERKAS_MASUK': return 'border-blue-500 bg-blue-50'
    case 'VALIDASI_DITERIMA': return 'border-green-500 bg-green-50'
    case 'VALIDASI_DITOLAK': return 'border-red-500 bg-red-50'
    case 'SURAT_BEBAS_PERPUS': return 'border-indigo-500 bg-indigo-50'
    case 'VERIFIKASI_YUDISIUM': return 'border-green-500 bg-green-50'
    default: return 'border-indigo-500 bg-indigo-50'
  }
}

const isMatchProdi = (jurusanData) => {
  if (!jurusanData) return false
  const j = jurusanData.toLowerCase()
  const p = (user.value.prodi || "").toLowerCase()
  return j === 'semua jurusan' || p.includes(j) || j.includes(p)
}

const getFileName = (url) => {
  if (!url) return ''
  const parts = url.split('/')
  return decodeURIComponent(parts[parts.length - 1]) || 'file.pdf'
}

// ========== COMPUTED ==========
const totalSelesai = computed(() => {
  let count = 0
  // Cek apakah sudah upload file/nilai, bukan hanya record ada
  if (verifikasi.value.transkrip.sudah_upload === true) count++
  if (verifikasi.value.perpus.sudah_upload === true) count++
  if (verifikasi.value.akademik.sudah_upload === true) count++
  return count
})

const progress = computed(() => Math.round((totalSelesai.value / 3) * 100))

const availableKelompok = computed(() => {
  const groups = new Set()
  daftarMataKuliahBAAK.value.forEach(mk => {
    if (isMatchProdi(mk.jurusan) && mk.kategori === 'Pilihan' && mk.kelompok) groups.add(mk.kelompok)
  })
  return Array.from(groups)
})

const availableTA = computed(() => {
  const groups = new Set()
  daftarMataKuliahBAAK.value.forEach(mk => {
    if (isMatchProdi(mk.jurusan) && mk.kategori === 'TA' && mk.kelompok) groups.add(mk.kelompok)
  })
  return Array.from(groups)
})

const isPerpusFormValid = computed(() => {
  const hasFileAbstrak = perpusForm.value.file_abstrak || (verifikasi.value.perpus.file_abstrak && !perpusForm.value.editFiles['file_abstrak'])
  if (!hasFileAbstrak) return false
  return Object.keys(perpusFileConfig).every(key => {
    if (key === 'file_abstrak') return true
    return perpusForm.value.files[key] || (verifikasi.value.perpus.files?.[key] && !perpusForm.value.editFiles[key])
  })
})

// ========== NOTIFIKASI FUNCTIONS ==========
const fetchNotifikasi = async () => {
  try {
    const res = await api.get('notifikasi/')
    notifikasiList.value = res.data
    unreadCount.value = notifikasiList.value.filter(n => !n.is_read).length
  } catch (err) { console.error('Gagal fetch notifikasi:', err) }
}

const fetchNotifikasiBaru = async () => {
  try {
    const res = await api.get('notifikasi/belum_dibaca/')
    const newNotif = res.data.results.filter(n => !toastNotifikasi.value.some(e => e.id === n.id) && !notifikasiList.value.some(e => e.id === n.id))
    if (newNotif.length > 0) {
      toastNotifikasi.value = [...newNotif, ...toastNotifikasi.value]
      unreadCount.value = res.data.count
      setTimeout(() => { toastNotifikasi.value = toastNotifikasi.value.filter(n => !newNotif.some(newN => newN.id === n.id)) }, 8000)
      await fetchNotifikasi()
    }
  } catch (err) { console.error('Gagal fetch notifikasi baru:', err) }
}

const bukaNotifikasi = async (notif) => {
  if (!notif.is_read) {
    try {
      await api.post(`notifikasi/${notif.id}/baca/`)
      notif.is_read = true
      unreadCount.value = Math.max(0, unreadCount.value - 1)
      await fetchNotifikasi()
    } catch (err) { console.error('Gagal menandai notifikasi:', err) }
  }
  showNotifikasiDropdown.value = false
  if (notif.tipe === 'VERIFIKASI_YUDISIUM') {
    await cekStatusPendaftaranYudisium()
    await fetchStatus()
  }
}

const bukaNotifikasiFromToast = async (notif) => {
  await bukaNotifikasi(notif)
  toastNotifikasi.value = toastNotifikasi.value.filter(n => n.id !== notif.id)
}

const bacaSemuaNotifikasi = async () => {
  try {
    await api.post('notifikasi/baca_semua/')
    notifikasiList.value.forEach(n => n.is_read = true)
    unreadCount.value = 0
    await fetchNotifikasi()
  } catch (err) { console.error('Gagal baca semua notifikasi:', err) }
}

const toggleNotifikasi = () => {
  showNotifikasiDropdown.value = !showNotifikasiDropdown.value
  if (showNotifikasiDropdown.value) { fetchNotifikasi() }
}

const lihatSemuaNotifikasi = () => {
  showNotifikasiDropdown.value = false
  alert('Fitur ini akan segera hadir')
}

const hapusToast = (id) => { toastNotifikasi.value = toastNotifikasi.value.filter(n => n.id !== id) }

// ========== API FUNCTIONS ==========
const fetchProfile = async () => {
  try {
    const res = await api.get('users/me/')
    Object.assign(user.value, res.data)
    editForm.value.email = user.value.email
  } catch (e) { console.error(e) }
}

const fetchMataKuliah = async () => {
  try {
    const res = await api.get('matakuliah/')
    daftarMataKuliahBAAK.value = res.data
  } catch (err) { console.error(err) }
}

const fetchStatus = async () => {
  loading.value = true
  try {
    const res = await api.get("pendaftaran/status_saya/")
    if (res.data.akademik) {
      verifikasi.value.akademik.status = res.data.akademik.status
      verifikasi.value.akademik.catatan = res.data.akademik.catatan
      verifikasi.value.akademik.sudah_upload = res.data.akademik.sudah_upload
      verifikasi.value.akademik.files = {
        ijazah: res.data.akademik.foto_ijazah || null,
        akte: res.data.akademik.foto_akte || null,
        ktp: res.data.akademik.foto_ktp || null,
        foto3x4: res.data.akademik.foto_3x4 || null
      }
    }
    if (res.data.perpus) {
      verifikasi.value.perpus.status = res.data.perpus.status || 'MENUNGGU'
      verifikasi.value.perpus.catatan = res.data.perpus.catatan || ''
      verifikasi.value.perpus.sudah_upload = res.data.perpus.sudah_upload || false
      verifikasi.value.perpus.file_abstrak = res.data.perpus.file_abstrak || null
      verifikasi.value.perpus.files = res.data.perpus.files || {}
      verifikasi.value.perpus.validated_at = res.data.perpus.validated_at || null
      verifikasi.value.perpus.link_surat_pdf = res.data.perpus.link_surat_pdf || null
      verifikasi.value.perpus.petugas_nama = res.data.perpus.petugas_nama || null
    }
    if (res.data.transkrip) {
      verifikasi.value.transkrip.status = res.data.transkrip.status || 'MENUNGGU'
      verifikasi.value.transkrip.catatan = res.data.transkrip.catatan || ''
      verifikasi.value.transkrip.sudah_upload = res.data.transkrip.sudah_upload || false
      verifikasi.value.transkrip.data_nilai = res.data.transkrip.data_nilai || []
    }
    error.value = false
    await cekStatusPendaftaranYudisium()
  } catch (err) { 
    console.error('❌ FetchStatus error:', err); 
    error.value = true 
  } finally { 
    loading.value = false 
  }
}

// Tambahkan di bagian methods
const fetchSuratPerpus = async () => {
  try {
    console.log('🔄 Fetching surat perpus...')
    const response = await api.get('get-surat-perpus/')
    console.log('Response surat perpus:', response.data)
    
    if (response.data.success && response.data.link_surat_pdf) {
      // Update verifikasi.perpus dengan link surat
      verifikasi.value.perpus.link_surat_pdf = response.data.link_surat_pdf
      verifikasi.value.perpus.status = response.data.status || 'DISETUJUI'
      
      console.log('✅ Surat PDF ditemukan:', response.data.link_surat_pdf)
      return true
    } else {
      console.log('⚠️ Surat PDF belum tersedia:', response.data.message)
      return false
    }
  } catch (error) {
    console.error('❌ Gagal fetch surat perpus:', error)
    return false
  }
}

// Perbaiki method refreshStatusSurat
const refreshStatusSurat = async () => {
  console.log('🔄 Refreshing status surat...')
  
  // Method 1: Fetch dari endpoint khusus
  const suratTersedia = await fetchSuratPerpus()
  
  if (suratTersedia) {
    alert('✅ Surat PDF sudah tersedia!')
    // Tutup modal dan buka ulang untuk refresh tampilan
    showSuratPerpusModal.value = false
    setTimeout(() => {
      showSuratPerpusModal.value = true
    }, 100)
  } else {
    // Method 2: Refresh semua status
    await fetchStatus()
    
    if (verifikasi.value.perpus.link_surat_pdf) {
      alert('✅ Surat PDF sudah tersedia!')
      showSuratPerpusModal.value = false
      setTimeout(() => {
        showSuratPerpusModal.value = true
      }, 100)
    } else {
      alert('⏳ Surat PDF masih dalam proses pembuatan. Silakan cek kembali nanti.')
    }
  }
}

// Perbaiki method bukaModalSuratPerpus
const bukaModalSuratPerpus = async () => {
  console.log('📑 Membuka modal surat perpus...')
  console.log('Data perpus saat ini:', verifikasi.value.perpus)
  
  // Fetch ulang untuk memastikan data terbaru
  await fetchSuratPerpus()
  
  if (verifikasi.value.perpus.link_surat_pdf) {
    console.log('✅ Menampilkan PDF:', verifikasi.value.perpus.link_surat_pdf)
    showSuratPerpusModal.value = true
  } else {
    console.log('⚠️ PDF belum tersedia, tetap buka modal dengan pesan loading')
    showSuratPerpusModal.value = true
  }
}

const refreshAllData = async () => {
  loadingRefresh.value = true
  try {
    await fetchStatus()
    await cekStatusPendaftaranYudisium()
    alert('✅ Data berhasil di-refresh!')
  } catch (err) {
    alert('❌ Gagal refresh data')
  } finally {
    loadingRefresh.value = false
  }
}

const cekStatusPendaftaranYudisium = async () => {
  try {
    const res = await api.get('pendaftaran-yudisium/cek-status/')
    bisaDaftarYudisium.value = res.data.bisa_daftar || false
    statusPendaftaran.value = res.data.status_pendaftaran || null
    tanggalDaftar.value = res.data.tanggal_daftar || null
    tanggalVerifikasi.value = res.data.tanggal_verifikasi || null
    catatanBAAK.value = res.data.catatan_baak || null
    
    detailPendaftaran.value = {
      nama_lengkap: user.value.full_name || '',
      nim: user.value.username || '',
      tempat_lahir: res.data.tempat_lahir || '',
      tanggal_lahir: res.data.tanggal_lahir || '',
      nik: res.data.nik || '',
      nama_ibu_kandung: res.data.nama_ibu_kandung || '',
      nama_bapak_kandung: res.data.nama_bapak_kandung || '',
      tanggal_daftar: tanggalDaftar.value || '',
      tanggal_verifikasi: tanggalVerifikasi.value || '',
      catatan_baak: catatanBAAK.value || ''
    }
    
    formPendaftaran.value.nama_lengkap = user.value.full_name || ''
    formPendaftaran.value.nim = user.value.username || ''
    
    if (res.data.pernah_daftar) {
      formPendaftaran.value.tempat_lahir = res.data.tempat_lahir || ''
      formPendaftaran.value.tanggal_lahir = res.data.tanggal_lahir || ''
      formPendaftaran.value.nik = res.data.nik || ''
      formPendaftaran.value.nama_ibu_kandung = res.data.nama_ibu_kandung || ''
      formPendaftaran.value.nama_bapak_kandung = res.data.nama_bapak_kandung || ''
    }
  } catch (err) {
    console.error('❌ Gagal cek status pendaftaran:', err)
    bisaDaftarYudisium.value = false
  }
}

const ambilDetailPendaftaranLengkap = async () => {
  try {
    const res = await api.get('pendaftaran-yudisium/detail/')
    if (res.data.success && res.data.data) {
      detailPendaftaran.value = {
        ...detailPendaftaran.value,
        ...res.data.data
      }
    }
  } catch (err) {
    console.error('❌ Gagal ambil detail pendaftaran:', err)
  }
}

const bukaDetailPendaftaranModal = async () => {
  await ambilDetailPendaftaranLengkap()
  showDetailPendaftaranModal.value = true
}

const bukaModalPendaftaran = () => {
  formPendaftaran.value = {
    nama_lengkap: user.value.full_name || '',
    nim: user.value.username || '',
    tempat_lahir: detailPendaftaran.value.tempat_lahir || '',
    tanggal_lahir: detailPendaftaran.value.tanggal_lahir || '',
    nik: detailPendaftaran.value.nik || '',
    nama_ibu_kandung: detailPendaftaran.value.nama_ibu_kandung || '',
    nama_bapak_kandung: detailPendaftaran.value.nama_bapak_kandung || '',
    disclaimer: false
  }
  showPendaftaranModal.value = true
}

const daftarYudisium = async () => {
  if (!formPendaftaran.value.disclaimer) {
    alert('Harap centang disclaimer terlebih dahulu')
    return
  }
  if (formPendaftaran.value.nik.length !== 16 || !/^\d+$/.test(formPendaftaran.value.nik)) {
    alert('NIK harus 16 digit angka')
    return
  }
  loadingPendaftaran.value = true
  try {
    const res = await api.post('pendaftaran-yudisium/daftar/', {
      nama_lengkap: formPendaftaran.value.nama_lengkap,
      nim: formPendaftaran.value.nim,
      tempat_lahir: formPendaftaran.value.tempat_lahir,
      tanggal_lahir: formPendaftaran.value.tanggal_lahir,
      nik: formPendaftaran.value.nik,
      nama_ibu_kandung: formPendaftaran.value.nama_ibu_kandung,
      nama_bapak_kandung: formPendaftaran.value.nama_bapak_kandung
    })
    if (res.data.success) {
      alert('✅ Pendaftaran yudisium berhasil dikirim! Silakan tunggu verifikasi dari BAAK.')
      showPendaftaranModal.value = false
      await cekStatusPendaftaranYudisium()
      await fetchStatus()
    }
  } catch (err) {
    const errorMsg = err.response?.data?.error || err.response?.data?.message || 'Gagal mendaftar yudisium'
    alert('❌ ' + errorMsg)
  } finally {
    loadingPendaftaran.value = false
  }
}

// ========== TRANSKRIP FUNCTIONS ==========
const kembaliKeDashboard = () => {
  currentView.value = 'dashboard'
  transkripStep.value = 1
}

const mulaiIsiTranskrip = () => {
  const savedData = verifikasi.value.transkrip.data_nilai || []
  if (savedData.length > 0) {
    generateTableDataFromSaved(savedData)
    transkripStep.value = 3
    currentView.value = 'transkrip'
  } else {
    selectedKelompokPilihan.value = ''
    selectedJenisTA.value = ''
    transkripStep.value = 1
    currentView.value = 'transkrip'
  }
}

const generateTableDataFromSaved = (savedData) => {
  const nilaiMap = new Map()
  savedData.forEach(item => {
    const kodeMk = item.kode_mk || item.kode
    nilaiMap.set(kodeMk, item.nilai || item.huruf || '')
  })
  const filteredMK = daftarMataKuliahBAAK.value.filter(mk => {
    if (!isMatchProdi(mk.jurusan)) return false
    if (mk.kategori === 'Wajib') return true
    if (mk.kategori === 'Pilihan') return mk.kelompok === selectedKelompokPilihan.value
    if (mk.kategori === 'TA') return mk.kelompok === selectedJenisTA.value
    return false
  })
  tableData.value = filteredMK.map(mk => ({
    kode: mk.kode,
    nama_mk: mk.nama,
    sks: mk.sks,
    kategori: mk.kategori,
    nilai: nilaiMap.get(mk.kode) || ''
  }))
}

const generateTableData = () => {
  const savedData = verifikasi.value.transkrip.data_nilai || []
  const nilaiMap = new Map()
  savedData.forEach(item => {
    const kodeMk = item.kode_mk || item.kode
    nilaiMap.set(kodeMk, item.nilai || item.huruf || '')
  })
  const filteredMK = daftarMataKuliahBAAK.value.filter(mk => {
    if (!isMatchProdi(mk.jurusan)) return false
    if (mk.kategori === 'Wajib') return true
    if (mk.kategori === 'Pilihan') return mk.kelompok === selectedKelompokPilihan.value
    if (mk.kategori === 'TA') return mk.kelompok === selectedJenisTA.value
    return false
  })
  tableData.value = filteredMK.map(mk => ({
    kode: mk.kode,
    nama_mk: mk.nama,
    sks: mk.sks,
    kategori: mk.kategori,
    nilai: nilaiMap.get(mk.kode) || ''
  }))
}

const nextStep = () => {
  if (transkripStep.value === 1) {
    if (availableKelompok.value.length > 0 && !selectedKelompokPilihan.value) {
      return alert('Silakan pilih kelompok peminatan Anda.')
    }
    transkripStep.value = 2
  } else if (transkripStep.value === 2) {
    if (!selectedJenisTA.value) {
      return alert('Silakan pilih jenis tugas akhir Anda.')
    }
    generateTableData()
    transkripStep.value = 3
  }
}

const simpanTranskrip = async () => {
  const wajibBelumDiisi = tableData.value.filter(mk => (mk.kategori === 'Wajib' || mk.kategori === 'TA') && (!mk.nilai || mk.nilai.trim() === ''))
  if (wajibBelumDiisi.length > 0) {
    return alert(`Mata kuliah WAJIB dan TA harus diisi nilainya!\n\nYang kosong: ${wajibBelumDiisi.map(m => m.nama_mk).join(', ')}`)
  }
  const dataYangDisimpan = tableData.value.filter(mk => mk.nilai && mk.nilai.trim() !== '')
  if (dataYangDisimpan.length === 0) return alert("Anda belum mengisi nilai apapun.")
  loadingSimpanTranskrip.value = true
  try {
    await api.post('transkrip-nilai/simpan-spreadsheet/', { data_nilai: dataYangDisimpan })
    alert("✅ Data transkrip berhasil disimpan!")
    currentView.value = 'dashboard'
    transkripStep.value = 1
    await fetchStatus()
  } catch (err) { 
    alert("Gagal menyimpan transkrip. Silakan coba lagi.") 
  } finally { 
    loadingSimpanTranskrip.value = false 
  }
}

// ========== MODAL FUNCTIONS ==========
const bukaModalDetail = (key) => {
  selectedDetailKey.value = key
  showDetailModal.value = true
}

const bukaModalProfil = () => {
  editForm.value.email = user.value.email
  showProfilModal.value = true
}

const simpanEmail = async () => {
  loadingUpdateProfil.value = true
  try {
    await api.patch('users/me/', { email: editForm.value.email })
    user.value.email = editForm.value.email
    showProfilModal.value = false
    alert('✅ Email berhasil diperbarui!')
  } catch (err) { alert("❌ Gagal memperbarui email") }
  finally { loadingUpdateProfil.value = false }
}

const bukaModalAkademik = () => {
  editAkademik.value = { ijazah: false, akte: false, ktp: false, foto3x4: false }
  akademikFiles.value = { ijazah: null, akte: null, ktp: null, foto3x4: null }
  showAkademikModal.value = true
}

const handleFileAkademik = (event, type) => {
  if (event.target.files[0]) akademikFiles.value[type] = event.target.files[0]
}

const simpanAkademik = async () => {
  const formData = new FormData()
  let hasFile = false
  if (akademikFiles.value.ijazah) { formData.append('foto_ijazah', akademikFiles.value.ijazah); hasFile = true }
  if (akademikFiles.value.akte) { formData.append('foto_akte', akademikFiles.value.akte); hasFile = true }
  if (akademikFiles.value.ktp) { formData.append('foto_ktp', akademikFiles.value.ktp); hasFile = true }
  if (akademikFiles.value.foto3x4) { formData.append('foto_3x4', akademikFiles.value.foto3x4); hasFile = true }
  if (!hasFile && !verifikasi.value.akademik.sudah_upload) return alert("Pilih file!")
  loadingAkademik.value = true
  try {
    await api.post('pendaftaran/upload-akademik/', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    alert('✅ Berkas akademik berhasil dikirim!')
    showAkademikModal.value = false
    fetchStatus()
  } catch (err) { alert("❌ Gagal mengirim berkas") }
  finally { loadingAkademik.value = false }
}

const bukaModalPerpus = async () => {
  perpusForm.value = { file_abstrak: null, files: {}, editFiles: {} }
  showPerpusModal.value = true
}

const handleFilePerpus = (event, key) => {
  if (event.target.files[0]) {
    const file = event.target.files[0]
    if (file.type !== 'application/pdf') return alert('Hanya file PDF yang diperbolehkan!')
    if (file.size > 5 * 1024 * 1024) return alert('Ukuran file maksimal 5MB!')
    perpusForm.value.files[key] = file
  }
}

const handleFileAbstrak = (event) => {
  if (event.target.files[0]) {
    const file = event.target.files[0]
    if (file.type !== 'application/pdf') {
      alert('Hanya file PDF yang diperbolehkan untuk abstrak!')
      return
    }
    if (file.size > 5 * 1024 * 1024) {
      alert('Ukuran file abstrak maksimal 5MB!')
      return
    }
    perpusForm.value.file_abstrak = file
  }
}

const simpanPerpus = async () => {
  const hasFileAbstrak = perpusForm.value.file_abstrak || (verifikasi.value.perpus.file_abstrak && !perpusForm.value.editFiles['file_abstrak'])
  if (!hasFileAbstrak) {
    alert('Mohon upload file abstrak PDF terlebih dahulu!')
    return
  }
  loadingPerpus.value = true
  const formData = new FormData()
  if (perpusForm.value.file_abstrak) formData.append('file_abstrak', perpusForm.value.file_abstrak)
  Object.keys(perpusFileConfig).forEach(key => {
    if (key !== 'file_abstrak' && perpusForm.value.files[key]) {
      formData.append(key, perpusForm.value.files[key])
    }
  })
  try {
    await api.post('bebas-perpus/upload/', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    alert('✅ Berhasil mengirim berkas perpustakaan!')
    showPerpusModal.value = false
    await fetchStatus()
  } catch (err) {
    alert('❌ Gagal: ' + (err.response?.data?.error || err.message))
  } finally { loadingPerpus.value = false }
}

const downloadSuratPDF = () => {
  const pdfUrl = verifikasi.value.perpus.link_surat_pdf
  if (!pdfUrl) {
    alert('PDF tidak tersedia untuk diunduh')
    return
  }
  const fullUrl = getFullImageUrl(pdfUrl)
  const link = document.createElement('a')
  link.href = fullUrl
  link.download = `Surat_Bebas_Perpustakaan_${user.value.username || 'mahasiswa'}.pdf`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

const cetakSuratPDF = () => {
  const pdfUrl = verifikasi.value.perpus.link_surat_pdf
  if (!pdfUrl) {
    alert('PDF tidak tersedia untuk dicetak')
    return
  }
  const fullUrl = getFullImageUrl(pdfUrl)
  const printWindow = window.open(fullUrl, '_blank')
  if (printWindow) {
    printWindow.onload = () => {
      setTimeout(() => { printWindow.print() }, 500)
    }
  } else {
    alert('Popup terblokir. Silakan izinkan popup untuk mencetak.')
  }
}


const bukaPanduanModal = () => { showPanduanModal.value = true }

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.replace("/login")
}

// ========== WATCHERS & LIFECYCLE ==========
watch([selectedKelompokPilihan, selectedJenisTA], () => {
  if (currentView.value === 'transkrip' && transkripStep.value === 3) {
    generateTableData()
  }
})

// Tambahkan di bagian watch
watch(() => verifikasi.value.perpus.link_surat_pdf, (newValue, oldValue) => {
  console.log('🔔 link_surat_pdf berubah:')
  console.log('  Old:', oldValue)
  console.log('  New:', newValue)
  
  if (newValue && !oldValue) {
    // Jika link baru muncul, beri notifikasi
    console.log('✅ Surat PDF baru terdeteksi!')
  }
}, { deep: true })

onMounted(() => {
  console.log("🚀 Dashboard Mhs mounted")
  fetchProfile()
  fetchStatus()
  fetchMataKuliah()
  fetchNotifikasi()
  intervalNotif = setInterval(fetchNotifikasiBaru, 15000)
})

onUnmounted(() => {
  if (intervalNotif) clearInterval(intervalNotif)
})
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.3s ease-in-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-slide-in {
  animation: slideIn 0.3s ease-out;
}
@keyframes slideIn {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>