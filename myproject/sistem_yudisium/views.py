import os
import uuid
import base64
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
from PIL import Image
import textwrap
from .models import *
from .serializers import *

User = get_user_model()
# ========== TAMBAHKAN FUNGSI INI DI BAGIAN ATAS views.py ==========
def buat_notifikasi(user, judul, pesan, tipe='INFO'):
    """Helper function untuk membuat notifikasi"""
    try:
        if not user:
            print("User tidak valid")
            return
        from .models import Notifikasi
        notif = Notifikasi.objects.create(
            user=user,
            judul=judul,
            pesan=pesan,
            tipe=tipe,
            is_read=False
        )
        print(f"✅ Notifikasi dibuat untuk {user.username}: {judul}")
        return notif
    except Exception as e:
        print(f"❌ Gagal membuat notifikasi: {e}")
        return None
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'register']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if 'full_name' in request.data:
                user.full_name = request.data['full_name']
                user.save()

            if user.role == 'MAHASISWA':
                mhs, created = Mahasiswa.objects.get_or_create(user=user, defaults={'nim': user.username})
                mhs.program_studi = request.data.get('prodi', '-')
                angkatan_req = request.data.get('angkatan')
                if angkatan_req:
                    mhs.angkatan = int(angkatan_req)
                mhs.save()

            return Response({
                "message": f"Akun {user.username} berhasil dibuat!",
                "username": user.username
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'PATCH':
            new_email = request.data.get('email')
            if new_email:
                request.user.email = new_email
                request.user.save()
                return Response({"message": "Email berhasil diupdate!"}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(request.user)
        response_data = dict(serializer.data)
        
        if request.user.role == 'MAHASISWA':
            try:
                mhs = Mahasiswa.objects.get(user=request.user)
                response_data['angkatan'] = mhs.angkatan
                response_data['prodi'] = mhs.program_studi
            except ObjectDoesNotExist:
                response_data['angkatan'] = '-'
                response_data['prodi'] = '-'
                
        return Response(response_data, status=status.HTTP_200_OK)
        

class MahasiswaViewSet(viewsets.ModelViewSet):
    queryset = Mahasiswa.objects.all()
    serializer_class = MahasiswaSerializer
    permission_classes = [IsAuthenticated]


# ================================================================
# CLASS PendaftaranYudisiumViewSet (PERBAIKI INI)
# ================================================================
class PendaftaranYudisiumViewSet(viewsets.ModelViewSet):
    queryset = PendaftaranYudisium.objects.all()
    serializer_class = PendaftaranYudisiumSerializer
    permission_classes = [IsAuthenticated]

    def get_file_url(self, request, file_field):
        """Helper untuk mendapatkan URL lengkap dari file"""
        if not file_field:
            return None
        try:
            if hasattr(file_field, 'url'):
                return request.build_absolute_uri(file_field.url)
            elif isinstance(file_field, str) and file_field:
                return request.build_absolute_uri(f'/media/{file_field}')
            return None
        except Exception as e:
            print(f"Error getting file URL: {e}")
            return None

    @action(detail=False, methods=['get'], url_path='status_saya')
    def status_saya(self, request):
        try:
            mhs = Mahasiswa.objects.get(user=request.user)
            periode = PeriodeYudisium.objects.filter(is_active=True).first()
            
            if not periode:
                return Response({
                    "error": "Belum ada periode yudisium aktif",
                    "transkrip": {"status": "MENUNGGU", "catatan": "", "sudah_upload": False},
                    "perpus": {"status": "MENUNGGU", "catatan": "", "sudah_upload": False, "files": {}, "link_surat_pdf": None},
                    "akademik": {"status": "MENUNGGU", "catatan": "", "sudah_upload": False}
                })

            pendaftaran = PendaftaranYudisium.objects.filter(mahasiswa=mhs, periode=periode).first()
            
            if not pendaftaran:
                pendaftaran = PendaftaranYudisium.objects.create(mahasiswa=mhs, periode=periode)

            berkas_akademik, _ = BerkasAkademik.objects.get_or_create(pendaftaran=pendaftaran)
            transkrip = TranskripNilai.objects.filter(pendaftaran=pendaftaran).first()
            perpus = BebasPerpus.objects.filter(pendaftaran=pendaftaran).first()

            # Perbaikan untuk perpustakaan
            perpus_sudah_upload = False
            perpus_files = {}
            link_surat_url = None
            
            if perpus:
                # Cek file abstrak
                if perpus.file_abstrak:
                    perpus_sudah_upload = True
                
                # Cek 11 file PDF
                file_fields = [
                    'bagian_awal', 'bab1', 'bab2', 'bab3', 'bab4', 'bab5',
                    'daftar_pustaka', 'lampiran', 'jurnal_publikasi',
                    'lampiran_cetak', 'cek_plagiasi_jurnal'
                ]
                for field in file_fields:
                    file_obj = getattr(perpus, field)
                    if file_obj:
                        perpus_sudah_upload = True
                        perpus_files[field] = self.get_file_url(request, file_obj)
                
                # KRUSIAL: Ambil link_surat_pdf dengan benar
                if perpus.link_surat_pdf:
                    link_surat_url = self.get_file_url(request, perpus.link_surat_pdf)

            response_data = {
                "full_name": getattr(mhs, 'nama', request.user.full_name), 
                "status_akhir": getattr(pendaftaran, 'status_akhir', 'PROSES'),
                "transkrip": {
                    "status": getattr(transkrip, 'status', 'MENUNGGU'),
                    "catatan": getattr(transkrip, 'catatan_baak', ''),
                    "sudah_upload": bool(transkrip and transkrip.data_nilai),
                    "data_nilai": getattr(transkrip, 'data_nilai', []) 
                },
                "perpus": {
                    "status": getattr(perpus, 'status', 'MENUNGGU'),
                    "catatan": getattr(perpus, 'catatan_perpus', ''),
                    "sudah_upload": perpus_sudah_upload,
                    "file_abstrak": self.get_file_url(request, getattr(perpus, 'file_abstrak', None)),
                    "files": perpus_files,
                    "validated_at": getattr(perpus, 'validated_at', None),
                    "link_surat_pdf": link_surat_url,
                    "petugas_nama": getattr(perpus.validated_by, 'full_name', None) if perpus and hasattr(perpus, 'validated_by') and perpus.validated_by else None
                },
                "akademik": {
                    "status": getattr(berkas_akademik, 'status', 'MENUNGGU'),
                    "catatan": getattr(berkas_akademik, 'catatan_akademik', ''),
                    "sudah_upload": bool(berkas_akademik.foto_ijazah or berkas_akademik.foto_akte),
                    "files": {
                        "ijazah": self.get_file_url(request, berkas_akademik.foto_ijazah),
                        "akte": self.get_file_url(request, berkas_akademik.foto_akte),
                        "ktp": self.get_file_url(request, berkas_akademik.foto_ktp),
                        "foto3x4": self.get_file_url(request, berkas_akademik.foto_3x4),
                    }
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist as e:
            return Response({"error": f"Data tidak ditemukan: {str(e)}"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"❌ Error di status_saya: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='upload-akademik')
    def upload_akademik(self, request):
        try:
            mhs = Mahasiswa.objects.get(user=request.user)
            periode = PeriodeYudisium.objects.filter(is_active=True).first()
            if not periode:
                return Response({"error": "Belum ada periode yudisium aktif"}, status=400)

            pendaftaran, created = PendaftaranYudisium.objects.get_or_create(mahasiswa=mhs, periode=periode)
            
            ijazah = request.FILES.get('foto_ijazah')
            akte = request.FILES.get('foto_akte')
            ktp = request.FILES.get('foto_ktp')
            foto_3x4 = request.FILES.get('foto_3x4')
            
            ada_perubahan = False

            if ijazah:
                pendaftaran.foto_ijazah = ijazah
                ada_perubahan = True
            if akte:
                pendaftaran.foto_akte = akte
                ada_perubahan = True
            if ktp:
                pendaftaran.foto_ktp = ktp
                ada_perubahan = True
            if foto_3x4:
                pendaftaran.foto_3x4 = foto_3x4
                ada_perubahan = True
                
            if ada_perubahan:
                pendaftaran.status_akademik = 'MENUNGGU'
                pendaftaran.save()
                
                berkas, _ = BerkasAkademik.objects.get_or_create(pendaftaran=pendaftaran)
                if ijazah:
                    berkas.foto_ijazah = ijazah
                if akte:
                    berkas.foto_akte = akte
                if ktp:
                    berkas.foto_ktp = ktp
                if foto_3x4:
                    berkas.foto_3x4 = foto_3x4
                berkas.status = 'MENUNGGU'
                berkas.save()

                return Response({"message": "Berhasil upload berkas akademik!"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Tidak ada file yang diterima."}, status=status.HTTP_400_BAD_REQUEST)
            
        except Mahasiswa.DoesNotExist:
            return Response({"error": "Data mahasiswa tidak ditemukan"}, status=404)
        except Exception as e:
            print(f"Error upload akademik: {str(e)}")
            return Response({"error": f"Kesalahan: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ================================================================
# FUNGSI get_surat_perpus (di LUAR class, sebagai @api_view)
# ================================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_surat_perpus(request):
    """Endpoint khusus untuk mendapatkan surat bebas perpustakaan"""
    try:
        mahasiswa = Mahasiswa.objects.get(user=request.user)
        periode = PeriodeYudisium.objects.filter(is_active=True).first()
        
        if not periode:
            return Response({
                "success": False,
                "message": "Tidak ada periode aktif",
                "link_surat_pdf": None
            })
        
        pendaftaran = PendaftaranYudisium.objects.filter(
            mahasiswa=mahasiswa, periode=periode
        ).first()
        
        if not pendaftaran:
            return Response({
                "success": False,
                "message": "Pendaftaran tidak ditemukan",
                "link_surat_pdf": None
            })
        
        bebas_perpus = BebasPerpus.objects.filter(pendaftaran=pendaftaran).first()
        
        if bebas_perpus and bebas_perpus.link_surat_pdf:
            # Bangun URL lengkap
            pdf_url = request.build_absolute_uri(bebas_perpus.link_surat_pdf.url)
            return Response({
                "success": True,
                "link_surat_pdf": pdf_url,
                "status": bebas_perpus.status,
                "validated_at": bebas_perpus.validated_at
            })
        else:
            return Response({
                "success": False,
                "message": "Surat PDF belum tersedia",
                "link_surat_pdf": None
            })
            
    except Mahasiswa.DoesNotExist:
        return Response({
            "success": False,
            "message": "Data mahasiswa tidak ditemukan",
            "link_surat_pdf": None
        })
    except Exception as e:
        return Response({
            "success": False,
            "message": str(e),
            "link_surat_pdf": None
        })

class PeriodeYudisiumViewSet(viewsets.ModelViewSet):
    queryset = PeriodeYudisium.objects.all()
    serializer_class = PeriodeYudisiumSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['patch'])
    def toggle_active(self, request, pk=None):
        periode = self.get_object()
        # Jika ingin mengaktifkan, nonaktifkan periode lain yang aktif
        if request.data.get('is_active') == True:
            PeriodeYudisium.objects.filter(is_active=True).exclude(pk=pk).update(is_active=False)
        periode.is_active = not periode.is_active  # atau dari request
        periode.save()
        serializer = self.get_serializer(periode)
        return Response(serializer.data)

class TranskripNilaiViewSet(viewsets.ModelViewSet):
    queryset = TranskripNilai.objects.all()
    serializer_class = TranskripNilaiSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='simpan-spreadsheet')
    def simpan_spreadsheet(self, request):
        try: 
            mhs = Mahasiswa.objects.get(user=request.user)
            
            periode = PeriodeYudisium.objects.filter(is_active=True).first()
            if not periode:
                return Response({"error": "Belum ada periode yudisium yang aktif. Hubungi Admin."}, status=status.HTTP_400_BAD_REQUEST)

            pendaftaran, created = PendaftaranYudisium.objects.get_or_create(mahasiswa=mhs, periode=periode)
            
            data_nilai_dari_vue = request.data.get('data_nilai', [])
            
            transkrip, t_created = TranskripNilai.objects.update_or_create(
                pendaftaran=pendaftaran,
                defaults={
                    'data_nilai': data_nilai_dari_vue, 
                    'status': 'MENUNGGU',
                    'catatan_baak': ''
                }
            )
            return Response({"message": "Data nilai berhasil disimpan!"}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @action(detail=True, methods=['patch', 'post'], url_path='verifikasi')
    def verifikasi(self, request, pk=None):
        """BAAK verifikasi transkrip nilai"""
        if request.user.role not in ['BAAK', 'SUPERADMIN']:
            return Response({"error": "Hanya petugas BAAK"}, status=403)
        
        try:
            transkrip = self.get_object()
        except Exception:
            return Response({"error": "Data tidak ditemukan"}, status=404)
        
        status_baru = request.data.get('status')
        catatan = request.data.get('catatan_baak', '')
        
        if not status_baru:
            return Response({"error": "Status harus diisi"}, status=400)
        
        if status_baru == 'DITOLAK' and not catatan:
            return Response({"error": "Alasan penolakan wajib diisi"}, status=400)
        
        transkrip.status = status_baru
        transkrip.catatan_baak = catatan
        transkrip.validated_at = timezone.now()
        transkrip.validated_by = request.user
        transkrip.save()
        
        # Kirim notifikasi
        if transkrip.pendaftaran and transkrip.pendaftaran.mahasiswa:
            mahasiswa_user = transkrip.pendaftaran.mahasiswa.user
            if status_baru == 'DISETUJUI':
                buat_notifikasi(
                    mahasiswa_user,
                    "✅ Transkrip Nilai Disetujui",
                    f"Transkrip nilai Anda telah disetujui oleh BAAK.",
                    "VALIDASI_DITERIMA"
                )
            else:
                buat_notifikasi(
                    mahasiswa_user,
                    "❌ Transkrip Nilai Ditolak",
                    f"Transkrip nilai Anda ditolak. Catatan: {catatan}",
                    "VALIDASI_DITOLAK"
                )
        
        return Response({
            'success': True,
            'message': f'Verifikasi berhasil',
            'status': status_baru
        })
class BebasPerpusViewSet(viewsets.ModelViewSet):
    queryset = BebasPerpus.objects.all()
    serializer_class = BebasPerpusSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='upload')
    def upload_perpus(self, request):
        try:
            mhs = Mahasiswa.objects.get(user=request.user)
            periode = PeriodeYudisium.objects.filter(is_active=True).first()
            if not periode:
                return Response({"error": "Tidak ada periode yudisium aktif"}, status=400)

            pendaftaran, _ = PendaftaranYudisium.objects.get_or_create(mahasiswa=mhs, periode=periode)
            
            # Siapkan data untuk update_or_create
            defaults_data = {
                'status': 'MENUNGGU',
                'catatan_perpus': None
            }
            
            # Upload file abstrak PDF
            file_abstrak = request.FILES.get('file_abstrak')
            if file_abstrak:
                if not file_abstrak.name.lower().endswith('.pdf'):
                    return Response({"error": "File abstrak harus berformat PDF"}, status=400)
                if file_abstrak.size > 5 * 1024 * 1024:
                    return Response({"error": "Ukuran file abstrak maksimal 5MB"}, status=400)
                defaults_data['file_abstrak'] = file_abstrak
            
            # Upload 11 file lainnya
            file_keys = [
                'bagian_awal', 'bab1', 'bab2', 'bab3', 'bab4', 'bab5', 
                'daftar_pustaka', 'lampiran', 'jurnal_publikasi', 
                'lampiran_cetak', 'cek_plagiasi_jurnal'
            ]

            for key in file_keys:
                if key in request.FILES:
                    file_obj = request.FILES[key]
                    if file_obj.name.lower().endswith('.pdf'):
                        defaults_data[key] = file_obj

            # Eksekusi simpan ke database
            BebasPerpus.objects.update_or_create(
                pendaftaran=pendaftaran,
                defaults=defaults_data
            )
            
            return Response({"message": "Berhasil mengunggah data perpustakaan!"}, status=status.HTTP_200_OK)
            
        except Mahasiswa.DoesNotExist:
            return Response({"error": "Data mahasiswa tidak ditemukan"}, status=404)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'patch'], url_path='verifikasi')
    def verifikasi(self, request, pk=None):
        """Perpustakaan verifikasi berkas (setuju/tolak) dengan notifikasi"""
        print("="*50)
        print("🔥 VERIFIKASI PERPUSTAKAAN DIPANGGIL!")
        print(f"User: {request.user.username}")
        print(f"Data: {request.data}")
        print("="*50)
        
        # Hanya Petugas Perpustakaan atau SUPERADMIN
        if request.user.role not in ['PERPUS', 'SUPERADMIN']:
            return Response({"error": "Hanya petugas Perpustakaan"}, status=403)
        
        try:
            bebas_perpus = self.get_object()
            mahasiswa = bebas_perpus.pendaftaran.mahasiswa
            print(f"✅ Ditemukan untuk mahasiswa: {mahasiswa.user.username}")
        except Exception as e:
            print(f"❌ Error: {e}")
            return Response({"error": "Data tidak ditemukan"}, status=404)
        
        status_baru = request.data.get('status')
        catatan = request.data.get('catatan_perpus', '')
        
        if not status_baru:
            return Response({"error": "Status harus diisi"}, status=400)
        
        if status_baru == 'DITOLAK' and not catatan:
            return Response({"error": "Alasan penolakan wajib diisi"}, status=400)
        
        # Update status
        bebas_perpus.status = status_baru
        bebas_perpus.catatan_perpus = catatan if status_baru == 'DITOLAK' else ''
        bebas_perpus.validated_at = timezone.now() if status_baru == 'DISETUJUI' else None
        bebas_perpus.validated_by = request.user if status_baru == 'DISETUJUI' else None
        bebas_perpus.save()
        
        # ========== KIRIM NOTIFIKASI KE MAHASISWA ==========
        mahasiswa_user = mahasiswa.user
        
        if status_baru == 'DISETUJUI':
            buat_notifikasi(
                mahasiswa_user,
                "✅ Berkas Perpustakaan Disetujui",
                f"Berkas perpustakaan Anda telah disetujui oleh {request.user.full_name}. Surat bebas perpustakaan akan segera diterbitkan.",
                "VALIDASI_DITERIMA"
            )
        else:  # DITOLAK
            buat_notifikasi(
                mahasiswa_user,
                "❌ Berkas Perpustakaan Ditolak",
                f"Berkas perpustakaan Anda ditolak. Catatan: {catatan}. Silakan perbaiki dan upload ulang.",
                "VALIDASI_DITOLAK"
            )
        
        return Response({
            'success': True,
            'message': f'Berkas perpustakaan berhasil {status_baru}',
            'status': status_baru,
            'catatan': catatan
        }, status=200)

    @api_view(['GET'])
    def get_surat_perpus(request):
        """Endpoint khusus untuk mendapatkan surat bebas perpustakaan"""
        try:
            mahasiswa = Mahasiswa.objects.get(user=request.user)
            periode = PeriodeYudisium.objects.filter(is_active=True).first()
            
            if not periode:
                return Response({
                    "success": False,
                    "message": "Tidak ada periode aktif",
                    "link_surat_pdf": None
                })
            
            pendaftaran = PendaftaranYudisium.objects.filter(
                mahasiswa=mahasiswa, periode=periode
            ).first()
            
            if not pendaftaran:
                return Response({
                    "success": False,
                    "message": "Pendaftaran tidak ditemukan",
                    "link_surat_pdf": None
                })
            
            bebas_perpus = BebasPerpus.objects.filter(pendaftaran=pendaftaran).first()
            
            if bebas_perpus and bebas_perpus.link_surat_pdf:
                # Bangun URL lengkap
                pdf_url = request.build_absolute_uri(bebas_perpus.link_surat_pdf.url)
                return Response({
                    "success": True,
                    "link_surat_pdf": pdf_url,
                    "status": bebas_perpus.status,
                    "validated_at": bebas_perpus.validated_at
                })
            else:
                return Response({
                    "success": False,
                    "message": "Surat PDF belum tersedia",
                    "link_surat_pdf": None
                })
                
        except Mahasiswa.DoesNotExist:
            return Response({
                "success": False,
                "message": "Data mahasiswa tidak ditemukan",
                "link_surat_pdf": None
            })
        except Exception as e:
            return Response({
                "success": False,
                "message": str(e),
                "link_surat_pdf": None
            })
    # views.py - Pastikan fungsi-fungsi ini ada di bagian bawah file

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ttd(request):
    """Endpoint untuk mendapatkan tanda tangan petugas"""
    try:
        ttd_dir = os.path.join(settings.MEDIA_ROOT, 'yudisium/ttd/')
        if os.path.exists(ttd_dir):
            files = os.listdir(ttd_dir)
            prefix = f"ttd_{request.user.id}_"
            for file in files:
                if file.startswith(prefix):
                    return Response({'ttd_url': f'/media/yudisium/ttd/{file}'})
        return Response({'ttd_url': None})
    except:
        return Response({'ttd_url': None})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_ttd(request):
    """Endpoint untuk upload tanda tangan petugas"""
    try:
        ttd_file = request.FILES.get('ttd')
        if not ttd_file:
            return Response({'error': 'No file uploaded'}, status=400)
        
        upload_dir = 'yudisium/ttd/'
        ttd_full_dir = os.path.join(settings.MEDIA_ROOT, upload_dir)
        if not os.path.exists(ttd_full_dir):
            os.makedirs(ttd_full_dir)
        
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        unique_id = uuid.uuid4().hex[:8]
        ext = ttd_file.name.split('.')[-1].lower()
        if ext not in ['png', 'jpg', 'jpeg']:
            ext = 'png'
        
        filename = f"ttd_{request.user.id}_{timestamp}_{unique_id}.{ext}"
        ttd_path = os.path.join(upload_dir, filename)
        saved_path = default_storage.save(ttd_path, ttd_file)
        
        return Response({'success': True, 'ttd_url': saved_path})
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_ttd(request):
    """Endpoint untuk menghapus tanda tangan petugas"""
    try:
        ttd_dir = os.path.join(settings.MEDIA_ROOT, 'yudisium/ttd/')
        if os.path.exists(ttd_dir):
            files = os.listdir(ttd_dir)
            prefix = f"ttd_{request.user.id}_"
            for file in files:
                if file.startswith(prefix):
                    file_path = os.path.join(ttd_dir, file)
                    try:
                        os.remove(file_path)
                    except:
                        pass
        return Response({'success': True})
    except:
        return Response({'success': True})
        


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_surat_pdf(request):
    """Endpoint untuk generate PDF surat bebas perpustakaan"""
    print("=" * 50)
    print("🚀 generate_surat_pdf DIPANGGIL!")
    print("=" * 50)
    
    try:
        # Ambil data dari request
        pengajuan_id = request.POST.get('pengajuan_id')
        nim = request.POST.get('nim')
        email_mahasiswa = request.POST.get('email')
        full_name = request.POST.get('full_name')
        prodi = request.POST.get('prodi', '')
        catatan_perpus = request.POST.get('catatan_perpus', '')
        ttd_position_x = request.POST.get('ttd_position_x', 85)
        ttd_position_y = request.POST.get('ttd_position_y', 85)
        ttd_petugas = request.POST.get('ttd_petugas', '')
        ttd_base64 = request.POST.get('ttd_base64', '')
        
        print(f"📝 Data: nim={nim}, nama={full_name}, prodi={prodi}")
        print(f"📝 TTD Base64 ada: {bool(ttd_base64)}")
        print(f"📝 TTD petugas path: {ttd_petugas}")
        
        # Cari data di database
        from .models import BebasPerpus, PendaftaranYudisium, Mahasiswa, PeriodeYudisium, Notifikasi
        
        bebas_perpus = None
        
        if pengajuan_id and pengajuan_id != 'null' and pengajuan_id != 'undefined':
            try:
                bebas_perpus = BebasPerpus.objects.get(id=pengajuan_id)
                print(f"✅ Ditemukan via pengajuan_id: {pengajuan_id}")
            except BebasPerpus.DoesNotExist:
                pass
        
        if not bebas_perpus and nim:
            try:
                mahasiswa = Mahasiswa.objects.get(nim=nim)
                periode = PeriodeYudisium.objects.filter(is_active=True).first()
                if periode:
                    pendaftaran = PendaftaranYudisium.objects.filter(
                        mahasiswa=mahasiswa, periode=periode
                    ).first()
                    if pendaftaran:
                        bebas_perpus = BebasPerpus.objects.filter(
                            pendaftaran=pendaftaran
                        ).first()
                        if bebas_perpus:
                            print(f"✅ Ditemukan via nim: {nim}")
            except Exception as e:
                print(f"Error mencari mahasiswa: {e}")
        
        if not bebas_perpus:
            return Response({'error': 'Pengajuan tidak ditemukan'}, status=404)
        
        # Buat direktori
        upload_dir = 'yudisium/surat_perpus/'
        full_upload_dir = os.path.join(settings.MEDIA_ROOT, upload_dir)
        if not os.path.exists(full_upload_dir):
            os.makedirs(full_upload_dir)
        
        # Nama file PDF
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        unique_id = uuid.uuid4().hex[:8]
        filename = f"surat_bebas_perpus_{nim}_{timestamp}_{unique_id}.pdf"
        pdf_path = os.path.join(full_upload_dir, filename)
        
        # ========== GENERATE PDF DENGAN REPORTLAB ==========
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.utils import ImageReader
        from PIL import Image
        import textwrap
        import base64
        from io import BytesIO
        from datetime import datetime
        
        c = canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4
        
        # Margin
        margin_left = 50
        margin_right = width - 50
        y_position = height - 50
        
        # ========== 1. LOGO ==========
        logo_loaded = False
        logo_paths_to_try = [
            os.path.join(settings.MEDIA_ROOT, 'stie-sbilogo.png'),
            os.path.join(settings.MEDIA_ROOT, 'stie-sbilogo.jpg'),
            os.path.join(settings.BASE_DIR, 'media', 'stie-sbilogo.png'),
        ]
        
        for logo_path in logo_paths_to_try:
            if logo_path and os.path.exists(logo_path):
                try:
                    logo = ImageReader(logo_path)
                    c.drawImage(logo, margin_left, y_position - 50, width=50, height=50, preserveAspectRatio=True)
                    logo_loaded = True
                    print(f"✅ Logo ditemukan di: {logo_path}")
                    break
                except Exception as e:
                    print(f"Gagal load logo: {e}")
        
        if not logo_loaded:
            print("⚠️ Logo tidak ditemukan, lanjut tanpa logo")
        
        # ========== 2. HEADER TEKS ==========
        text_x = margin_left + 60 if logo_loaded else margin_left
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(text_x, y_position - 10, "PERPUSTAKAAN")
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(text_x, y_position - 30, "STIE SOLUSI BISNIS INDONESIA YOGYAKARTA")
        
        c.setFont("Helvetica", 9)
        c.drawString(text_x, y_position - 45, "Jl. Ring Road Utara No. 17, Condongcatur, Depok, Sleman, Yogyakarta 55283")
        c.drawString(text_x + 20, y_position - 55, "Telp. (0274) 887984 | Email: perpustakaan@stie-sbi.ac.id")
        
        # Garis pemisah
        c.line(margin_left, y_position - 70, margin_right, y_position - 70)
        c.line(margin_left, y_position - 73, margin_right, y_position - 73)
        
        # ========== 3. JUDUL SURAT ==========
        y_position -= 100
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width/2, y_position, "SURAT BEBAS PINJAMAN PUSTAKA")
        
        # ========== 4. ISI SURAT ==========
        y_position -= 40
        c.setFont("Helvetica", 11)
        
        text1 = "Surat ini diberikan untuk permohonan mahasiswa yang sudah menyelesaikan semua biaya administrasi/denda :"
        lines = textwrap.wrap(text1, 80)
        for line in lines:
            c.drawString(margin_left, y_position, line)
            y_position -= 15
        
        y_position -= 10
        
        text2 = "Identitas pemohon surat bebas pinjam pustaka ini :"
        c.drawString(margin_left, y_position, text2)
        y_position -= 25
        
        c.setFont("Helvetica", 11)
        c.drawString(margin_left + 20, y_position, f"Nama                         : {full_name or '[NAMA]'}")
        y_position -= 20
        c.drawString(margin_left + 20, y_position, f"No. Mahasiswa          : {nim or '[NIM]'}")
        y_position -= 20
        c.drawString(margin_left + 20, y_position, f"Jurusan                      : {prodi or 'Akuntansi'}")
        y_position -= 30
        
        text3 = "Semoga surat ini dapat memenuhi keperluan diatas."
        c.drawString(margin_left, y_position, text3)
        
        # ========== 5. TANGGAL ==========
        y_position -= 60
        bulan_indonesia = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 
                          'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
        now = datetime.now()
        tanggal_str = f"{now.day} {bulan_indonesia[now.month-1]} {now.year}"
        c.drawRightString(margin_right, y_position, f"Yogyakarta, {tanggal_str}")
        
        # ========== 6. TANDA TANGAN ==========
        # Posisi untuk TTD (setelah tanggal)
        ttd_y_position = y_position - 40
        ttd_processed = False
        
        # --- PROSES GAMBAR TTD ---
        
        # Opsi 1: TTD dari Base64 (dari preview frontend)
        if ttd_base64 and ttd_base64.startswith('data:image'):
            try:
                print("🖼️ Memproses TTD dari Base64...")
                if 'base64,' in ttd_base64:
                    img_data = base64.b64decode(ttd_base64.split('base64,')[1])
                else:
                    img_data = base64.b64decode(ttd_base64)
                
                img = Image.open(BytesIO(img_data))
                
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                ttd_temp_path = os.path.join(full_upload_dir, f"ttd_temp_{unique_id}.png")
                img.save(ttd_temp_path, 'PNG')
                
                # Hitung posisi X berdasarkan persentase
                ttd_x = margin_left + (int(ttd_position_x) / 100) * (margin_right - margin_left - 80)
                
                # Gambar TTD
                ttd_img = ImageReader(ttd_temp_path)
                c.drawImage(ttd_img, ttd_x, ttd_y_position - 20, width=60, height=35, 
                           preserveAspectRatio=True, mask='auto')
                
                os.remove(ttd_temp_path)
                ttd_processed = True
                print(f"✅ TTD Base64 diproses, posisi X={ttd_position_x}%")
            except Exception as e:
                print(f"❌ Gagal proses TTD base64: {e}")
        
        # Opsi 2: TTD dari path server (yang sudah diupload)
        if not ttd_processed and ttd_petugas:
            try:
                print(f"🔍 Mencari TTD di server: {ttd_petugas}")
                full_ttd_path = os.path.join(settings.MEDIA_ROOT, ttd_petugas)
                
                if os.path.exists(full_ttd_path):
                    print(f"  ✅ File TTD ditemukan!")
                    ttd_x = margin_left + (int(ttd_position_x) / 100) * (margin_right - margin_left - 80)
                    ttd_img = ImageReader(full_ttd_path)
                    c.drawImage(ttd_img, ttd_x, ttd_y_position - 20, width=60, height=35, 
                               preserveAspectRatio=True, mask='auto')
                    ttd_processed = True
                    print(f"✅ TTD dari server diproses")
                else:
                    print(f"  ❌ File tidak ditemukan di: {full_ttd_path}")
                    
                    # Coba cari di folder ttd
                    ttd_dir = os.path.join(settings.MEDIA_ROOT, 'yudisium/ttd')
                    if os.path.exists(ttd_dir):
                        print(f"  Mencari di folder: {ttd_dir}")
                        for file in os.listdir(ttd_dir):
                            if file.endswith(('.png', '.jpg', '.jpeg')):
                                print(f"    Menemukan file: {file}")
                                full_ttd_path = os.path.join(ttd_dir, file)
                                ttd_x = margin_left + (int(ttd_position_x) / 100) * (margin_right - margin_left - 80)
                                ttd_img = ImageReader(full_ttd_path)
                                c.drawImage(ttd_img, ttd_x, ttd_y_position - 20, width=60, height=35, 
                                           preserveAspectRatio=True, mask='auto')
                                ttd_processed = True
                                print(f"✅ TTD ditemukan di folder ttd: {file}")
                                break
            except Exception as e:
                print(f"❌ Gagal proses TTD dari path: {e}")
        
        if not ttd_processed:
            print("⚠️ TTD TIDAK DIPROSES - hanya menampilkan nama petugas")
        
        # --- NAMA PETUGAS DAN JABATAN ---
        petugas_nama = request.user.full_name or request.user.username
        
        # Geser posisi nama petugas ke bawah jika ada gambar TTD
        nama_offset = 10 if ttd_processed else 10
        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(margin_right, ttd_y_position - 15 + nama_offset, petugas_nama)
        
        c.setFont("Helvetica", 9)
        c.drawRightString(margin_right, ttd_y_position - 30 + nama_offset, "Pustakawan")
        
        # ========== 7. CATATAN TAMBAHAN ==========
        if catatan_perpus and catatan_perpus.strip():
            catatan_y = ttd_y_position - 70
            c.setFont("Helvetica", 9)
            c.drawString(margin_left, catatan_y, f"Catatan: {catatan_perpus}")
        
        # Simpan PDF
        c.save()
        print(f"✅ PDF tersimpan di: {pdf_path}")
        
        # ========== 8. UPDATE DATABASE ==========
        relative_path = os.path.join(upload_dir, filename).replace('\\', '/')
        
        bebas_perpus.link_surat_pdf = relative_path
        bebas_perpus.status = 'DISETUJUI'
        bebas_perpus.validated_at = timezone.now()
        bebas_perpus.validated_by = request.user
        bebas_perpus.ttd_position_x = int(ttd_position_x)
        bebas_perpus.ttd_position_y = int(ttd_position_y)
        
        if ttd_petugas:
            bebas_perpus.ttd_petugas = ttd_petugas
        
        if catatan_perpus and catatan_perpus.strip():
            bebas_perpus.catatan_perpus = catatan_perpus
        
        bebas_perpus.save()
        
        # ========== 9. BUAT NOTIFIKASI ==========
        try:
            if bebas_perpus.pendaftaran and bebas_perpus.pendaftaran.mahasiswa:
                mahasiswa_user = bebas_perpus.pendaftaran.mahasiswa.user
                Notifikasi.objects.create(
                    user=mahasiswa_user,
                    judul="📑 Surat Bebas Perpustakaan Telah Terbit",
                    pesan=f"Surat keterangan bebas perpustakaan Anda telah diterbitkan.",
                    tipe='SURAT_BEBAS_PERPUS',
                    is_read=False
                )
                print(f"✅ Notifikasi dikirim ke: {mahasiswa_user.username}")
        except Exception as notif_error:
            print(f"Gagal buat notifikasi: {notif_error}")
        
        # Buat URL untuk response
        request_scheme = request.scheme
        request_host = request.get_host()
        full_pdf_url = f"{request_scheme}://{request_host}/media/{relative_path}"
        
        return Response({
            'success': True,
            'message': 'Surat PDF berhasil di-generate',
            'pdf_url': full_pdf_url,
            'saved_path': relative_path
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_logo(request):
    """Endpoint untuk mendapatkan logo dari backend"""
    try:
        # Cari logo di folder media
        logo_paths = [
            os.path.join(settings.MEDIA_ROOT, 'stie-sbilogo.png'),
            os.path.join(settings.MEDIA_ROOT, 'stie-sbilogo.jpg'),
            os.path.join(settings.MEDIA_ROOT, 'logo.png'),
        ]
        
        for logo_path in logo_paths:
            if os.path.exists(logo_path):
                logo_url = request.build_absolute_uri(settings.MEDIA_URL + os.path.basename(logo_path))
                return Response({'success': True, 'logo_url': logo_url})
        
        return Response({'success': False, 'logo_url': None})
    except Exception as e:
        return Response({'success': False, 'logo_url': None, 'error': str(e)})

class NotifikasiViewSet(viewsets.ModelViewSet):
    queryset = Notifikasi.objects.all()
    serializer_class = NotifikasiSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notifikasi.objects.filter(user=self.request.user).order_by('-created_at')

    @action(detail=False, methods=['get'], url_path='belum_dibaca')
    def belum_dibaca(self, request):
        """Endpoint untuk mendapatkan notifikasi yang belum dibaca"""
        notifikasi_belum_dibaca = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(notifikasi_belum_dibaca, many=True)
        return Response({
            "count": notifikasi_belum_dibaca.count(),
            "results": serializer.data
        })

    @action(detail=True, methods=['post'], url_path='baca')
    def tandai_baca(self, request, pk=None):
        """Endpoint untuk menandai notifikasi sebagai sudah dibaca"""
        notifikasi = self.get_object()
        notifikasi.is_read = True
        notifikasi.save()
        return Response({"message": "Notifikasi ditandai sudah dibaca"})

    @action(detail=False, methods=['post'], url_path='baca_semua')
    def baca_semua(self, request):
        """Endpoint untuk menandai semua notifikasi sebagai sudah dibaca"""
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({"message": "Semua notifikasi ditandai sudah dibaca"})

class BerkasAkademikViewSet(viewsets.ModelViewSet):
    queryset = BerkasAkademik.objects.all() 
    serializer_class = BerkasAkademikSerializer
    permission_classes = [IsAuthenticated]

    def get_file_url(self, request, file_field):
        if not file_field: return None
        return request.build_absolute_uri(file_field.url)

    @action(detail=False, methods=['get'], url_path='list-mahasiswa')
    def mahasiswa(self, request):
        if request.user.role not in ['AKADEMIK', 'SUPERADMIN']:
            return Response({"error": "Akses ditolak"}, status=status.HTTP_403_FORBIDDEN)

        semua_mhs = Mahasiswa.objects.all()
        data = []
        for mhs in semua_mhs:
            pendaftaran = PendaftaranYudisium.objects.filter(mahasiswa=mhs).last()
            if not pendaftaran:
                continue  # lewati jika belum ada pendaftaran

            berkas, created = BerkasAkademik.objects.get_or_create(pendaftaran=pendaftaran)

            # Hanya tampilkan jika sudah ada minimal satu file yang diupload
            if (berkas.foto_ijazah or berkas.foto_akte or
                berkas.foto_ktp or berkas.foto_3x4):
                data.append({
                    "id": pendaftaran.id,
                    "mahasiswa_id": mhs.id,
                    "full_name": mhs.user.full_name,
                    "nim": mhs.nim,
                    "prodi": getattr(mhs, 'program_studi', '-'),
                    "status_akademik": berkas.status or "MENUNGGU",
                    "catatan_akademik": berkas.catatan_akademik or "",
                    "foto_ijazah": self.get_file_url(request, berkas.foto_ijazah),
                    "foto_akte": self.get_file_url(request, berkas.foto_akte),
                    "foto_ktp": self.get_file_url(request, berkas.foto_ktp),
                    "foto_3x4": self.get_file_url(request, berkas.foto_3x4),
                })

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='verifikasi-berkas')
    def verifikasi_berkas(self, request):
        mhs_id = request.data.get('mahasiswa_id')
        status_baru = request.data.get('status')
        catatan = request.data.get('catatan', '')

        try:
            pendaftaran = PendaftaranYudisium.objects.filter(mahasiswa_id=mhs_id).last()
            if not pendaftaran:
                return Response({"error": "Pendaftaran tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

            berkas, _ = BerkasAkademik.objects.get_or_create(pendaftaran=pendaftaran)
            berkas.status = status_baru
            berkas.catatan_akademik = catatan
            berkas.save()

            pendaftaran.status_akademik = status_baru
            pendaftaran.catatan_akademik = catatan
            pendaftaran.save()
            # ========== KIRIM NOTIFIKASI KE MAHASISWA ==========
            if pendaftaran.mahasiswa:
                mahasiswa_user = pendaftaran.mahasiswa.user
                
                if status_baru == 'DISETUJUI':
                    judul = "✅ Berkas Akademik Disetujui"
                    pesan = f"Berkas akademik Anda telah disetujui oleh {request.user.full_name}. Pendaftaran Anda sudah lengkap."
                    tipe = 'VALIDASI_DITERIMA'
                else:
                    judul = "❌ Berkas Akademik Ditolak"
                    pesan = f"Berkas akademik Anda ditolak. Catatan: {catatan}. Silakan perbaiki dan upload ulang."
                    tipe = 'VALIDASI_DITOLAK'
                
                buat_notifikasi(mahasiswa_user, judul, pesan, tipe)

            return Response({"message": "Berhasil memperbarui status!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# =========================================================================
# VIEWSET UNTUK MATA KULIAH BAAK
# =========================================================================
class MataKuliahViewSet(viewsets.ModelViewSet):
    queryset = MataKuliah.objects.all()
    serializer_class = MataKuliahSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'kode' # PENTING: Agar bisa Edit dan Hapus berdasarkan "Kode MK"

# =========================================================================
# VIEWSET UNTUK DASHBOARD BAAK
# =========================================================================
class BAAKViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='berkas-masuk')
    def berkas_masuk(self, request):
        transkrip = TranskripNilai.objects.all().order_by('-id')
        data = []
        for item in transkrip:
            # Pengecekan aman menggunakan getattr
            if getattr(item, 'pendaftaran', None) and getattr(item.pendaftaran, 'mahasiswa', None):
                mhs = item.pendaftaran.mahasiswa
                
                # Pengecekan aman apakah user punya full_name
                full_name = "Tanpa Nama"
                if hasattr(mhs, 'user') and hasattr(mhs.user, 'full_name'):
                    full_name = mhs.user.full_name

                # Pengecekan aman jika file_transkrip terhapus
                file_url = None
                if hasattr(item, 'file_transkrip') and item.file_transkrip:
                    file_url = item.file_transkrip.url
                    
                data.append({
                    "id": item.id,
                    "full_name": full_name,
                    "nim": getattr(mhs, 'nim', ''),
                    "data_nilai": getattr(item, 'data_nilai', []),
                    "status": getattr(item, 'status', 'MENUNGGU'),
                    "catatan": getattr(item, 'catatan_baak', ''),
                    "file_transkrip": file_url
                })
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='daftar-mahasiswa')
    def daftar_mahasiswa(self, request):
        mhs_list = Mahasiswa.objects.all()
        data = []
        for mhs in mhs_list:
            pendaftaran = PendaftaranYudisium.objects.filter(mahasiswa=mhs).last()
            
            transkrip = TranskripNilai.objects.filter(pendaftaran=pendaftaran).last() if pendaftaran else None
            perpus = BebasPerpus.objects.filter(pendaftaran=pendaftaran).last() if pendaftaran else None
            akademik = BerkasAkademik.objects.filter(pendaftaran=pendaftaran).last() if pendaftaran else None
            
            full_name = mhs.user.full_name if hasattr(mhs, 'user') and hasattr(mhs.user, 'full_name') else "Tanpa Nama"

            data.append({
                "id": mhs.id,
                "full_name": full_name,
                "nim": getattr(mhs, 'nim', ''),
                "status_transkrip": getattr(transkrip, 'status', 'BELUM'),
                "status_perpus": getattr(perpus, 'status', 'BELUM'),
                "status_akademik": getattr(akademik, 'status', 'BELUM'),
            })
        return Response(data, status=status.HTTP_200_OK)


class PendaftaranYudisiumFinalViewSet(viewsets.ModelViewSet):
    serializer_class = PendaftaranYudisiumFinalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'MAHASISWA':
            try:
                mahasiswa = Mahasiswa.objects.get(user=user)
                return PendaftaranYudisiumFinal.objects.filter(mahasiswa=mahasiswa)
            except Mahasiswa.DoesNotExist:
                return PendaftaranYudisiumFinal.objects.none()
        elif user.role in ['SUPERADMIN', 'BAAK', 'AKADEMIK']:
            return PendaftaranYudisiumFinal.objects.all().order_by('-tanggal_daftar')
        return PendaftaranYudisiumFinal.objects.none()
    
    @action(detail=False, methods=['post'], url_path='daftar')
    def daftar_yudisium(self, request):
        """Endpoint untuk mahasiswa mendaftar yudisium"""
        try:
            mahasiswa = Mahasiswa.objects.get(user=request.user)
            
            periode = PeriodeYudisium.objects.filter(is_active=True).first()
            if not periode:
                return Response({"error": "Tidak ada periode yudisium aktif"}, status=400)
            
            pendaftaran, _ = PendaftaranYudisium.objects.get_or_create(
                mahasiswa=mahasiswa, periode=periode
            )
            
            # Cek status semua bagian
            transkrip_ok = hasattr(pendaftaran, 'transkrip') and pendaftaran.transkrip.status == 'DISETUJUI'
            perpus_ok = hasattr(pendaftaran, 'perpus') and pendaftaran.perpus.status == 'DISETUJUI'
            akademik_ok = hasattr(pendaftaran, 'akademik') and pendaftaran.akademik.status == 'DISETUJUI'
            
            if not (transkrip_ok and perpus_ok and akademik_ok):
                return Response({
                    "error": "Belum semua berkas selesai divalidasi",
                    "status": {
                        "transkrip": pendaftaran.transkrip.status if hasattr(pendaftaran, 'transkrip') else 'BELUM',
                        "perpus": pendaftaran.perpus.status if hasattr(pendaftaran, 'perpus') else 'BELUM',
                        "akademik": pendaftaran.akademik.status if hasattr(pendaftaran, 'akademik') else 'BELUM'
                    }
                }, status=400)
            
            existing = PendaftaranYudisiumFinal.objects.filter(mahasiswa=mahasiswa).first()
            if existing:
                return Response({
                    "error": "Anda sudah pernah mendaftar yudisium",
                    "status": existing.status,
                    "tanggal_daftar": existing.tanggal_daftar
                }, status=400)
            
            serializer = PendaftaranYudisiumFinalCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            
            pendaftaran_final = PendaftaranYudisiumFinal.objects.create(
                mahasiswa=mahasiswa,
                periode=periode,
                nama_lengkap=serializer.validated_data['nama_lengkap'],
                nim=serializer.validated_data['nim'],
                tempat_lahir=serializer.validated_data['tempat_lahir'],
                tanggal_lahir=serializer.validated_data['tanggal_lahir'],
                nik=serializer.validated_data['nik'],
                nama_ibu_kandung=serializer.validated_data['nama_ibu_kandung'],
                nama_bapak_kandung=serializer.validated_data['nama_bapak_kandung'],
                status='MENUNGGU'
            )
            
            baak_users = User.objects.filter(role__in=['SUPERADMIN', 'BAAK'])
            for baak in baak_users:
                Notifikasi.objects.create(
                    user=baak,
                    judul="Pendaftaran Yudisium Baru",
                    pesan=f"Mahasiswa {mahasiswa.user.full_name} ({mahasiswa.nim}) telah mendaftar yudisium."
                )

            Notifikasi.objects.create(
                user=request.user,
                judul="Pendaftaran Yudisium Berhasil",
                pesan="Pendaftaran yudisium Anda telah dikirim ke BAAK untuk diverifikasi."
            )
            
            return Response({
                "success": True,
                "message": "Pendaftaran yudisium berhasil dikirim",
                "data": PendaftaranYudisiumFinalSerializer(pendaftaran_final).data
            }, status=201)
            
        except Mahasiswa.DoesNotExist:
            return Response({"error": "Data mahasiswa tidak ditemukan"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
    
    @action(detail=True, methods=['post', 'patch', 'put'], permission_classes=[permissions.IsAuthenticated])
    def verifikasi(self, request, pk=None):
        """
        BAAK memberikan komentar/catatan dan mengubah status pendaftaran menjadi DISETUJUI
        """
        if request.user.role not in ['BAAK', 'SUPERADMIN']:
            return Response({"error": "Hanya petugas BAAK yang dapat memberikan catatan yudisium"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            pendaftaran = self.get_object()
        except Exception:
            return Response({"error": "Data Pendaftaran tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

        catatan = request.data.get('catatan_baak', '')
        status_baru = request.data.get('status', 'DISETUJUI')
        
        if not catatan:
            return Response({"error": "Komentar/Catatan tidak boleh kosong"}, status=status.HTTP_400_BAD_REQUEST)

        # ========== PERBAIKAN UTAMA ==========
        # Update Catatan, Status, dan Tanggal Verifikasi
        pendaftaran.catatan_baak = catatan
        pendaftaran.status = status_baru
        pendaftaran.tanggal_verifikasi = timezone.now()
        pendaftaran.save()

        # Catat Riwayat Perubahan
        RiwayatPendaftaranYudisium.objects.create(
            pendaftaran=pendaftaran,
            status_sebelum='MENUNGGU',
            status_sesudah=status_baru,
            catatan=f"BAAK memberikan komentar: {catatan}",
            petugas=request.user
        )

        # Buat Notifikasi untuk Mahasiswa
        try:
            if hasattr(pendaftaran, 'mahasiswa') and hasattr(pendaftaran.mahasiswa, 'user'):
                Notifikasi.objects.create(
                    user=pendaftaran.mahasiswa.user, 
                    judul="✅ Pendaftaran Yudisium Diverifikasi",
                    pesan=f"Pendaftaran yudisium Anda telah diverifikasi. Catatan: {catatan}",
                    is_read=False
                )
        except Exception as e:
            print(f"Gagal membuat notifikasi: {e}")

        # Kembalikan data lengkap
        serializer = self.get_serializer(pendaftaran)
        
        return Response({
            "message": "Pendaftaran berhasil diverifikasi",
            "status": status_baru,
            "catatan_baak": pendaftaran.catatan_baak,
            "tanggal_verifikasi": pendaftaran.tanggal_verifikasi,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='cek-status')
    def cek_status_pendaftaran(self, request):
        """Cek status pendaftaran yudisium mahasiswa"""
        try:
            mahasiswa = Mahasiswa.objects.get(user=request.user)
            periode = PeriodeYudisium.objects.filter(is_active=True).first()
            
            if not periode:
                return Response({"sudah_daftar": False, "bisa_daftar": False})
            
            pendaftaran = PendaftaranYudisium.objects.filter(
                mahasiswa=mahasiswa, periode=periode
            ).first()
            
            if pendaftaran:
                transkrip_ok = hasattr(pendaftaran, 'transkrip') and pendaftaran.transkrip.status == 'DISETUJUI'
                perpus_ok = hasattr(pendaftaran, 'perpus') and pendaftaran.perpus.status == 'DISETUJUI'
                akademik_ok = hasattr(pendaftaran, 'akademik') and pendaftaran.akademik.status == 'DISETUJUI'
                semua_berkas_ok = transkrip_ok and perpus_ok and akademik_ok
            else:
                semua_berkas_ok = False
            
            pendaftaran_final = PendaftaranYudisiumFinal.objects.filter(mahasiswa=mahasiswa).first()
            
            return Response({
                "sudah_daftar": pendaftaran_final is not None,
                "bisa_daftar": semua_berkas_ok and pendaftaran_final is None,
                "status_pendaftaran": pendaftaran_final.status if pendaftaran_final else None,
                "tanggal_daftar": pendaftaran_final.tanggal_daftar if pendaftaran_final else None,
                "catatan_baak": pendaftaran_final.catatan_baak if pendaftaran_final else None,
                "status_berkas": {
                    "transkrip": pendaftaran.transkrip.status if pendaftaran and hasattr(pendaftaran, 'transkrip') else 'BELUM',
                    "perpus": pendaftaran.perpus.status if pendaftaran and hasattr(pendaftaran, 'perpus') else 'BELUM',
                    "akademik": pendaftaran.akademik.status if pendaftaran and hasattr(pendaftaran, 'akademik') else 'BELUM'
                } if pendaftaran else None
            })
            
        except Mahasiswa.DoesNotExist:
            return Response({"sudah_daftar": False, "bisa_daftar": False})
        except Exception as e:
            return Response({"sudah_daftar": False, "bisa_daftar": False, "error": str(e)})