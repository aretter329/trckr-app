<script setup> 
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { computed, ref } from 'vue';
import WorkoutDisplay from './WorkoutDisplay.vue';
import { useUserStore } from "@/store/user";
import { watch } from 'vue';
import { defineEmits } from 'vue';
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
  
const date= ref(new Date());
const attrs = ref([]);
const selectedWorkouts = computed(() => {
  if (date.value === null || attrs.value == []) {
    return [];
  }
  const dateInfo = attrs.value.filter(attr => attr.dates.toDateString() === date.value.toDateString());
  if (!dateInfo.some(attr => attr.popover)) {
    return [];
  }
  return [dateInfo[0].popover.content];
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


watch(workouts, (newWorkouts) => {
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
};  

</script> 

<template>
  <div v-if="workouts" class="calendar-container"> 
      <VDatePicker 
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
        {{ selectedWorkouts[0].workout.id }}
        <WorkoutDisplay 
          :original_workout_id="selectedWorkouts[0].workout.id" 
          :id="selectedWorkouts[0].id" 
          :key="selectedWorkouts[0].id"
        />

        <RouterLink :to="{ name: 'workout', params: { workoutId: selectedWorkouts[0].id } }">
          View workout
        </RouterLink>
      </div>
      <div v-else>
        No workout assigned 
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

