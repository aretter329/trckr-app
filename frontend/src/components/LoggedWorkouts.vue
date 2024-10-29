<script setup>
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { ref } from 'vue';
import WorkoutDisplay from './WorkoutDisplay.vue';

const props = defineProps({
  loggedWorkouts: {
    type: Array,
    required: true
  }
});
</script>

<template> 

<div v-for="logged_workout in loggedWorkouts" class="workout">
  {{ new Date(logged_workout.date).toLocaleDateString('en-US') }}
  {{ logged_workout.athlete.username }}
  {{ logged_workout.notes }}
  <WorkoutDisplay :id="logged_workout.id" :original_workout="logged_workout.workout"/>
</div>

</template>

<style scoped>
.workout{
  border: 1px solid black;
  margin: 10px;
  padding: 10px;
  width: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>