<script setup>
import { useUserStore } from "@/store/user";
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { ref, computed, watch } from "vue";
import WODs from '../components/WODs.vue';
import { useQuery } from "@vue/apollo-composable";
import gql from 'graphql-tag';

const userStore = useUserStore();
const name = userStore.getUser.firstName;
const username = userStore.getUser.username;
const router = useRouter();
const user = ref({
  isAuthenticated: false, 
  token: userStore.getToken || "", 
  info: userStore.getUser || {}
})
const selectedDate = ref(new Date());
const isCoach = userStore.getUser.isCoach;

const handleDate = (newDate) => {
  selectedDate.value = newDate;
};

const formattedDate = computed(() => {
  const date = selectedDate.value;
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
});


onMounted(() => {
  if (!user.value.token) {
    router.push("/login");
  }
  else{
    user.value.isAuthenticated = true; 
  }
});


const { result: athletes, refetch: refetchAthletes } = useQuery(gql` 
  query athletesWithWorkoutOnDate($coachUsername: String!, $date: Date!) {
    athletesWithWorkoutOnDate(coachUsername: $coachUsername, date: $date) {
        id
        username
        firstName
        lastName
    }
  }`, 
  {
    coachUsername: username,
    date: formattedDate
  }
);



</script> 

<template>
  <h1> Welcome, {{ name || username }}! </h1>
   <div class='row'>
    <div class="wod-container"> 

      <WODs @update-date="handleDate"/>
      <div v-if="isCoach">

        Workouts {{ formattedDate === new Date().toISOString().split('T')[0] ? 'today' : formattedDate }}:
        <div v-if="athletes && athletes.athletesWithWorkoutOnDate.length > 0">
          <div v-for="athlete in athletes.athletesWithWorkoutOnDate" :key="athlete.id">
            <RouterLink :to="'/athlete/' + athlete.username">
              {{ athlete.firstName }} {{ athlete.lastName }} {{ athlete.username }}
            </RouterLink>
          </div>
        </div>
        <div v-else>
          No athletes with workouts on this date
        </div>
      </div>
      
      <div v-else>
        
      </div>

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