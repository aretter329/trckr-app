<script setup> 
import { useQuery, useMutation } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { ref } from 'vue';
import { LOG_WORKOUT } from '@/mutations';
import { defineEmits } from 'vue';

const emit = defineEmits(['showAssignment']);
const start_date = ref('');
const selectedAthletes = ref([]); 

const props = defineProps({
  program: {
    type: Array,
    required: true,
  },
  coach: {
    type: String,
    required: false,
    default: true,
  }
});

const attrs = {
  key: 'today',
  highlight: {
    color: 'green',
    fillMode: 'light',
  },
  dates: new Date()
}

const { mutate: logWorkoutMutation } = useMutation(LOG_WORKOUT);

const logWorkout = async (username, assigned_date, workout_id, sets) => {
  try {
    const response = await logWorkoutMutation({
      athleteUsername: username,
      workoutId: workout_id,
      sets: sets,
      notes: '',
      assignedDate: assigned_date,
    });

    console.log(response);
  } catch (error) {
    console.error(error);
  }
};


function assignToAthletes() {
  let assigned_date = new Date(start_date.value).toISOString().split('T')[0];

  props.program.forEach(day => {
    console.log(`Day: ${day.name}`);
    day.workouts.forEach(workout => {
      //need to get the sets for each workout and make them blank?? 
      let sets = workout.blocks.map(block => 
        block.exercises.map(exercise => 
          exercise.sets.map(set => ({
        setId: set.id,
        repsCompleted: -1,
        weightCompleted: -1
          }))
        )
      ).flat(2);
      selectedAthletes.value.forEach(username => {
        console.log('assigning workout on', assigned_date, 'to', username);
        logWorkout(username, assigned_date, workout.id, sets);
      });
    });
    
    assigned_date = new Date(new Date(assigned_date).setDate(new Date(assigned_date).getDate() + 1)).toISOString().split('T')[0];
  });
  emit('showAssignment', false);
};

const { result, loading, error } = useQuery(gql` 
  query{
    allAthletesByCoach(coachUsername: "${props.coach}") {
      id
      username
      coach {
        id
        username
      }
  }
  }`,
  {
    variables() {
      return {
        coachUsername: props.coach
      };
    }
  }
);

</script> 

<template>
  <div v-if="result && result.allAthletesByCoach">
    <div v-for="athlete in result.allAthletesByCoach" :key="athlete.id">
      <input type="checkbox" :id="athlete.id" v-model="selectedAthletes" :value="athlete.username">
      <label :for="athlete.id">{{ athlete.username }}</label>
    </div>
  </div> 
  Start Date: 
 

  <VDatePicker 
      ref="calendar" 
      transparent 
      borderless 
      :color="'green'" 
      v-model="start_date"
      :attributes="attrs">
    </VDatePicker>

    <button @click="assignToAthletes"> confirm </button>
</template> 