import { createRouter, createWebHistory } from 'vue-router'
//import SignUp from './components/SignUp.vue';
import HomePage from './components/HomePage.vue';
const routes =[
    {
        name: 'HomePage',
        component: HomePage,
        path: '/',
    }
];
const router = createRouter({
    history:createWebHistory(),
    routes,
});

export default router;