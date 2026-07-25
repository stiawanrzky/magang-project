from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# ============================================
# CUSTOM ADMIN SITE - Perbaiki Tampilan
# ============================================

# 1. Admin untuk User (menggunakan UserAdmin bawaan Django)
class CustomUserAdmin(UserAdmin):
    # Menambahkan UUID ke list display
    list_display = ('id', 'username', 'email', 'full_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'full_name', 'id')
    ordering = ('username',)
    
    # Field yang ditampilkan saat edit
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informasi Pribadi', {
            'fields': ('full_name', 'email', 'role')
        }),
        ('Izin', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Tanggal Penting', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    # Field yang ditampilkan saat create user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'full_name', 'email', 'role'),
        }),
    )

# 2. Admin untuk Mahasiswa
class MahasiswaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nim', 'get_full_name', 'program_studi', 'angkatan', 'no_hp')
    list_filter = ('program_studi', 'angkatan')
    search_fields = ('nim', 'user__username', 'user__full_name', 'id')
    raw_id_fields = ('user',)
    readonly_fields = ('id',)
    
    def get_full_name(self, obj):
        return obj.user.full_name if obj.user else '-'
    get_full_name.short_description = 'Nama Lengkap'
    get_full_name.admin_order_field = 'user__full_name'

# 3. Admin untuk PeriodeYudisium
class PeriodeYudisiumAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama_periode', 'tanggal_mulai', 'tanggal_selesai', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('nama_periode', 'id')
    readonly_fields = ('id',)

# 4. Admin untuk PendaftaranYudisium
class PendaftaranYudisiumAdmin(admin.ModelAdmin):
    list_display = ('id', 'mahasiswa', 'periode', 'tanggal_daftar', 'status_akhir')
    list_filter = ('status_akhir', 'periode')
    search_fields = ('mahasiswa__nim', 'mahasiswa__user__full_name', 'id')
    raw_id_fields = ('mahasiswa', 'periode')
    readonly_fields = ('id', 'tanggal_daftar')

# 5. Admin untuk TranskripNilai
class TranskripNilaiAdmin(admin.ModelAdmin):
    list_display = ('id', 'pendaftaran', 'status', 'validated_by', 'validated_at')
    list_filter = ('status',)
    search_fields = ('pendaftaran__mahasiswa__nim', 'id')
    raw_id_fields = ('pendaftaran', 'validated_by')
    readonly_fields = ('id', 'validated_at')

# 6. Admin untuk BerkasAkademik
class BerkasAkademikAdmin(admin.ModelAdmin):
    list_display = ('id', 'pendaftaran', 'status', 'validated_by', 'validated_at')
    list_filter = ('status',)
    search_fields = ('pendaftaran__mahasiswa__nim', 'id')
    raw_id_fields = ('pendaftaran', 'validated_by')
    readonly_fields = ('id', 'validated_at')

# 7. Admin untuk BebasPerpus
class BebasPerpusAdmin(admin.ModelAdmin):
    list_display = ('id', 'pendaftaran', 'status', 'validated_by', 'validated_at')
    list_filter = ('status',)
    search_fields = ('pendaftaran__mahasiswa__nim', 'id')
    raw_id_fields = ('pendaftaran', 'validated_by')
    readonly_fields = ('id', 'validated_at')

# 8. Admin untuk Notifikasi
class NotifikasiAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'judul', 'tipe', 'created_at', 'is_read')
    list_filter = ('tipe', 'is_read')
    search_fields = ('user__username', 'judul', 'id')
    raw_id_fields = ('user',)
    readonly_fields = ('id', 'created_at')

# 9. Admin untuk MataKuliah
class MataKuliahAdmin(admin.ModelAdmin):
    list_display = ( 'kode', 'nama', 'sks', 'jurusan', 'kategori')
    list_filter = ('jurusan', 'kategori')
    search_fields = ('kode', 'nama')
    readonly_fields = ('kode',)

# 10. Admin untuk PendaftaranYudisiumFinal
class PendaftaranYudisiumFinalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nim', 'nama_lengkap', 'periode', 'status', 'tanggal_daftar')
    list_filter = ('status', 'periode')
    search_fields = ('nim', 'nama_lengkap', 'nik', 'id')
    raw_id_fields = ('mahasiswa', 'periode')
    readonly_fields = ('id', 'tanggal_daftar', 'tanggal_verifikasi')
    fieldsets = (
        ('Data Diri', {
            'fields': ('nama_lengkap', 'nim', 'tempat_lahir', 'tanggal_lahir', 'nik')
        }),
        ('Data Orang Tua', {
            'fields': ('nama_ibu_kandung', 'nama_bapak_kandung')
        }),
        ('Status Pendaftaran', {
            'fields': ('status', 'catatan_baak', 'tanggal_daftar', 'tanggal_verifikasi')
        }),
    )

# 11. Admin untuk RiwayatPendaftaranYudisium
class RiwayatPendaftaranYudisiumAdmin(admin.ModelAdmin):
    list_display = ('id', 'pendaftaran', 'status_sebelum', 'status_sesudah', 'petugas', 'tanggal')
    list_filter = ('status_sebelum', 'status_sesudah')
    search_fields = ('pendaftaran__nim', 'id')
    raw_id_fields = ('pendaftaran', 'petugas')
    readonly_fields = ('id', 'tanggal')

# 12. Admin untuk TtdPetugas
class TtdPetugasAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama_petugas', 'jabatan', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('nama_petugas', 'jabatan', 'id')
    readonly_fields = ('id', 'created_at')

# ============================================
# REGISTER SEMUA MODEL
# ============================================

# Unregister User bawaan Django jika sudah terdaftar
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# Register dengan custom admin
admin.site.register(User, CustomUserAdmin)
admin.site.register(Mahasiswa, MahasiswaAdmin)
admin.site.register(TtdPetugas, TtdPetugasAdmin)
admin.site.register(PeriodeYudisium, PeriodeYudisiumAdmin)
admin.site.register(PendaftaranYudisium, PendaftaranYudisiumAdmin)
admin.site.register(TranskripNilai, TranskripNilaiAdmin)
admin.site.register(BerkasAkademik, BerkasAkademikAdmin)
admin.site.register(BebasPerpus, BebasPerpusAdmin)
admin.site.register(Notifikasi, NotifikasiAdmin)
admin.site.register(MataKuliah, MataKuliahAdmin)
admin.site.register(PendaftaranYudisiumFinal, PendaftaranYudisiumFinalAdmin)
admin.site.register(RiwayatPendaftaranYudisium, RiwayatPendaftaranYudisiumAdmin)

# ============================================
# KONFIGURASI ADMIN SITE
# ============================================

admin.site.site_header = 'Sistem Yudisium Administration'
admin.site.site_title = 'Sistem Yudisium'
admin.site.index_title = 'Dashboard Sistem Yudisium'