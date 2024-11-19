<script setup>
import { ref } from 'vue';
import { useQuery, useMutation } from "@vue/apollo-composable";
import { ADD_ATHLETE } from '@/mutations';
import { useUserStore } from "@/store/user";
import gql from 'graphql-tag';

const userStore = useUserStore();
const athleteUsername = ref('');

const addAthlete = async () => {
  try{
    await addAthleteMutation.mutate(
      {
        athleteUsername: athleteUsername.value,
        coachUsername: userStore.getUser.username
      }
    );
  }
  catch (error) {
    console.error(error);
  }
  athleteUsername.value = '';

};

const addAthleteMutation = useMutation(ADD_ATHLETE, {
  variables() {
    return {
      athleteUsername: athleteUsername.value,
      coachUsername: userStore.getUser.username
    };
  }
});

const { result, loading, error } = useQuery(gql` 
  query{
    allAthletesByCoach(coachUsername: "${userStore.getUser.username}") {
      id
      username
      coach {
        id
        username
      }
  }
  }`,
  {
    variables() {
      return {
        coachUsername: userStore.getUser.username
      };
    }
  }
);



</script>

<template>
  <div>
    <input type="text" v-model="athleteUsername" placeholder="Athlete username">
    <button @click="addAthlete">Add Athlete</button>
  </div>

  <h2> Your atheltes </h2>

  <div v-if="result && result.allAthletesByCoach">
    <div v-for="athlete in result.allAthletesByCoach" :key="athlete.id">
      {{ athlete.username }}
    </div>
  </div>

</template>