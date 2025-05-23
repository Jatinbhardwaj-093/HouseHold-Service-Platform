import { createRouter, createWebHistory } from 'vue-router';
import WebsiteHome from '@/views/WebsiteHomeView.vue';
import LoginView from '@/views/LoginView.vue';
import SignUpView from '@/views/SignUpView.vue';
import CustomerSignUpView from '@/views/CustomerSignUpView.vue';
import CustomerHomeView from '@/views/CustomerHomeView.vue';
import Customer_ServiceView from '@/views/Customer_ServiceView.vue';
import ParticularService from '@/components/Customer/ParticularService.vue';
import CustomerStatisticsView from '@/views/Customer_StatsView.vue';
import AdminHomeView from '@/views/AdminHomeView.vue';
import Admin_ProfessionalDetailView from '@/views/Admin_ProfessionalDetailView.vue';
import Admin_CustomerDetailView from '@/views/Admin_CustomerDetailView.vue';
import Admin_OngoinServiceView from '@/views/Admin_OngoinServiceView.vue';
import Admin_StatsView from '@/views/Admin_StatsView.vue';
import ProffesionalSignUp from '@/views/ProffesionalSignUp.vue';
import ProffesionalHomeView from '@/views/Professional_HomeView.vue';
import ProfessionalHistory from '@/views/Professional_HistoryView.vue';
import ProfessionalStatisticsView from '@/views/Professional_StatsView.vue';


const routes = [
  {
    path: '/',
    name: 'home',
    component: WebsiteHome
  },
  {
    path: '/login',
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
    path: '/admin/statistics',
    name: 'admin-statistics',
    component: Admin_StatsView,
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
    path: '/customer/services',
    name: 'customer-services',
    component: Customer_ServiceView,
    meta: { requiresAuth: true, role: 'customer' }
  },
  {
    path: '/customer/service/:serviceId',
    name: 'customer-particular-service',
    component: ParticularService,
    meta: { requiresAuth: true, role: 'customer' }
  },
  {
    path: '/customer/statistics',
    name: 'customer-statistics',
    component: CustomerStatisticsView,
    meta: { requiresAuth: true, role: 'customer' }
  },
  {
    path: '/professional',
    name: 'professional',
    component: ProffesionalHomeView,
    meta: { requiresAuth: true, role: 'professional' }
  },
  {
    path: '/proffessional/signup',
    name: 'proffessional-signup',
    component: ProffesionalSignUp,
  },
  {
    path: '/proffessional/history',
    name: 'professional-history',
    component: ProfessionalHistory,
    meta: { requiresAuth: true, role: 'professional' }
  },
  {
    path: '/proffessional/statistics',
    name: 'professional-statistics',
    component: ProfessionalStatisticsView,
    meta: { requiresAuth: true, role: 'professional' }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const adminToken = localStorage.getItem('adminToken');
  const professionalToken = localStorage.getItem('professionalToken');
  const customerToken = localStorage.getItem('customerToken');

  // Map tokens based on roles
  const roleTokenMap = {
    admin: adminToken,
    professional: professionalToken,
    customer: customerToken,
  };

  const userRole = to.meta.role; // Role required by the route

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!userRole || !roleTokenMap[userRole]) {
      // Redirect to login if no role or valid token for role
      next({ path: '/' });
    } else {
      next();
    }
  } else {
    next();
  }
});


export default router;
