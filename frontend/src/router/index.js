import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/components/Home.vue'; 
import VideoUpload from '@/components/VideoUpload.vue'; 
import VideoChat from '@/components/VideoChat.vue'; 

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  
  {
    path: '/upload',
    name: 'Video-to-text',
    component: VideoUpload,
  },
  {
    path: '/chat',
    name: 'VideoChat',
    component: VideoChat,
  },

  {
    path: '/:catchAll(.*)', 
    redirect: '/' 
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  console.log(`Navigating to: ${to.path}`);
  next();
});

export default router;
