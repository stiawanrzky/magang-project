"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from sistem_yudisium.views import (
    UserViewSet, MahasiswaViewSet, PeriodeYudisiumViewSet,
    PendaftaranYudisiumViewSet, TranskripNilaiViewSet,BebasPerpusViewSet, NotifikasiViewSet, BerkasAkademikViewSet, MataKuliahViewSet, BAAKViewSet,PendaftaranYudisiumFinalViewSet,PendaftaranYudisiumFinalCreateSerializer, 
    generate_surat_pdf,
    upload_ttd,
    get_ttd,delete_ttd,
    get_logo
)

# 1. Inisialisasi Router untuk API
router = DefaultRouter()
# PERBAIKAN: Menghilangkan tanda koma (,) di akhir setiap baris
router.register(r'users', UserViewSet)
router.register(r'mahasiswa', MahasiswaViewSet)
router.register(r'periode-yudisium', PeriodeYudisiumViewSet, basename='periode-yudisium')
router.register(r'pendaftaran', PendaftaranYudisiumViewSet, basename='pendaftaran')
router.register(r'akademik', BerkasAkademikViewSet)
router.register(r'transkrip-nilai', TranskripNilaiViewSet, basename='transkrip-nilai')
router.register(r'bebas-perpus', BebasPerpusViewSet)
router.register(r'notifikasi', NotifikasiViewSet)
router.register(r'matakuliah', MataKuliahViewSet, basename='matakuliah')
router.register(r'baak', BAAKViewSet, basename='baak')
router.register(r'pendaftaran-yudisium', PendaftaranYudisiumFinalViewSet, basename='pendaftaran-yudisium')


# 2. Pengaturan URL Utama
urlpatterns = [
    # Akses Panel Admin: http://127.0.0.1:8000/admin/
    path('admin/', admin.site.urls),

    # Akses Dashboard API: http://127.0.0.1:8000/api/
    path('api/', include(router.urls)),

    # --- ENDPOINT UNTUK LOGIN ---
    # Gunakan path ini di Vue: api.post('token/', ...)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Endpoint untuk memperbarui token yang kadaluarsa
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/generate-surat-pdf/', generate_surat_pdf, name='generate-surat-pdf'),
    path('api/upload-ttd/', upload_ttd, name='upload-ttd'),
    path('api/ttd-perpus/', get_ttd, name='get-ttd'),
    path('api/delete-ttd/', delete_ttd, name='delete_ttd'),
    path('api/get-logo/', get_logo, name='get_logo'),
    path('api/notifikasi/', NotifikasiViewSet.as_view({'get': 'list'}), name='notifikasi'),
    path('api/notifikasi/<int:pk>/baca/', NotifikasiViewSet.as_view({'post': 'tandai_baca'}), name='notifikasi-baca'),
   
]

# 3. Konfigurasi Static & Media (Untuk file upload)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)