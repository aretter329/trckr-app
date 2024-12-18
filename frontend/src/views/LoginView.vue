<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { USER_SIGNIN } from '@/mutations';
import { useUserStore } from '@/store/user';
import { useMutation } from "@vue/apollo-composable";

const userStore = useUserStore();
const username = ref('');
const password = ref('');
const error = ref('');
const router = useRouter();

const loginUser = useMutation(USER_SIGNIN, {
  variables() {
    return {
      username: username.value,
      password: password.value
    };
  },
});

const login = async () => {
  console.log('login');
  try {
    const user = await loginUser.mutate({
      username: username.value,
      password: password.value
    });
    username.value = '';
    password.value = '';
    userStore.setToken(user.data.tokenAuth.token);
    userStore.setUser(user.data.tokenAuth.user);
    router.push('/');
  }
  catch (err) {
    error.value = err.message;
    console.error(err);
  }
};

const resetError = () => {
  error.value = '';
};

</script>

<template>
  
  <div class="login centered-content"> 
    <h1 style="font-size: 50px; margin-bottom: 20px;"> Trckr </h1>
    
    <form style="display: flex; flex-direction: column; align-items: center;" @submit.prevent="login">
      <div> 
        <label for="username"> Username </label>
        <input v-model="username" type="text" id="username" name="username" required @input="resetError">
      </div>
      <div> 
        <label for="password"> Password </label>
        <input v-model="password" type="password" id="password" name="password" required @input="resetError">
      </div>
      <button class='simple-button' style="width: 75px" type="submit"> Login </button>
  </form>

  <p v-if="error" class="error"> {{ error }} </p>

  <div style="margin: 10px; display: flex; flex-direction: column; align-items: center;">
     <div> Need an account? </div>
     <div> <button class='simple-button'  @click="router.push('/register')">Register</button> </div>
    </div>
  </div>

  

  
</template>


<style scoped>
.login {
  display: flex; 
  margin-top: 100px;
  align-items: center;
}


</style>
