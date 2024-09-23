<script setup>
import { useAuthStore } from "../store/auth";
import { onMounted } from "vue";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

const logout = () => {
  authStore.logout(router);
  router.push("/login");
};

onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
  }
});

</script> 

<template>
  <h1> welcome to home page </h1>
  <div v-if="authStore.isAuthenticated">
    <p v-if="authStore.user">{{ `hi, ${authStore.user.username}` }}</p>
    <p> youre logged in </p>
    <button @click="logout">Logout</button>
  </div>
  <p v-else> You are not logged in 
    <router-link to="/login">Login</router-link>
  </p>
</template>