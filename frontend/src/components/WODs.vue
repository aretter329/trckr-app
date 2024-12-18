<script setup> 
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { computed, ref } from 'vue';
import { useUserStore } from "@/store/user";
import { watch, watchEffect } from 'vue';
import { defineEmits } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const userStore = useUserStore();
const username = userStore.getUser.username;
const user = userStore.getUser;
const calendar = ref(null);

/*content: change font color 
  highlight: change background color
  fillMode: light, dark, none
  color: green, red, blue, yellow, orange, purple, pink, teal, cyan, lime, amber, brown, grey, white, black
  dot: puts dot below date
  POPOVER  can have a brief description of the workout (this is only helpful on desktop)
  */
  
const date = ref(new Date()); //default to current date
const attrs = ref([]);  //array of objects with date and workout info
const selectedWorkouts = computed(() => { //array of workouts for the selected date
  if (date.value === null || attrs.value == []) {
    return [];
  }
  const dateInfo = attrs.value.filter(attr => attr.dates.toDateString() === date.value.toDateString());
  console.log('date info', dateInfo);
  if (!dateInfo.some(attr => attr.popover)) {
    return [];
  }
  console.log(dateInfo);
  //return [dateInfo[1].popover.content];
  if (dateInfo[1] && dateInfo[1].popover) {
    return [dateInfo[1].popover.content];
  } else {
    return [dateInfo[0].popover.content];
  }
});
const emit = defineEmits(['updateDate']);

watch(date, (newDate) => {
  emit('updateDate', newDate);
});

const { result: workouts, loading, error } = useQuery(gql` 
  query{
    getLoggedWorkoutsByAthlete(athleteUsername: "${username}") {
      assignedDate
      id
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

watchEffect(() => {
  const newWorkouts = workouts.value;
  if (newWorkouts) {
    const workoutDates = newWorkouts.getLoggedWorkoutsByAthlete.map(workout => {
      const date = new Date(workout.assignedDate);
      date.setHours(date.getHours() + 5);
      return {
        date,
        workout
      };
    });
    attrs.value = [
      {
        key: 'today',
        highlight: {
          color: 'green',
          fillMode: 'light',
        },
        dates: new Date()
      },
      ...workoutDates.map(({ date, workout }) => ({
        key: date.toISOString(),
        dot: {
          color: 'green',
        },
        dates: date,
        popover: {
          label: 'Workout assigned',
          content: workout || 'No notes available'
        },
        workout
      }))
    ];
  }
});

const handleDate = (date) => {
  if (attrs.value.length > 0) {
    console.log('date', date);
    const selectedDate = attrs.value.find(attr => attr.dates.toDateString() === date.toDateString());
    console.log(selectedDate);
    if (selectedDate && selectedDate.workout) {
      router.push({ name: 'workout', params: { workoutId: selectedDate.workout.id } });
    }
  }
};  

</script> 

<template>
  
  <div v-if="workouts" class="calendar-container"> 
      <VDatePicker 
        style="width: 300px;"
        ref="calendar" 
        transparent 
        borderless 
        :color="'green'" 
        @update:model-value="handleDate"
        v-model="date"
        :attributes="attrs"
      >
      </VDatePicker>
      
      <div v-if="selectedWorkouts && selectedWorkouts.length > 0">
        <RouterLink :to="{ name: 'workout', params: { workoutId: selectedWorkouts[0].id } }">
          View today's workout
        </RouterLink>
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
</style>

