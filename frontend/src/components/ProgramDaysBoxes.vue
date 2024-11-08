<script setup> 
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import WorkoutModal from './WorkoutModal.vue';
import { useMutation } from "@vue/apollo-composable";
import { useUserStore } from "@/store/user";
import { LOG_WORKOUT } from '@/mutations';

const props = defineProps({
  program_id: {
    type: String,
    required: true,
  },
  allowAssignment: {
    type: Boolean,
    required: false,
    default: true,
  }
});



const { result, loading, error } = useQuery(gql`
  query{
    programDays(programId: "${props.program_id}") {
      id
      name
      orderInProgram
      workouts{
        id 
        type
        orderInDay
        blocks{
          id
          name
          orderInWorkout
          exercises{
            id
            name
            description 
            orderInBlock
            sets{
              id
              reps
              weight
              number
            }
          }
        }
      }
    }
}
`);

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

function assignToAthletes(usernames, start_date) {
  let assigned_date = new Date(start_date).toISOString().split('T')[0];

  result.value.programDays.forEach(day => {
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
      usernames.forEach(username => {
        console.log('assigning workout on', assigned_date, 'to', username);
        logWorkout(username, assigned_date, workout.id, sets);
      });
    });
    
    assigned_date = new Date(new Date(assigned_date).setDate(new Date(assigned_date).getDate() + 1)).toISOString().split('T')[0];
  });
};


</script>

<template> 
  <div v-if="result && result.programDays" style="border-top: 2px solid black">
    <button v-show="allowAssignment" @click="assignToAthletes(['athlete1'], new Date())"> Assign Program</button>
    {{ result.programDays }}
    <div class="program-days-boxes">
      <div v-for="day in result.programDays" :key="day.id" class="program-day-box">
        <div class="day-name">{{ day.name }}</div> 
          <div v-for="workout in day.workouts" :key="workout.id" class="workout-box" :class="workout.type">
            <div class="workout-type">
              <div class="title-row">
              {{ workout.type }}
              <WorkoutModal 
                :workout="workout" 
              />
              </div>
              <div v-for="block in workout.blocks" :key="block.id" class="p-block-div">
                <div v-for="exercise in block.exercises" :key="exercise.id">
                  {{ exercise.name }} <br/>
                  <div class="set-list">
                    {{ exercise.sets.map(set => `${set.reps} @ ${set.weight}`).join(', ') }}
                  </div>
                </div>
              </div>  
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

.program-days-boxes {
  display: flex;
  flex-wrap: wrap;
}

.program-day-box{
  padding: 10px;
}

.workout-box{
  margin: 10px;
  padding: 10px;
  background-color: lightgray; 
}

.day-name{
  display: flex; 
  justify-content: center;
}
</style> 