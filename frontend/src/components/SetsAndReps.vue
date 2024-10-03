<script setup> 
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { ref } from 'vue';
const props = defineProps({
  exercise_id: {
    type: String,
    required: true,
  }
});

const sets = ref([]);


const { result, loading, error } = useQuery(gql`
  query{
    setsByExercise(exerciseId: "${props.exercise_id}") {
      reps 
      weight
      number
    }
  }
`);

sets.value = result.value?.setsByExercise;
</script>

<template>
  <div class="set-list">
    <div v-for="set in sets" :key="set.id" class="set-box">
      {{ set.reps }} reps <br/>
      {{ set.weight }} lbs <br/>
      number {{ set.number }} <br/>
    </div>
  </div>
</template>