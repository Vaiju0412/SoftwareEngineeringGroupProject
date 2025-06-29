import { createRouter, createWebHistory } from 'vue-router'

// --- Import your components ---
import SignUp from './components/SignUp.vue';
import HomePage from './components/HomePage.vue';
import Login from './components/Login.vue';
import ManageDependents from './components/ManageDependents.vue';
import DependentProfile from './components/DependentProfile.vue';



const routes = [
    // --- Public Routes (No auth required) ---
    {
        name: 'Login',
        component: Login,
        path: '/login',
    },
    {
        name: 'SignUp',
        component: SignUp,
        path: '/signup',
    },
    
    // --- Route for the 'hasSS' redirect target ---
    {
        name: 'ManageDependents',
        component: ManageDependents,
        path: '/caregiver/manage/dependent',
        // This route requires login, but not the 'hasSS' key
        meta: { 
            requiresAuth: false,
            requiresHasSS: false
         }
    },

    // --- Protected Routes ---
    {
        name: 'HomePage',
        component: HomePage,
        path: '/',
        // This route ONLY requires the user to be logged in.
        meta: { 
            requiresAuth: false,
            requiresHasSS: true
        }
    },
    {
        name: 'DependentProfile', // <-- Add the new route
        path: '/profile/:userId', // <-- Dynamic segment for the user ID
        component: DependentProfile,
        meta: { requiresAuth: false, requiresHasSS: false } // Protect this route
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// Global Navigation Guard
router.beforeEach((to, from, next) => {
    // Check if the route requires authentication
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    // Check if the route requires the 'hasSS' key
    const requiresHasSS = to.matched.some(record => record.meta.requiresHasSS);

    // Get status from sessionStorage
    const isLoggedIn = sessionStorage.getItem('isLoggedIn') === 'true';
    const hasSS = sessionStorage.getItem('hasSS') === 'true';

    // --- CHECK 1: LOGIN STATUS ---
    // If route requires auth and user is not logged in, redirect to login page.
    // This is the highest priority check.
    if (requiresAuth && !isLoggedIn) {
        next({ name: 'Login' });
        return; // Stop further execution
    }

    // --- CHECK 2: 'hasSS' STATUS ---
    // If route requires the 'hasSS' key, and the user is logged in, but doesn't have the key,
    // redirect them to the 'add dependent' page.
    if (requiresHasSS && !hasSS) {
        // We use path here as requested. Using a named route is also a good practice.
        next({ path: '/caregiver/manage/dependent' });
        return; // Stop further execution
    }

    // If all checks pass, allow navigation.
    next();
});

export default router;