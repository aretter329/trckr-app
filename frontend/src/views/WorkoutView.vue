<script setup>
import { ref, watchEffect } from 'vue';
import { useMutation, useQuery } from "@vue/apollo-composable";
import gql from 'graphql-tag';
import { UPDATE_LOGGED_SETS } from '@/mutations';


const currentSets = ref([]);
const message = ref('');
const props = defineProps({
  workoutId: String
})

const { result: workout, } = useQuery(gql`
  query {
    loggedWorkoutById(loggedWorkoutId: "${props.workoutId}") {
      athlete{
        id
        username
      }
      assignedDate
      date
      workout{
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
      notes
    }
  }
`, {
    variables() {
      return {
        loggedWorkoutId: props.workoutId,
      };
    }
  });

const { result: loggedSets, refetch:refetchSets } = useQuery(gql` 
  query{
    loggedSetsByWorkout(workoutId: "${props.workoutId}") {
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
  },
);

watchEffect(() => {
  if (loggedSets.value) {
    currentSets.value = loggedSets.value.loggedSetsByWorkout.map(set => ({
      setId: set.id,
      repsCompleted: set.repsCompleted,
      weightCompleted: set.weightCompleted,
      original_set_id: set.set.id
    }));
  }
});

const { mutate: updateLoggedSetsMutation } = useMutation(UPDATE_LOGGED_SETS);

const updateLoggedSets = async () => {
  try {
    const response = await updateLoggedSetsMutation({
      loggedSets: currentSets.value.map(set => ({
        setId: set.setId,
        repsCompleted: set.repsCompleted,
        weightCompleted: set.weightCompleted
      })),
      loggedWorkoutId: props.workoutId,
    });
    console.log(response);
    refetchSets();
    message.value = 'Workout saved!';
  } catch (error) {
    console.error(error);
  }
};

</script>

<template>
  
  <div v-if="workout && loggedSets" class="wrapper centered-content">
    <div v-for="block in workout.loggedWorkoutById.workout.blocks" :key="block.id" class="p-block-div" style="width: auto;">
      <div v-for="exercise in block.exercises" :key="exercise.id" class="exercise-box">
        <span class="exercise-header"> {{ exercise.name }} </span>
          <table>
            <tr>
              <td>Weight</td>
              <td v-for="(set, index) in exercise.sets" :key="index">
                <input type='number' 
                     v-model="(currentSets.find(loggedSet => loggedSet.original_set_id === set.id)).weightCompleted" 
                     :placeholder="set.weight"  
                     @input="message=''">
              </td>
            </tr>
            <tr>
              <td>Reps</td>
              <td v-for="(set, index) in exercise.sets" :key="index">
                <input type='number' 
                   v-model="(currentSets.find(loggedSet => loggedSet.original_set_id === set.id)).repsCompleted" 
                   :placeholder="set.reps" 
                   @input="message=''" >
              </td>
            </tr>
          </table>
      </div>
    </div>
    <button v-if="message==''" class="simple-button" @click="updateLoggedSets"> save workout </button>
    <p v-if="message"> {{ message }}</p>
  </div>


  
</template>


<style scoped>

td{ 
  padding: 5px;
}

input{
  width: 50px;
}

.exercise-header{
  font-size: 16px;
  font-weight: bold;
}

.wrapper{
  padding: 20px;
}





</style>
