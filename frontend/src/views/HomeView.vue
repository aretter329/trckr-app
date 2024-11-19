<script setup>
import { useUserStore } from "@/store/user";
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { ref } from "vue";
import WODs from '../components/WODs.vue';
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import WorkoutDisplay from '../components/WorkoutDisplay.vue';

const userStore = useUserStore();
const name = userStore.getUser.firstName;
const username = userStore.getUser.username;
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


const formatDate = (date) => {
  const d = new Date(date);
  let month = '' + (d.getMonth() + 1);
  let day = '' + d.getDate();
  const year = d.getFullYear();

  if (month.length < 2) 
    month = '0' + month;
  if (day.length < 2) 
    day = '0' + day;

  return [year, month, day].join('-');
};

const { result: workouts, loading, error } = useQuery(gql` 
  query{
    assignedWorkoutsByAthleteAndDate(athleteUsername: "${username}", assignedDate: "${formatDate(new Date())}") {
      assignedDate
      workout{
        id
        
      }
      notes
      id
    }
  }`,
  {
    variables() {
      return {
        athleteUsername: username,
        assignedDate: formatDate(new Date())
      };
    }
  }
);

</script> 

<template>
  <h1> Welcome, {{ name || username }}! </h1>
   <div class='row'>

    <div class="centered-content"> 
      <h2> Today's Workout </h2>
      <div v-if="workouts && workouts.assignedWorkoutsByAthleteAndDate.length > 0">
        <WorkoutDisplay :original_workout_id="workouts.assignedWorkoutsByAthleteAndDate[0].workout.id" :id="workouts.assignedWorkoutsByAthleteAndDate[0].id" />
      </div>
    </div>

    <div class="wod-container"> 
      <WODs />
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