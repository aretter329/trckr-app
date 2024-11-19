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
function resetPassword() {
    // Implement reset password logic here
    alert("Reset password functionality to be implemented");
  }

</script> 

<template>
  <h1> Settings </h1>

  <div class="centered-content">
    <div>
      <label for="firstName">First Name:</label>
      <input type="text" id="firstName" v-model="user.info.firstName" />
    </div>
    <div>
      <label for="lastName">Last Name:</label>
      <input type="text" id="lastName" v-model="user.info.lastName" />
    </div>
    <div>
      <label for="username">Username:</label>
      <input type="text" id="username" :value="user.info.username" disabled />
    </div>
    <div>
      <label for="email">Email:</label>
      <input type="email" id="email" :value="user.info.email" disabled />
    </div>
    <div>
      <button @click="resetPassword">Reset Password</button> (this doesn't work yet)
    </div>
    
  </div>
 
</template>

<style scoped>
  * {
    text-align: center;
  }
  
  input{ 
    margin: 5px;
  }
</style>