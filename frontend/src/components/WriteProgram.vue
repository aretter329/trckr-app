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

const deleteExercise = (index) => {
  exercises.value.splice(index, 1);
};

//add logic to number the days as keys in the days dictionary, etc. 
const addDay = () => {
  days.value.push({ name: '', workouts: [] });
};

const deleteDay = (index) => {
  days.value.splice(index, 1);
};

const addWorkout = (day) => {
  day.workouts.push({ type: 'strength', exercises: [] });
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
      <label for="title">Title</label>
      <input type="text" id="title" v-model="title" />
      <div class="days">
      <div class="day-container" v-for="day, index in days" :key="index">
        <div style="display: flex;">
        Day {{ index+1 }}
        <button class="delete-day delete-button" @click="deleteDay(index)">
          X
        </button>
        </div>

        <div class="workout-container" v-for="workout, index in day.workouts" :key="index">
          <label for="workout-type">type</label>
          <select id="workout-type" v-model="workout.type">
            <option value="strength">Strength</option>
            <option value="cardio">Cardio</option>
          </select>
          
          <div class="exercise-container" v-for="exercise, index in workout.exercises" :key="index">
            <div style="display: flex;">
              <label for="name" style="padding-right: 10px;">Exercise Name</label>
              <input type="text" v-model="exercise.name" style="width: 150px;"/>
              <button class="delete-exercise delete-button" @click="deleteExercise(index)">
                X
              </button>
            </div>
            
          
            <table>
              <tr>
                <th>
                  Set
                </th>
                <th v-for="set, index in exercise.sets" :key="index">
                  {{ index+1 }}
                </th>
                <th> 
                  <button class="add-button" @click="addSet(exercise)">+</button>
                </th>
              </tr>
              <tr>
                <td>Weight</td>
                <td v-for="set in exercise.sets" :key="set.index">
                  <input type="text" v-model="set.weight" />
                </td>
              </tr>
              <tr>
                <td>Reps</td>
                <td v-for="set in exercise.sets" :key="set.index">
                  <input type="text" v-model="set.reps" />
                </td>
              </tr>
              <tr>
                <td></td>
                <td v-for="set in exercise.sets" :key="set.index">
                  <button class="delete-button" @click="deleteSet(set.index)">X</button>
                </td>
              </tr>
            </table>
          
          </div>
          <button class="add-button" @click="addExercise(workout)">add exercise</button>


        </div>
        <button class="add-button" @click="addWorkout(day)">Add Workout</button>
        
      </div>
      <button class="add-button" @click="addDay()">Add Day</button>
      </div>
      <label for="body">Notes</label>
      {{ days }}
      <textarea id="body" v-model="body"></textarea>
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
  }
  button:hover {
    cursor: pointer;
    transform: translate(2px, 2px);
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
  }
  td{
    width: 75px;
  }

  .days{
    display: flex;
  }
  .day-container{ 
    border: 2px solid black; 
    width: 100%;
    margin: 10px;
    background-color: lightblue;

    .delete-button{
      background-color: transparent;
      color: black;
      margin-left: auto;
    }
  }
  .exercise-container{
    border: 2px solid black; 
    width: 100%;
    margin: 10px;
    background-color: pink;
  }

  *{
    background-color: transparent;
    color: black;
  }

  .container{
    background-color: white;
    padding: 30px;
  }

  button{ 
    border-radius: 4px;
  }

  .add-button{
    background-color: green;
    color: white;
    border: none;
    padding: 10px;
    margin: 10px;
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

</style>