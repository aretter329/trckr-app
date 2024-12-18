<script setup> 
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { useUserStore } from "@/store/user";
import AssignmentBox from './AssignmentBox.vue';
import { ref } from 'vue';

const userStore = useUserStore();

const coach = userStore.getUser.username;

const showAssignment = ref(false);

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





</script>

<template> 
  <div v-if="result && result.programDays" class="main">
    <button class='simple-button' v-show="allowAssignment" @click="showAssignment=true"> Assign Program</button>
    <AssignmentBox v-if="showAssignment" :coach="coach" :program="result.programDays" @showAssignment="showAssignment=false"/>
    <div class="program-days-boxes">
      <div v-for="day in result.programDays" :key="day.id" class="program-day-box">
        <div class="day-name">{{ day.name }}</div> 
          <div v-for="workout in day.workouts" :key="workout.id" class="workout-box" :class="workout.type">
            <div class="workout-type">
              <div class="title-row">
              {{ workout.type }}
              </div>
              <div v-for="block in workout.blocks" :key="block.id" class="p-block-div">
                <div v-for="exercise in block.exercises" :key="exercise.id">
                  {{ exercise.name }} <br/>
                  <div class="set-list">
                    {{ exercise.sets.length }} x {{ exercise.sets.map(set => set.reps).join(', ') }}
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
  border: 3px solid gray;
  border-radius: 5px; 
}

.day-name{
  display: flex; 
  justify-content: center;
}

.main{
  display: flex; 
  flex-direction: column; 
  align-items: center;
}

.set-list{
  margin-bottom: 5px;
}
</style> 