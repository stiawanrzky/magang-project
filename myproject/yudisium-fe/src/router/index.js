import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue' 
import DashboardBAAK from '../views/DashboardBAAK.vue'
import DashboardMhs from '../views/DashboardMhs.vue'
import DashboardAkademik from '../views/DashboardAkademik.vue'
import DashboardPerpus from '../views/DashboardPerpus.vue' // Tambahkan import ini
import DashboardAdmin from '../views/DashboardAdmin.vue'   // Tambahkan import ini

const routes = [
  { path: '/login', name: 'login', component: Login },
  { path: '/register', name: 'register', component: Register },
  { path: '/', redirect: '/login' },
  { 
    path: '/dashboard-baak',
    name: 'dashboardBAAK',
    component: DashboardBAAK,
    meta: { requiresAuth: true, role: 'BAAK' }
  },
  { 
    path: '/dashboard-mhs', 
    name: 'dashboardMhs', 
    component: DashboardMhs, 
    meta: { requiresAuth: true, role: 'MAHASISWA' } 
  },
  { 
    path: '/dashboard-akademik', 
    name: 'dashboardAkademik', 
    component: DashboardAkademik, 
    meta: { requiresAuth: true, role: 'AKADEMIK' } 
  },
  {
    path: '/dashboard-perpus',
    name: 'dashboardPerpus', 
    component: DashboardPerpus, // Diubah agar menggunakan import di atas
    meta: { requiresAuth: true, role: 'PERPUS' }
  }, // Tanda koma ditambahkan di sini agar tidak error
  {
    path: '/dashboard-admin',
    name: 'dashboardAdmin', 
    component: DashboardAdmin, // Diubah agar menggunakan import di atas
    meta: { requiresAuth: true, role: 'SUPERADMIN' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation Guard (Satpam)
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');
  const userRole = (localStorage.getItem('user_role') || '').toUpperCase();

  if (to.meta.requiresAuth) {
    if (!token) {
      return next({ name: 'login' });
    }
    
    if (to.meta.role && to.meta.role !== userRole) {
      if (userRole === 'MAHASISWA') return next({ name: 'dashboardMhs' });
      if (userRole === 'BAAK')  return next({ name: 'dashboardBAAK' });
      if (userRole === 'AKADEMIK') return next({ name: 'dashboardAkademik' });
      if (userRole === 'PERPUS') return next({ name: 'dashboardPerpus' });
      if (userRole === 'SUPERADMIN') return next({ name: 'dashboardAdmin' });
      return next({ name: 'login' });
    }
  }

  if (to.name === 'login' && token) {
     if (userRole === 'MAHASISWA') return next({ name: 'dashboardMhs' });
      if (userRole === 'BAAK')  return next({ name: 'dashboardBAAK' });
      if (userRole === 'AKADEMIK') return next({ name: 'dashboardAkademik' });
      if (userRole === 'PERPUS') return next({ name: 'dashboardPerpus' });
      if (userRole === 'SUPERADMIN') return next({ name: 'dashboardAdmin' });
  }

  next();
});

export default router;