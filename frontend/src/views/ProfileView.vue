<script setup>
import { useUserStore } from "@/store/user";
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { ref } from "vue";

const userStore = useUserStore();
const name = userStore.getUser.firstName;
const router = useRouter();
const user = ref({
  isAuthenticated: false, 
  token: userStore.getToken || "", 
  info: userStore.getUser || {}
})


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
  <div class="centered-content">
    <h1> {{ user.info.username }} </h1>


  <h2> Workouts Completed: </h2>
  actual number of workouts completed

  <h2> Strength Maxes: </h2>
  list of the exercises and their maxes for the individual 
  </div>
  


  
 
</template>

<style scoped>
  * {
    text-align: center;
  }
  
  .wod-container {
    border: 3px solid green;
    margin: auto;
    padding: 10px;
    width: 50%;
  }
</style>