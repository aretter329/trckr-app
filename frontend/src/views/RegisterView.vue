<template>
  <div>
    <h1>Register</h1>
    <form @submit.prevent="register">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required>
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <div>
        <label for="confirmPassword">Confirm Password:</label>
        <input type="password" id="confirmPassword" v-model="confirmPassword" required>
      </div>
      <button type="submit">Register</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
//import { useMutation, gql } from '@vue/apollo-composable';

const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');

const checkPassword = () => {
    if (password.value !== confirmPassword || password.value === '') {
        alert('Passwords do not match');
        return false;
    }
    return true;
};


const register = async () => {
  try {
    const isValidPassword = checkPassword();
    if (!isValidPassword) {
      return;
    }
  }
  catch (error) {
    console.error(error);
  }
};



</script>

<style scoped>
</style>