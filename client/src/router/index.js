import { createRouter, createWebHistory } from 'vue-router';
import ModelView from '../views/ModelView.vue';

const routes = [
  {
    path: '/',
    name: 'model',
    component: ModelView,
  },
  {
    path: '/upload',
    name: 'upload',
    component: () => import('../views/UploadView.vue'),
  },
  {
    path: '/model/:modelID',
    name: 'modelID',
    component: () => import('../views/ModelIDView.vue'),
  },
  {
    path: '/test/:modelID',
    name: 'test',
    component: () => import('../views/TestView.vue'),
  },
  {
    path: '/service/:modelID',
    name: 'service',
    component: () => import('../views/ServiceView.vue'),
  },
  {
    path: '/predict/:modelID/:serviceID',
    name: 'predict',
    component: () => import('../views/PredictView.vue'),
  },
  {
    path: '/batch/:modelID/:serviceID',
    name: 'batch',
    component: () => import('../views/BatchView.vue'),
  },
  {
    path: '/task/:modelID/:serviceID/:taskID',
    name: 'task',
    component: () => import('../views/TaskIDView.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  // chrome
  document.body.scrollTop = 0;
  // firefox
  document.documentElement.scrollTop = 0;
  // safari
  window.pageYOffset = 0;
  next();
});

export default router;
