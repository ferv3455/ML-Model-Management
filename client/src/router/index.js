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
    path: '/predict/:modelID',
    name: 'predict',
    component: () => import('../views/PredictView.vue'),
  },
  {
    path: '/batch/:modelID',
    name: 'batch',
    component: () => import('../views/BatchView.vue'),
  },
  {
    path: '/task/:modelID/:taskID',
    name: 'task',
    component: () => import('../views/TaskIDView.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
