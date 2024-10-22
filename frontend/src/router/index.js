import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '@/views/LoginView.vue';
import SignUpView from '@/views/SignUpView.vue';
import CustomerHomeView from '@/views/CustomerHomeView.vue';
import CustomerSignUpView from '@/views/CustomerSignUpView.vue';
import AdminHomeView from '@/views/AdminHomeView.vue';
import Admin_ProfessionalDetailView from '@/views/Admin_ProfessionalDetailView.vue';
import Admin_CustomerDetailView from '@/views/Admin_CustomerDetailView.vue';
import Admin_OngoinServiceView from '@/views/Admin_OngoinServiceView.vue';

const routes = [
  {
    path: '/',
    name: 'login',
    component: LoginView
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUpView
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminHomeView,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/professional-detail',
    name: 'professional-detail',
    component: Admin_ProfessionalDetailView,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/customer-detail',
    name: 'customer-detail',
    component: Admin_CustomerDetailView,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/ongoing-service',
    name: 'ongoing-service',
    component: Admin_OngoinServiceView,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/customer/signup',
    name: 'customer-signup',
    component: CustomerSignUpView,
  },
  {
    path: '/customer',
    name: 'customer',
    component: CustomerHomeView,
    meta: { requiresAuth: true, role: 'customer' }
  },
  {
    path: '/professional',
    name: 'professional',
    component: AdminHomeView,
    meta: { requiresAuth: true, role: 'professional' }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const userRole = localStorage.getItem('user_role');

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      next({ path: '/' });
    } else if (to.meta.role && to.meta.role !== userRole) {
      next({ path: '/' });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
