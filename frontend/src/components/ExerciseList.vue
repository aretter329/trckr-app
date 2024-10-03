<script setup> 
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { ref } from 'vue';
import SetsAndReps from './SetsAndReps.vue';

const props = defineProps({
  workout_id: {
    type: String,
    required: true,
  }
});

const exercises = ref([]);


const { result, loading, error } = useQuery(gql`
  query{
    exercisesByWorkout(workoutId: "${props.workout_id}") {
      id
      name
      block
      orderInBlock
    }
  }
`);

exercises.value = result.value?.exercisesByWorkout;
</script>

<template>
  <div class="exercise-list">
    <div v-for="exercise in exercises" :key="exercise.id" class="exercise-box">
      {{ exercise.name }} <br/>
      block: {{ exercise.block }}  <br/>
      order in block: {{ exercise.orderInBlock }} </br>
      <SetsAndReps :exercise_id="exercise.id" />
        
    </div>
  </div>
</template>