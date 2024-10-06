import { createRouter, createWebHistory } from "vue-router";
import AuthorView from "../views/AuthorView.vue";
import AllProgramsView from "../views/AllProgramsView.vue";
import ProgramView from "../views/ProgramView.vue";
import ProgramsByTagView from "../views/ProgramsByTagView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import HomeView from "../views/HomeView.vue";
import AthletesView from "../views/AthletesView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
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
      path: "/author/:username",
      name: "author",
      component: AuthorView,
    },
    {
      path: "/program/:slug",
      name: "program",
      component: ProgramView,
    },
    {
      path: "/tag/:tag",
      name: "tag",
      component: ProgramsByTagView,
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
  ],
});

export default router;