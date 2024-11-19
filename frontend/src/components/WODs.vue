<script setup> 
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { ref } from 'vue';
import WorkoutDisplay from './WorkoutDisplay.vue';
import { useUserStore } from "@/store/user";
import { watch } from 'vue';

const userStore = useUserStore();
const username = userStore.getUser.username;
const user = userStore.getUser;

const { result: workouts, loading, error } = useQuery(gql` 
  query{
    getLoggedWorkoutsByAthlete(athleteUsername: "${username}") {
      assignedDate
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


const calendar = ref(null);

/*content: change font color 
  highlight: change background color
  fillMode: light, dark, none
  color: green, red, blue, yellow, orange, purple, pink, teal, cyan, lime, amber, brown, grey, white, black
  dot: puts dot below date
  POPOVER  can have a brief description of the workout (this is only helpful on desktop)
  */
  
const date= ref();
const attrs = ref([]);


watch(workouts, (newWorkouts) => {
  console.log('here')
  if (newWorkouts) {
    const workoutDates = newWorkouts.getLoggedWorkoutsByAthlete.map(workout => {
      const date = new Date(workout.assignedDate);
      date.setHours(date.getHours() + 5);
      return date;
    });
    console.log(workoutDates);
    attrs.value = [
      {
        key: 'today',
        highlight: {
          color: 'green',
          fillMode: 'light',
        },
        dates: new Date()
      },
      ...workoutDates.map(date => ({
        key: date.toISOString(),
        dot: {
          color: 'green',
        },
        dates: date,
        popover: {
          label: 'Workout assigned',
        }
      }))
    ];
  }
});

  

</script> 

<template>

  <div v-if="workouts" class="calendar-container"> 
        <VDatePicker 
      ref="calendar" 
      transparent 
      borderless 
      :color="'green'" 
      v-model="date"
      :attributes="attrs">
      
    </VDatePicker>
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
</style>

