import { createRouter, createWebHistory } from 'vue-router'
import SignUp from './components/SignUp.vue';
import HomePage from './components/HomePage.vue';
import Login from './components/Login.vue';

const routes = [
    {
        name: 'SignUp',
        component: SignUp,
        path: '/signup',
        // This route should be accessible to non-logged-in users.
        // No meta field needed.
    },
    {
        name: 'HomePage',
        component: HomePage,
        path: '/',
        // This route requires the user to be logged in.
        // We add a meta field to indicate this.
        meta: { requiresAuth: false }
    },
    {
        name: 'Login',
        component: Login,
        path: '/login',
        // This route should be accessible to non-logged-in users.
        // No meta field needed.
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// Global Navigation Guard
router.beforeEach((to, from, next) => {
    // 1. Check if the route requires authentication.
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

    // 2. Get the logged-in status from sessionStorage.
    //    Note: sessionStorage stores strings, so we check against 'true'.
    const isLoggedIn = sessionStorage.getItem('isLoggedIn') === 'true';

    // 3. If the route requires auth and the user is NOT logged in,
    //    redirect to the login page.
    if (requiresAuth && !isLoggedIn) {
        next({ name: 'Login' });
    } else {
        // 4. Otherwise, allow the navigation to proceed.
        //    This covers routes that don't require auth, or routes
        //    that do require auth and the user is logged in.
        next();
    }
});

export default router;