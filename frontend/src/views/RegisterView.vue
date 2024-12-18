

<script setup>
import { ref } from 'vue';
import { USER_SIGNUP } from '@/mutations';
import { useMutation } from "@vue/apollo-composable";
import router from '@/router';

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
      isAthlete: role.value === 'athlete',
      firstName: firstName.value,
      lastName: lastName.value
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
      isAthlete: role.value === 'athlete',
      firstName: firstName.value.charAt(0).toUpperCase() + firstName.value.slice(1),
      lastName: lastName.value.charAt(0).toUpperCase() + lastName.value.slice(1)
    });
    firstName.value = '';
    lastName.value = '';
    username.value = '';
    email.value = '';
    password.value = '';
    confirmPassword.value = '';
    console.log(response);
    router.push('/login');
  }
  catch (error) {
    console.error(error);
  }
  
};



</script>

<template>
  <div class="centered-content">
    <h2>Register</h2>
    <form @submit.prevent="register" style="display: flex; flex-direction: column;" >
      <div> 
        <label for="firstName">First Name:</label>
        <input v-model="firstName" id="firstName" type="text" required>
      </div>

      <div>
        <label for="lastName">Last Name:</label>
        <input v-model="lastName" id="lastName" type="text">
      </div>

      <div>
        <label for="email">Email:</label>
        <input v-model="email" id="email" type="email" required>
      </div>

      <div>
        <label for="username">Username:</label>
        <input v-model="username" id="username" type="text" required>
      </div>

      <div>
        <label for="password">Password:</label>
        <input v-model="password" id="password" type="password" required>
      </div>
      <div>
        <label for="confirmPassword">Confirm Password:</label>
        <input v-model="confirmPassword" id="confirmPassword" type="password" required>
      </div>

      <div>
        <input type="radio" id="athlete" value="athlete" name="role" v-model="role" checked="checked">
        <label for="athlete">Athlete</label>
        <br/>
        <input type="radio" id="coach" value="coach" name="role" v-model="role">
        <label for="coach">Coach</label>
        
      </div>
        <button class="simple-button" type="submit">Register</button>
    </form>
    <p v-if="error">{{ error }}</p>
    <p v-if="success">{{ success }}</p>
  </div>
</template>

<style scoped>

form div {
  margin-bottom: 15px;
}

input[type="text"],
input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 5px;
}

input[type="radio"] {
  margin: 5px;
}

p {
  margin-top: 10px;
  color: red;
}

p.success {
  color: green;
}
</style>