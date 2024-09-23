<template>
  <div class="login"> 
    <h2> Login </h2>
    <form @submit.prevent="login">
      <div> 
        <label for="username"> Username </label>
        <input v-model="username" type="text" id="username" name="username" required @input="resetError">
      </div>
      <div> 
        <label for="password"> Password </label>
        <input v-model="password" type="password" id="password" name="password" required @input="resetError">
      </div>
    <button type="submit"> Login </button>
  </form>
  <p v-if="error" class="error"> {{ error }} </p>
  </div>
</template>

<script setup>
//import { useAuthStore } from "../store/auth";
import { ref } from 'vue';
//import { useRouter } from 'vue-router';
import { USER_SIGNIN } from '@/mutations';
import { useUserStore } from '@/store/user';
import { useMutation } from "@vue/apollo-composable";

const userStore = useUserStore();

//const authStore = useAuthStore();
const username = ref('');
const password = ref('');
const error = ref('');
//const router = useRouter();

const loginUser = useMutation(USER_SIGNIN, {
  variables() {
    return {
      username: username.value,
      password: password.value
    };
  }
});

const login = async () => {
  try {
    const user = await loginUser.mutate({
      username: username.value,
      password: password.value
    });
    username.value = '';
    password.value = '';
    userStore.setToken(user.data.tokenAuth.token);
    userStore.setUser(user.data.tokenAuth.user);
    console.log(user);
  }
  catch (error) {
    console.error(error);
  }
  

};

/*
const resetError = () => {
  error.value = '';
};
*/
</script>

<style scoped>
</style>
