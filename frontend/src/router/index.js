import { createRouter, createWebHistory } from "vue-router";
import AllProgramsView from "../views/AllProgramsView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import HomeView from "../views/HomeView.vue";
import AthletesView from "../views/AthletesView.vue";
import ProfileView from "../views/ProfileView.vue";
import SettingsView from "../views/SettingsView.vue";
import WorkoutView from "../views/WorkoutView.vue"; 
import AthleteView from "../views/AthleteView.vue";
import { useUserStore } from "@/store/user";
import { ref } from "vue";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: { requiresAuth: true },
    },
    {
      path: "/all-programs",
      name: "programs",
      component: AllProgramsView,
    },
    {
      path: "/athletes",
      name: "athletes",
      component: AthletesView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
    },
    {
      path: "/profile", 
      name: "profile",
      component: ProfileView,
    },
    {
      path: "/settings",
      name: "settings",
      component: SettingsView,
    },
    {
      path: "/workout/:workoutId",
      name: "workout",
      component: WorkoutView,
      props: true,
    },
    {
      path: "/athlete/:athleteUsername",
      name: "athlete",
      component: AthleteView,
      props: true,
    }
  ],
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = false; // Replace with actual authentication check
  const userStore = useUserStore();
  const user = ref({
    isAuthenticated: false, 
    token: userStore.getToken || "", 
    info: userStore.getUser || {}
  })

  if (user.value.token) {
    user.value.isAuthenticated = true; 
  }

  if (to.matched.some(record => record.meta.requiresAuth) && !user.value.isAuthenticated) {
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router;