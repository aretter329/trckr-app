<script setup>
import { useUserStore } from "@/store/user";
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { ref } from "vue";
import WODs from '../components/WODs.vue';

const userStore = useUserStore();
const name = userStore.getUser.firstName;
const username = userStore.getUser.username;
const router = useRouter();
const user = ref({
  isAuthenticated: false, 
  token: userStore.getToken || "", 
  info: userStore.getUser || {}
})
const selectedDate = ref(new Date());

const handleDate = (newDate) => {
  selectedDate.value = newDate;
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
  <h1> Welcome, {{ name || username }}! </h1>
   <div class='row'>
    <div class="wod-container"> 
      <WODs @update-date="handleDate"/>
    </div>
</div>
 
</template>

<style scoped>
  * {
    text-align: center;
  }
  
  .wod-container {
    margin: auto;
    padding: 10px;
    width: 50%;
  }

  .row{
    display: flex;

  }

</style>