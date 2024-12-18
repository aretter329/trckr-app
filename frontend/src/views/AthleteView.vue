<script setup>
import { ref, watchEffect, computed } from 'vue';
import { useMutation, useQuery } from "@vue/apollo-composable";
import gql from 'graphql-tag';
import WorkoutProgress from '@/components/WorkoutProgress.vue';

const props = defineProps({
  athleteUsername: String
})

const { result: workouts, loading, error } = useQuery(gql` 
  query{
    getLoggedWorkoutsByAthlete(athleteUsername: "${props.athleteUsername}") {
      assignedDate
      id
      loggedSets{
        id
        repsCompleted
        weightCompleted
        }
      workout{
        id
      }
      notes
    }
  }`,
  {
    variables() {
      return {
        athleteUsername: username
      };
    }
  }
);

const { result: athlete } = useQuery(gql` 
  query{
    userInfo(username: "${props.athleteUsername}") {
      id
      username
      firstName
      lastName
    }
  }`,
  {
    variables() {
      return {
        username: props.athleteUsername
      };
    }
  }
);

const collapsedWorkouts = ref([]);

const toggleCollapse = (workoutId) => {
    if (isCollapsed(workoutId)) {
        collapsedWorkouts.value = collapsedWorkouts.value.filter(w => w !== workoutId);
    } else {
        collapsedWorkouts.value.push(workoutId);
    }
};

const isCollapsed = (workoutId) => {
    return collapsedWorkouts.value.includes(workoutId);
};

const formatDate = (date) => {
    return new Date(date).toLocaleDateString();
};

const sortedWorkouts = computed(() => {
    return [...workouts.value.getLoggedWorkoutsByAthlete].sort((a, b) => {
        return new Date(b.assignedDate) - new Date(a.assignedDate);
    });
});
</script>

<template>
  <div v-if="athlete" class="centered-content">
    <h1>{{ athlete.userInfo.firstName && athlete.userInfo.lastName ? athlete.userInfo.firstName + ' ' + athlete.userInfo.lastName : athlete.userInfo.username }}'s workouts</h1>
  </div>

  <div class='content' v-if="workouts">
    <div v-for="workout in sortedWorkouts" :key="workout.id">
      <div class="workout-row" @click="toggleCollapse(workout.id)">
            {{ formatDate(new Date(new Date(workout.assignedDate).setDate(new Date(workout.assignedDate).getDate() + 1)).toLocaleString('en-US', { timeZone: 'America/New_York' })) }}
        </div>
        <div v-if="isCollapsed(workout.id)" class="workout-details">
          <WorkoutProgress :workoutId="workout.id" />
          Notes: <!-- ADD NOTES FROM ATHELTE HERE -->
        </div>
      </div>
  </div>
</template>


<style scoped>

.workout-row {
  cursor: pointer;
  width: 80vw;
  border: 1px solid #ccc;
  padding: 10px;
  margin: 10px;
  border-radius: 5px;
  background-color: rgb(238, 236, 236);
}

.content{ 
  display: flex;
  flex-direction: column;
  align-items: center;
}


</style>
