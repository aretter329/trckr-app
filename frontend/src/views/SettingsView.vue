<script setup>
import { useUserStore } from "@/store/user";
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { ref } from "vue";
import { useMutation } from "@vue/apollo-composable";
import { UPDATE_PASSWORD } from "@/mutations";

const userStore = useUserStore();
const name = userStore.getUser.firstName;
const router = useRouter();
const user = ref({
  isAuthenticated: false, 
  token: userStore.getToken || "", 
  info: userStore.getUser || {}
})
const resetPassword = ref(false);
const newPassword = ref("");
const confirmNewPassword = ref("");
const passwordAlert = ref("");
const passwordSuccess = ref(false);
const error = ref("");



onMounted(() => {
  if (!user.value.token) {
    router.push("/login");
  }
  else{
    user.value.isAuthenticated = true; 
  }
});

const { mutate: updatePasswordMutation } = useMutation(UPDATE_PASSWORD);

const resetPasswordMutation = async () => {
  error.value = "";
  passwordAlert.value = "";
  if (newPassword.value !== confirmNewPassword.value) {
    console.error("Passwords do not match");
    error.value = "Passwords do not match";
    return;
  }
  
  try {
    const response = await updatePasswordMutation({
      newPassword: newPassword.value,
      username: user.value.info.username
    });
    console.log(response);
    passwordAlert.value = "Password successfully updated";
    resetPassword.value = false;
    newPassword.value = "";
    confirmNewPassword.value = "";
  } catch (err) {
    error.value = err.message;
    console.error(err);
  }
  
};


</script> 

<template>
  <h1> Settings </h1>

  <div class="centered-content">
    <!--
    <div>
      <label for="firstName">First Name:</label>
      <input type="text" id="firstName" v-model="user.info.firstName" />
    </div>
    <div>
      <label for="lastName">Last Name:</label>
      <input type="text" id="lastName" v-model="user.info.lastName" />
    </div>
    -->
    <div>
      <label for="username">Username:</label>
      <input type="text" id="username" :value="user.info.username" disabled />
    </div>
    <div>
      <label for="email">Email:</label>
      <input type="email" id="email" :value="user.info.email" disabled />
    </div>
    <div>
      <button v-if="!resetPassword" @click="resetPassword = true">Reset Password</button>
      <div v-if="resetPassword" class="password"> 
        <label for="password">New Password:</label>
        <input type="password" id="password" v-model="newPassword" />
        <label for="confirmPassword">Confirm New Password:</label>
        <input type="password" id="confirmPassword" v-model="confirmNewPassword" />
        <button class='simple-button' @click="resetPasswordMutation">Submit</button>
      </div>
      
      <p v-if="passwordAlert" class="success"> {{ passwordAlert }} </p>
      <p v-if="error" class="error"> {{ error }} </p>
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

  .password{
    background-color: lightgray;
    display: flex;
    flex-direction: column;
    border: 1px solid black;
    padding: 10px;
    margin: 10px;
  }
</style>