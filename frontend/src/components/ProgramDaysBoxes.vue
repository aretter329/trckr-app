<script setup> 
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
const props = defineProps({
  program_id: {
    type: String,
    required: true,
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
        exercises{
          id
          name
          description 
          block
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
`);
</script>

<template> 
  <div v-if="result && result.programDays">
    <div class="program-days-boxes">
      <div v-for="day in result.programDays" :key="day.id" class="program-day-box">
        <div class="day-name">{{ day.name }}</div> 
          <div v-for="workout in day.workouts" :key="workout.id" class="workout-box" :class="workout.type">
            <div class="workout-type">
              {{ workout.type }}
              <div v-for="exercise in workout.exercises" :key="exercise.id" class="exercise-box">
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
</template>

<style scoped>
*{
  border-radius: 5px;
}
.program-days-boxes {
  display: flex;
  flex-wrap: wrap;
}

.program-day-box{
  border: 1px solid gray;
  margin: 10px;
  padding: 10px;
  background-color: lightgray;
}

.workout-box{
  margin: 10px;
  padding: 10px;
  border: 1px solid gray;
}

.day-name{
  display: flex; 
  justify-content: center;
}

.exercise-box{
  margin: 5px;}

.strength{
  background-color: var(--strength-color);
}

.cardio{
  background-color: var(--cardio-color);
}

.rest{
  background-color: gray;
}

</style> 