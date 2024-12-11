import { createRouter, createWebHistory } from 'vue-router';
import Home from './components/Home.vue';
import VideoUploader from './components/VideoUpload.vue';
import Chat from './components/VideoChat.vue';

const routes = [
    { path: '/' ,component: Home},
    { path: '/upload', component: VideoUploader },
    { path: '/chat', component: Chat },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
