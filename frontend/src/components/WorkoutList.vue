<script setup> 
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { ref } from 'vue';
import ExerciseList from './ExerciseList.vue';
const props = defineProps({
  day_id: {
    type: String,
    required: true,
  }
});


const { result, loading, error } = useQuery(gql`
  query{
    workoutsByDay(dayId: "${props.day_id}") {
      id
      type
      orderInDay
    }
  }
`);

const workouts = result.value?.workoutsByDay;

</script>

<template>
  <div class="workout-list">
    <div v-for="workout in workouts" :key="workout.id" class="workout-box">
      <div class="workout-type">
        {{ workout.type }}
        <ExerciseList :workout_id="workout.id" />
      </div>
    </div>
  </div>
</template>