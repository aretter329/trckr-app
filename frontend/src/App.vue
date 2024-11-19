<script setup>
import { RouterLink, RouterView } from "vue-router";
import { useUserStore } from "@/store/user";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { onMounted } from "vue";
import { provide } from 'vue'
import { ApolloClients } from '@vue/apollo-composable'

provide(ApolloClients)
//localStorage.clear()

const router = useRouter();
const userStore = useUserStore();
const user = ref({
  isAuthenticated: false, 
  token: userStore.getToken || "", 
  info: userStore.getUser || {}
})

const logout = () => {
  console.log('logout');
  userStore.removeToken();
  userStore.removeUser();
  router.push("/login");
};

/*onMounted(() => {
  if (!user.value.token) {
    router.push("/login");
  }
  else{
    user.value.isAuthenticated = true; 
  }
});
*/
import { watch } from "vue";

watch(() => user.value.token, (newToken, oldToken) => {
  console.log('token changed');
  if (!user.value.token) {
    user.value.isAuthenticated = false;
    router.push("/login");
  } else {
    user.value.isAuthenticated = true;
  }
});



const showMenu = ref(false);
</script>

<template>
  
  <header>
    <nav>
      <div v-if="user.isAuthenticated" @mouseover="showMenu = true" @mouseleave="showMenu = false">
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