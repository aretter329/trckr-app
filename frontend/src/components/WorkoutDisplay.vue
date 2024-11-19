<script setup> 
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { defineProps, ref, watch } from 'vue';


const props = defineProps({
  id: {
    type: String,
    required: true
  },
  original_workout: {
    type: Object,
    required: false
  },
  original_workout_id: {
    type: String,
    required: false
  }
});

const { result: loggedSets, loading, error1} = useQuery(gql` 
  query{
    loggedSetsByWorkout(workoutId: "${props.id}") {
      repsCompleted
      weightCompleted
      id
      set{
      id
      }

    }
  }`,
  {
    variables() {
      return {
        workoutId: props.id
      };
    }
  }
);

const { result: originalWorkout } = useQuery(gql` 
  query{
    workoutById(workoutId: "${props.original_workout_id}") {
      id
      blocks{
        id
        exercises{
          id
          name
          description
          sets{
            id
            reps
            weight
            number
          }
        }
      }

    }
  }`,
  {
    variables() {
      return {
        workoutId: props.original_workout_id
      };
    }
  }
);

watch(() => props.id, () => {
  console.log('refetch')
});

watch(() => props.original_workout_id, () => {

});

</script> 

<template> 


<div v-if="originalWorkout && loggedSets" >
  <div v-for="block in originalWorkout.workoutById.blocks" :key="block.id" class="p-block-div">
    <div v-for="exercise in block.exercises" :key="exercise.id" class="exercise-box">
      {{ exercise.name }} <br/>
      <div class="set-list">
        <table>
          <tr>
            <td> Weight </td>
            <td v-for="set, index in exercise.sets" :key="index">
              
               {{ loggedSets.loggedSetsByWorkout.find(loggedSet => loggedSet.set.id === set.id).weightCompleted }}
            </td>
          </tr>
          <tr>
            <td> Reps </td>
            <td v-for="set, index in exercise.sets" :key="index">
              {{ loggedSets.loggedSetsByWorkout.find(loggedSet => loggedSet.set.id === set.id).repsCompleted }}
            </td>
          </tr>
        </table>
        
      </div>
    </div>
  </div> 

</div>

</template> 

<style scoped>
td{ 
  border: 1px solid black;
  padding: 5px;
}

</style>