<template>
  <div>
    <label for="username">Username:</label>
    <input type="text" id="username" v-model="username" required>
    <label for="password">Password:</label>
    <input type="password" id="password" v-model="password" required>
    <button @click="login">Login</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const username = ref('');
const password = ref('');


</script>

<style scoped>
</style>
