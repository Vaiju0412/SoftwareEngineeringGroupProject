import { createRouter, createWebHistory } from 'vue-router'
import SignUp from './components/SignUp.vue';
import HomePage from './components/HomePage.vue';
import Login from './components/Login.vue';
const routes =[
    {
        name: 'SignUp',
        component: SignUp,
        path: '/',
    },
    {
        name: 'HomePage',
        component: HomePage,
        path: '/homepage',
    },
    {
        name: 'Login',
        component: Login,
        path: '/login',
    }

];
const router = createRouter({
    history:createWebHistory(),
    routes,
});

export default router;