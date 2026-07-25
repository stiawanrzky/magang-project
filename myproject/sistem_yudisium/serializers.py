from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # Deklarasi password agar hanya bisa diisi (POST) tapi tidak ditampilkan (GET)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'full_name', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Menggunakan create_user agar password otomatis di-hash
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ''),
            role=validated_data.get('role', 'MAHASISWA')
        )
        return user


class MahasiswaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahasiswa
        fields = '__all__'


class PeriodeYudisiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodeYudisium
        fields = ['id', 'nama_periode', 'tanggal_mulai', 'tanggal_selesai', 'is_active']
        read_only_fields = ['id']


class PendaftaranYudisiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendaftaranYudisium
        fields = '__all__'
    

# =======================================================================
# NEW SERIALIZER: Menangani format data master Tanda Tangan Petugas
# =======================================================================
class TtdPetugasSerializer(serializers.ModelSerializer):
    class Meta:
        model = TtdPetugas
        fields = ['id', 'nama_petugas', 'jabatan', 'file_ttd', 'is_active', 'created_at']


class TranskripNilaiSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='pendaftaran.mahasiswa.user.full_name', read_only=True)
    nim = serializers.CharField(source='pendaftaran.mahasiswa.nim', read_only=True)
    program_studi = serializers.CharField(source='pendaftaran.mahasiswa.program_studi', read_only=True)

    class Meta:
        model = TranskripNilai
        fields = [
            'id', 'pendaftaran', 'full_name', 'nim', 'program_studi',
            'data_nilai', 'status', 'catatan_baak', 'validated_by', 'validated_at'
        ]


class BerkasAkademikSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='pendaftaran.mahasiswa.user.full_name', read_only=True)
    nim = serializers.CharField(source='pendaftaran.mahasiswa.nim', read_only=True)

    class Meta:
        model = BerkasAkademik
        fields = [
            'id', 'pendaftaran', 'full_name', 'nim',
            'status', 'catatan_akademik',
            'foto_ijazah', 'foto_akte', 'foto_ktp', 'foto_3x4',
            'validated_by', 'validated_at'
        ]


class BebasPerpusSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='pendaftaran.mahasiswa.user.full_name', read_only=True)
    nim = serializers.CharField(source='pendaftaran.mahasiswa.nim', read_only=True)
    jurusan = serializers.CharField(source='pendaftaran.mahasiswa.program_studi', read_only=True, default='')
    petugas_nama = serializers.SerializerMethodField()
    validated_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = BebasPerpus
        fields = [
            'id', 'pendaftaran', 'full_name', 'nim', 'jurusan', 
            'status', 'catatan_perpus', 'file_abstrak',
            'bagian_awal', 'bab1', 'bab2', 'bab3', 'bab4', 'bab5',
            'daftar_pustaka', 'lampiran', 'jurnal_publikasi',
            'lampiran_cetak', 'cek_plagiasi_jurnal',
            'link_surat_pdf', 'ttd_petugas', 'ttd_position_x', 'ttd_position_y',
            'validated_at', 'validated_at_formatted', 'petugas_nama'
        ]
    
    def get_petugas_nama(self, obj):
        """Ambil nama petugas yang memvalidasi"""
        if hasattr(obj, 'validated_by') and obj.validated_by:
            return obj.validated_by.full_name
        return None
    
    def get_validated_at_formatted(self, obj):
        """Format tanggal validasi"""
        if obj.validated_at:
            return obj.validated_at.strftime('%d %B %Y %H:%M')
        return None
        
        


class NotifikasiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifikasi
        fields = '__all__'


class MataKuliahSerializer(serializers.ModelSerializer):
    class Meta:
        model = MataKuliah
        fields = '__all__'

class PendaftaranYudisiumFinalSerializer(serializers.ModelSerializer):
    mahasiswa_nama = serializers.CharField(source='mahasiswa.user.full_name', read_only=True)
    
    class Meta:
        model = PendaftaranYudisiumFinal
        fields = [ 'id','mahasiswa_nama', 'periode', 'nama_lengkap', 'nim', 
                  'tempat_lahir', 'tanggal_lahir', 'nik', 'nama_ibu_kandung', 
                  'nama_bapak_kandung', 'status', 'catatan_baak', 'tanggal_daftar',
                  'tanggal_verifikasi']
        read_only_fields = ['id', 'tanggal_daftar', 'tanggal_verifikasi']
class RiwayatPendaftaranYudisiumSerializer(serializers.ModelSerializer):
    petugas_nama = serializers.CharField(source='petugas.full_name', read_only=True)
    
    class Meta:
        model = RiwayatPendaftaranYudisium
        fields = ['id', 'status_sebelum', 'status_sesudah', 'catatan', 'petugas', 
                  'petugas_nama', 'tanggal']
# Tambahkan di bagian bawah file serializers.py, setelah class yang sudah ada

class PendaftaranYudisiumFinalCreateSerializer(serializers.Serializer):
    """Serializer untuk menerima data pendaftaran dari frontend"""
    nama_lengkap = serializers.CharField(max_length=200)
    nim = serializers.CharField(max_length=20)
    tempat_lahir = serializers.CharField(max_length=100)
    tanggal_lahir = serializers.DateField()
    nik = serializers.CharField(max_length=16)
    nama_ibu_kandung = serializers.CharField(max_length=200)
    nama_bapak_kandung = serializers.CharField(max_length=200)
    
    def validate_nik(self, value):
        if not value.isdigit() or len(value) != 16:
            raise serializers.ValidationError("NIK harus 16 digit angka")
        return value