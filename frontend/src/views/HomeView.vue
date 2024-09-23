<script setup>
import { useUserStore } from "@/store/user";
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { ref } from "vue";

const userStore = useUserStore();
const router = useRouter();
const user = ref({
  isAuthenticated: false, 
  token: userStore.getToken || "", 
  info: userStore.getUser || {}
})

const logout = () => {
  userStore.removeToken();
  userStore.removeUser();
  router.push("/login");
};

onMounted(() => {
  if (!user.value.token) {
    router.push("/login");
  }
  else{
    user.value.isAuthenticated = true; 
  }
});

</script> 

<template>
  <h1> welcome to home page </h1>
  <div v-if="user.isAuthenticated">
    <p v-if="userStore.user">{{ `hi, ${userStore.getUser.username}` }}</p>
    <p> youre logged in </p>
    <button @click="logout">Logout</button>
  </div>
  <p v-else> You are not logged in 
    <router-link to="/login">Login</router-link>
  </p>
</template>