<script setup>
import { ref } from 'vue';
import { useQuery, useMutation } from "@vue/apollo-composable";
import gql from "graphql-tag";
import { useUserStore } from "@/store/user";

const title = ref('');
const body = ref('');
const userStore = useUserStore();
const tags = ref([]);
const sets = ref([{ weight: '', reps: '' }]);
const exercises = ref([]);
const days = ref([]);
const exercise_states = ref([]);
const blocks = ['A', 'B', 'C', 'D', 'E', 'F'];

const addSet = (exercise) => {
  exercise.sets.push({ weight: '', reps: '' });
};

const deleteSet = (index) => {
  sets.value.splice(index, 1);
};

const addExercise = (workout) => {
  console.log(workout);
  workout.exercises.push({ name: '', 
    sets: [{
      weight: '',
      reps: ''
    }],
  }
  );
};

const expandExercise = (exercise) => {
  exercise_states.value[exercise] = !exercise_states.value[exercise];
};

const deleteExercise = (workout, index) => {
  workout.exercises.splice(index, 1);
};

//add logic to number the days as keys in the days dictionary, etc. 
const addDay = () => {
  const day_number = days.value.length + 1;
  days.value.push({ number: day_number, workouts: [] });
};

const deleteDay = (number) => {
  const dayIndex = days.value.findIndex(day => day.number === number);
  if (dayIndex !== -1) {
    days.value.splice(dayIndex, 1);
  }
  //need to fix bug here for numbering days after deleting an earlier day
};

const addWorkout = (day) => {
  day.workouts.push({ type: 'strength', exercises: [], blocks: [] });
};

const saveExercise = (workout) => {
  workout.exercises.push(workout);
};


const CREATE_PROGRAM = gql`
  mutation CreateProgram($title: String!, $body: String!, $slug: String!, $author: String!, $tags: [String!]) {
    createProgram(title: $title, body: $body, slug: $slug, author: $author, tags: $tags) {
      program {
        id
        title
        body
        slug
      }
    }
  }
`;

const createProgram = useMutation(CREATE_PROGRAM, {
  variables() {
    return {
      title: title.value,
      body: body.value,
      slug: title.value.toLowerCase().replace(/\s+/g, '-'),
      author: userStore.getUser.username,
      tags: tags.value
    };
  }
});

const addProgram = async () => {
  try {
    const response = await createProgram.mutate({
      title: title.value,
      body: body.value,
      slug: title.value.toLowerCase().replace(/\s+/g, '-'),
      author: userStore.getUser.username, // Get the current user
      tags: tags.value
    });
    title.value = '';
    body.value = '';
  } catch (error) {
    console.error(error);
  }
  console.log(response);
};


</script>

<template>

  <div class="container">
    <form @submit.prevent="">
      <input type="text" id="title" v-model="title" placeholder="Program Name" style="width: 300px"/>
      <div class="days">
      <div class="day-container" v-for="day, index in days" :key="index">
          Day {{ day.number }}
        <div class="workout-container" v-for="(workout, index) in day.workouts" :key="index" :class="workout.type">
            <select id="workout-type" v-model="workout.type" style="width: 100px;">
            <option value="strength">Strength</option>
            <option value="cardio">Cardio</option>
          </select>
          
            <div class="exercise-container" v-for="exercise, index in workout.exercises" :key="index" :class="`block${exercise.block}`">            
            <div v-if="exercise_states[index]" style="display: flex;">
                <p style="margin-left: 20px;">
                  {{ exercise.name }} 
                  <button class="edit-button" @click="expandExercise(index)">edit</button>
                </p>
                
                <button class="delete-exercise delete-button" @click="deleteExercise(workout, index)">
                X
              </button>
            </div>
            <div v-else>
              <input type="text" v-model="exercise.name" placeholder="Exercise Name" style="width: 150px;"/>
                <select v-model="exercise.block">
                  <option v-for="block in blocks" :value="block">{{ block }}</option>
                </select>
              <button class="delete-exercise delete-button" @click="deleteExercise(workout, index)">
                X
              </button>
          
            <table>
              <tr>
                
                <td v-for="set in exercise.sets" :key="set.index">
                  <input type="number" v-model="set.weight" step="1" placeholder="weight"/>
                </td>
                <button @click="addSet(exercise)">+</button>
              </tr>
              
              <tr>
                <td v-for="set in exercise.sets" :key="set.index">
                  <input type="number" v-model="set.reps" step="1" placeholder="reps"/>
                </td>
              </tr>
              <tr>
                <td v-for="set in exercise.sets" :key="set.index">
                  <button class="delete-button" @click="deleteSet(set.index)">X</button>
                </td>
              </tr>
            </table>
            <button @click="expandExercise(index)">done</button>
          </div>
          
          </div>
          <button @click="addExercise(workout)">add exercise</button>


        </div>
        <button style="width: 100px;" @click="addWorkout(day)">Add Workout</button>
      </div>
      <button style="height: 50px;" @click="addDay(index)">Add Day</button>
      </div> 
      {{ days }}
      <textarea id="body" v-model="body" placeholder="Notes"></textarea>
      <button type="submit">submit</button>
    </form>


  </div>
  
</template>

<style scoped>
  label {
    display: block;
    margin-top: 1rem;
  }
  input, textarea {
    width: 100%;
    padding: 0.5rem;
    margin-top: 0.5rem;
    background-color: white;
  }
  button {
    margin-top: 1rem;
    padding: 0.5rem;
    border-radius: 4px;
  }
  button:hover {
    cursor: pointer;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
  }
  td{
    width: 75px;
  }

  .days{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
  }
  .day-container{ 
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
    background-color:#f7f5f5b2;
    border-radius: 5px;
    width: 400px;
    margin: 10px;
    display: flex; 
    justify-content: center;
    flex-direction: column;
    align-items: center;

    .delete-button{
      background-color: transparent;
      color: black;
      margin-left: auto;
    }
  }
  .exercise-container{
    border: 2px solid black; 
    margin: 10px;
    background-color: white;
  }

  .workout-container{
    background: lightgray;
    display: flex;
    flex-direction: column;
    margin: 5px;
    width: 95%;
  }

  .blockA{
    border: 3px solid var(--dodger-blue);
  }

  .blockB{
    border: 3px solid var(--flame-orange);
  }

  .blockC{
    border: 3px solid var(--lime-green);
  }

  .blockD{
    border: 3px solid var(--persian-blue);
  }

  .blockE{
    border: 3px solid var(--smoky-black);
  }

  .blockF{
    border: 3px solid var(--uranian-blue);
  }

  .cardio{
    background-color: lightyellow;
  }

  .strength{ 
    background-color: lightblue;
  }
 
  *{
    background-color: transparent;
    color: black;
  }


  .container{
    background-color: white;
    padding: 30px;
  }

  .delete-button{
    background-color: red;
    color: white;
    border: none;
    padding: 10px;
    margin: 10px;
  }

  .delete-exercise{
    margin-left: auto;
  }

  .edit-button{
    border: none;
    padding: none; 
    margin-left: 20px; 
  }

  form{
    display: flex; 
    flex-direction: column;
    align-items: center;
    
  }
</style>