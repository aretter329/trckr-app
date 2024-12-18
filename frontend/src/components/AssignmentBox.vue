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

const toggleGroupSelection = (group) => {
  group.athletes.forEach(athlete => {
    if (!selectedAthletes.value.includes(athlete.username)) {
      selectedAthletes.value.push(athlete.username);
    }
  });
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
          }))
        )
      ).flat(2);
      selectedAthletes.value.forEach(username => {
        console.log('assigning sets', sets);
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
      firstName
      lastName
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

const { result: workoutGroups } = useQuery(gql`
  query{
    workoutGroupsByCoach(coachUsername: "${props.coach}") {
      coach{
        id
        username
      }
      name
      athletes {
        id
        username
        firstName
        lastName
      }
    }
  }
`,
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
  <div style="display: flex;">
    <div style="display: flex; flex-direction: column; align-items: center;" class="sub-box"> 
      Start Date: 
      <VDatePicker 
        ref="calendar" 
        transparent 
        borderless 
        :color="'green'" 
        v-model="start_date"
        :attributes="attrs">
      </VDatePicker>
    </div>

    <div class="sub-box">
      <h3> Workout Groups </h3>
      <div v-if="workoutGroups && workoutGroups.workoutGroupsByCoach">
        <div v-for="group in workoutGroups.workoutGroupsByCoach" :key="group.name">
          <input type="checkbox" :id="group.name" @change="toggleGroupSelection(group)" />
          <label :for="group.name">{{ group.name }}</label>
        </div>
      </div>
    </div>

    <div style="margin-left: 50px;" class="sub-box">
      <h3> Athletes </h3>
      <div v-if="result && result.allAthletesByCoach">
        <div v-for="athlete in result.allAthletesByCoach" :key="athlete.id">
          <input type="checkbox" :id="athlete.id" v-model="selectedAthletes" :value="athlete.username">
          <label :for="athlete.id"> {{ athlete.firstName && athlete.lastName ? athlete.firstName + ' ' + athlete.lastName : athlete.username }}</label>
        </div>
      </div>
    </div>
    
  </div>
    <button class='simple-button' style='font-weight: bold;' @click="assignToAthletes"> confirm </button>
</template> 

<style scoped>
  .sub-box {
    margin-left: 50px;
    margin-right: 50px;
    padding: 10px; 
  }

  input{
    margin-right: 5px;
  }

</style> 