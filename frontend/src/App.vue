<script setup>
import { RouterLink, RouterView, useRouter } from "vue-router";
import { useUserStore } from "@/store/user";
import { ref, watch, computed, provide } from "vue";
import { ApolloClients } from '@vue/apollo-composable'

provide(ApolloClients)
//localStorage.clear()

const router = useRouter();
const userStore = useUserStore();
const showMenu = ref(false);

const user = computed(() => ({
  isAuthenticated: !!userStore.getToken,
  token: userStore.getToken,
  info: userStore.getUser
}));

const logout = () => {
  console.log('logout');
  userStore.removeToken();
  userStore.removeUser();
  router.push("/login");
};



watch(() => user.value.token, (newToken, oldToken) => {
  console.log('token changed');
  if (!user.value.token) {
    user.value.isAuthenticated = false;
    router.push("/login");
  } else {
    user.value.isAuthenticated = true;
  }
});


</script>

<template>
  
  <header>
    <nav>
      <div v-if="user.isAuthenticated" style="display: flex">
        <div @mouseover="showMenu = true" @mouseleave="showMenu = false">
          {{ userStore.getUser.username }}
          <div v-if="showMenu" class="dropdown-menu">
            <RouterLink to="/profile">Profile</RouterLink>
            <RouterLink to="/settings">Settings</RouterLink>
            <RouterLink to="/login" @click="logout">Logout</RouterLink>
          </div>
        </div>
        <RouterLink to="/" :class="{ active: $route.path === '/'}">
          <div class="nav-link">
            Home
          </div>
        </RouterLink>
        <RouterLink v-if="user.info.isCoach" to="/all-programs" :class="{ active: $route.path === '/all-programs'}">
          <div class="nav-link">
            Programs
          </div>
        </RouterLink>
        <RouterLink v-if="user.info.isCoach" to="/athletes" :class="{ active: $route.path === '/athletes'}">
          <div class="nav-link">
            Athletes
          </div>
        </RouterLink>
      </div>
      <div v-else style="display:flex">
        <RouterLink to="/login" :class="{ active: $route.path === '/login'}">
          <div class="nav-link">
            Login
          </div>
        </RouterLink>
        <RouterLink to="/register" :class="{ active: $route.path === '/register'}">
          <div class="nav-link">
            Register
          </div>
        </RouterLink>
      </div>

    </nav>
  </header>

  <body>
    <RouterView />
      
  </body>
 
</template>

<style scoped>

  header {
    position: fixed; 
    top: 0; 
    left: 0; 
    right: 0;
    background-color: var(--dodger-blue);
  }

  nav {
    text-align: center;
    display: flex;
    justify-content: center;
  }
  
  nav a {
    padding: 0.5rem;
  }

  body{
    padding-top: 2rem;
    background-color: rgb(248, 247, 255);
    
  }

  .active {
    font-weight: bold;
    background-color: var(--uranian-blue);
  }

  .dropdown-menu {
    display: flex;
    flex-direction: column;
    position: absolute;
    background-color: var(--dodger-blue);
    color: white;
    border-radius: 5px;
    padding: 5px;
    margin-top: 5px;
  }
 
</style>