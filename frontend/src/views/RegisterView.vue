<template>
  <div>
    <h2>Register</h2>
    <form @submit.prevent="register" >
      <div>
        <label for="email">Email:</label>
        <input v-model="email" id="email" type="email" required>
      </div>
      <div>
        <label for="username">Username:</label>
        <input v-model="username" id="username" type="text" required>
      </div>
      <div>
        <input type="radio" id="athlete" value="athlete" name="role" v-model="role" checked="checked">
        <label for="athlete">Athlete</label>
        <input type="radio" id="coach" value="coach" name="role" v-model="role">
        <label for="coach">Coach</label>
        
      </div>
      <div>
        <label for="password">Password:</label>
        <input v-model="password" id="password" type="password" required>
      </div>
      <div>
        <label for="confirmPassword">Confirm Password:</label>
        <input v-model="confirmPassword" id="confirmPassword" type="password" required>
      </div>
        <button type="submit">Register</button>
    </form>
    {{role}}
    <p v-if="error">{{ error }}</p>
    <p v-if="success">{{ success }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { USER_SIGNUP } from '@/mutations';
import { useMutation } from "@vue/apollo-composable";

const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const error = ref('');
const success = ref('');
const role = ref('athlete');


const createUser = useMutation(USER_SIGNUP, {
  variables() {
    return {
      username: username.value,
      email: email.value,
      password: password.value,
      isCoach: role.value === 'coach',
      isAthlete: role.value === 'athlete'
    };
  }
});


const checkPassword = () => {
    if (password.value !== confirmPassword.value || password.value === '') {
        alert('Passwords do not match');
        return false;
    }
    return true;
};

const register = async () => {
  if (!checkPassword()) {
    return;
  }
  try {
    const response = await createUser.mutate({
      username: username.value,
      email: email.value,
      password: password.value,
      isCoach: role.value === 'coach',
      isAthlete: role.value === 'athlete'
    });
    username.value = '';
    email.value = '';
    password.value = '';
    console.log(response);
  }
  catch (error) {
    console.error(error);
  }
  
};



</script>

<style scoped>
</style>