from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
# 1. Custom User Model
class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="UUID unik sebagai pengganti integer ID"
    )

    class Role(models.TextChoices):
        MAHASISWA = 'MAHASISWA', 'Mahasiswa'
        BAAK = 'BAAK', 'Bagian Administrasi Akademik Kemahasiswaan'
        AKADEMIK = 'AKADEMIK', 'Akademik'
        PERPUS = 'PERPUS', 'Perpustakaan'
        SUPERADMIN = 'SUPERADMIN', 'Super Admin'

    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=Role.choices)

    def __str__(self):
        return f"{self.username} - {self.role}"

# 2. Model Mahasiswa
class Mahasiswa(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nim = models.CharField(max_length=20, unique=True)
    program_studi = models.CharField(max_length=100)
    angkatan = models.IntegerField()
    no_hp = models.CharField(max_length=15)

    def __str__(self):
        return self.nim

# NEW MASTER MODEL: Model Master Tanda Tangan Petugas / Pejabat (UNTUK SOLUSI GENERATE PDF)
# Model baru ini ditambahkan di bagian atas agar aman dan siap dipanggil oleh serializer/views nanti
class TtdPetugas(models.Model):
    nama_petugas = models.CharField(max_length=150, help_text="Nama Lengkap beserta Gelar")
    jabatan = models.CharField(max_length=100, help_text="Contoh: Ketua Program Studi, Dekan, Kepala Perpus")
    file_ttd = models.ImageField(upload_to='yudisium/ttd_master/', null=True, blank=True, help_text="Upload gambar tanda tangan transparan format PNG")
    is_active = models.BooleanField(default=True, help_text="Set aktif jika petugas ini yang berwenang menandatangani surat sekarang")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tanda Tangan Petugas"
        verbose_name_plural = "Tanda Tangan Petugas"

    def __str__(self):
        return f"{self.nama_petugas} ({self.jabatan}) - {'Aktif' if self.is_active else 'Tidak Aktif'}"


# 3. Model Periode Yudisium
class PeriodeYudisium(models.Model):
    nama_periode = models.CharField(max_length=100)
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nama_periode

# 4. Model Pendaftaran Yudisium
class PendaftaranYudisium(models.Model):
    class StatusAkhir(models.TextChoices):
        MENUNGGU = 'MENUNGGU', 'Menunggu'
        LULUS = 'LULUS', 'Lulus'
        TIDAK_LULUS = 'TIDAK_LULUS', 'Tidak Lulus'

    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE)
    periode = models.ForeignKey(PeriodeYudisium, on_delete=models.CASCADE)
    tanggal_daftar = models.DateTimeField(auto_now_add=True)
    status_akhir = models.CharField(
        max_length=20,
        choices=StatusAkhir.choices,
        default=StatusAkhir.MENUNGGU
    )
    class Meta:
        unique_together = ('mahasiswa', 'periode')

    def __str__(self):
        return f"{self.mahasiswa.nim} - {self.periode.nama_periode}"

# 5. Model Transkrip Nilai (Validasi BAAK)
# models.py - class TranskripNilai

class TranskripNilai(models.Model):
    class Status(models.TextChoices):
        MENUNGGU = 'MENUNGGU', 'Menunggu'
        DISETUJUI = 'DISETUJUI', 'Disetujui'
        DITOLAK = 'DITOLAK', 'Ditolak'

    pendaftaran = models.OneToOneField(PendaftaranYudisium, on_delete=models.CASCADE, related_name='transkrip')
    
    data_nilai = models.JSONField(default=list, blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.MENUNGGU)
    catatan_baak = models.TextField(blank=True, null=True)  # UBAH: dari catatan_dpa menjadi catatan_baak
    
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={'role': 'BAAK'}
    )
    validated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Transkrip - {self.pendaftaran.mahasiswa}"


        

# 6. Berkas Akademik (Yang membuat petugas tidak melihat KOSONG)
class BerkasAkademik(models.Model):
    STATUS_CHOICES = (('MENUNGGU', 'MENUNGGU'), ('DISETUJUI', 'DISETUJUI'), ('DITOLAK', 'DITOLAK'))
    
    pendaftaran = models.OneToOneField(PendaftaranYudisium, on_delete=models.CASCADE, related_name='akademik')
    foto_ijazah = models.FileField(upload_to='yudisium/akademik/', null=True, blank=True)
    foto_akte = models.FileField(upload_to='yudisium/akademik/', null=True, blank=True)
    foto_ktp = models.FileField(upload_to='yudisium/akademik/', null=True, blank=True)
    foto_3x4 = models.FileField(upload_to='yudisium/akademik/', null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='MENUNGGU')
    catatan_akademik = models.TextField(null=True, blank=True)
    validated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    validated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Akademik - {self.pendaftaran.mahasiswa}"

# 7. Model Bebas Perpus

class BebasPerpus(models.Model):
    class Status(models.TextChoices):
        MENUNGGU = 'MENUNGGU', 'Menunggu'
        DISETUJUI = 'DISETUJUI', 'Disetujui'
        DITOLAK = 'DITOLAK', 'Ditolak'

    pendaftaran = models.OneToOneField(PendaftaranYudisium, on_delete=models.CASCADE, related_name='perpus')
    
    # 1. Abstrak - UBAH MENJADI FileField untuk upload PDF
    file_abstrak = models.FileField(upload_to='yudisium/perpus/abstrak/', null=True, blank=True, verbose_name="File Abstrak PDF")
    # Untuk backward compatibility, biarkan field abstrak lama (akan dihapus nanti)
    
    
    # 2. File-file PDF
    bagian_awal = models.FileField(upload_to='yudisium/perpus/awal/', null=True, blank=True)
    bab1 = models.FileField(upload_to='yudisium/perpus/bab1/', null=True, blank=True)
    bab2 = models.FileField(upload_to='yudisium/perpus/bab2/', null=True, blank=True)
    bab3 = models.FileField(upload_to='yudisium/perpus/bab3/', null=True, blank=True)
    bab4 = models.FileField(upload_to='yudisium/perpus/bab4/', null=True, blank=True)
    bab5 = models.FileField(upload_to='yudisium/perpus/bab5/', null=True, blank=True)
    daftar_pustaka = models.FileField(upload_to='yudisium/perpus/pustaka/', null=True, blank=True)
    lampiran = models.FileField(upload_to='yudisium/perpus/lampiran/', null=True, blank=True)
    jurnal_publikasi = models.FileField(upload_to='yudisium/perpus/jurnal/', null=True, blank=True)
    lampiran_cetak = models.FileField(upload_to='yudisium/perpus/lampiran_cetak/', null=True, blank=True)
    cek_plagiasi_jurnal = models.FileField(upload_to='yudisium/perpus/plagiasi_jurnal/', null=True, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.MENUNGGU)
    catatan_perpus = models.TextField(blank=True, null=True) 
    validated_at = models.DateTimeField(null=True, blank=True)
    link_surat_pdf = models.CharField(max_length=500, blank=True, null=True)
    
    ttd_petugas = models.CharField(max_length=500, blank=True, null=True)
    ttd_position_x = models.IntegerField(default=50)
    ttd_position_y = models.IntegerField(default=70)
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={'role__in': ['PERPUS', 'SUPERADMIN']}
    )

    def __str__(self):
        return f"Perpus - {self.pendaftaran.mahasiswa}"

    @property
    def link_surat_pdf_url(self):
        """Property untuk mendapatkan URL lengkap surat PDF"""
        if self.link_surat_pdf:
            from django.templatetags.static import static
            return static(self.link_surat_pdf) if self.link_surat_pdf.startswith('/') else f'/media/{self.link_surat_pdf}'
        return None
    
    def save(self, *args, **kwargs):
        # Pastikan link_surat_pdf disimpan dengan path yang benar
        if self.link_surat_pdf and not self.link_surat_pdf.startswith('yudisium/surat_perpus/'):
            # Jika path sudah diawali dengan /media/, hapus prefix-nya
            if self.link_surat_pdf.startswith('/media/'):
                self.link_surat_pdf = self.link_surat_pdf[7:]
        super().save(*args, **kwargs)

        

# 8. Model Notifikasi
class Notifikasi(models.Model):
    TIPE_CHOICES = [
        ('BERKAS_MASUK', 'Berkas Masuk'),
        ('VALIDASI_DITERIMA', 'Validasi Diterima'),
        ('VALIDASI_DITOLAK', 'Validasi Ditolak'),
        ('SURAT_BEBAS_PERPUS', 'Surat Bebas Perpustakaan'),
        ('PENDAFTARAN_YUDISIUM', 'Pendaftaran Yudisium'),
        ('VERIFIKASI_YUDISIUM', 'Verifikasi Yudisium'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    judul = models.CharField(max_length=200)
    pesan = models.TextField()
    tipe = models.CharField(max_length=50, choices=TIPE_CHOICES, default='BERKAS_MASUK', blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # ← tambahkan baris ini  
    def __str__(self):
        return f"{self.user.username} - {self.judul}"

# =======================================================
# 9. LOGIKA OTOMATISASI (SIGNALS)
# =======================================================

@receiver(post_save, sender=User)
def create_mahasiswa_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'MAHASISWA':
        Mahasiswa.objects.get_or_create(
            user=instance, 
            nim=instance.username, 
            defaults={
                'program_studi': '-',
                'angkatan': 0,
                'no_hp': '-'
            }
        )

@receiver(post_save, sender=User)
def save_mahasiswa_profile(sender, instance, **kwargs):
    if instance.role == 'MAHASISWA' and hasattr(instance, 'mahasiswa'):
        instance.mahasiswa.save()



class MataKuliah(models.Model):
    kode = models.CharField(max_length=50, primary_key=True) 
    nama = models.CharField(max_length=255)
    sks = models.IntegerField(default=2)
    jurusan = models.CharField(max_length=100, default='Semua Jurusan')
    kategori = models.CharField(max_length=50, default='Wajib')
    kelompok = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.kode} - {self.nama}"


class PendaftaranYudisiumFinal(models.Model):
    """Model untuk pendaftaran yudisium setelah semua berkas selesai"""
    STATUS_CHOICES = [
        ('MENUNGGU', 'Menunggu Verifikasi BAAK'),
        ('DISETUJUI', 'Disetujui / Diverifikasi BAAK'),  # PERBAIKAN: Ubah dari DIVERIFIKASI ke DISETUJUI
        ('DITOLAK', 'Ditolak')
    ]
    
    mahasiswa = models.OneToOneField('Mahasiswa', on_delete=models.CASCADE, related_name='pendaftaran_final')
    periode = models.ForeignKey('PeriodeYudisium', on_delete=models.CASCADE, related_name='pendaftaran_final')
    
    # Data diri
    nama_lengkap = models.CharField(max_length=200)
    nim = models.CharField(max_length=20)
    tempat_lahir = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()
    nik = models.CharField(max_length=16, unique=True)
    nama_ibu_kandung = models.CharField(max_length=200)
    nama_bapak_kandung = models.CharField(max_length=200)
    
    # Status pendaftaran
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='MENUNGGU')
    catatan_baak = models.TextField(blank=True, null=True)
    tanggal_daftar = models.DateTimeField(auto_now_add=True)
    tanggal_verifikasi = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Pendaftaran Yudisium Final"
        verbose_name_plural = "Pendaftaran Yudisium Final"
        ordering = ['-tanggal_daftar']
    
    def __str__(self):
        return f"{self.nim} - {self.nama_lengkap}"

class RiwayatPendaftaranYudisium(models.Model):
    """Riwayat perubahan status pendaftaran yudisium"""
    pendaftaran = models.ForeignKey(PendaftaranYudisiumFinal, on_delete=models.CASCADE, related_name='riwayat')
    status_sebelum = models.CharField(max_length=20)
    status_sesudah = models.CharField(max_length=20)
    catatan = models.TextField(blank=True, null=True)
    petugas = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    tanggal = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.pendaftaran.nim} - {self.status_sebelum} → {self.status_sesudah}"