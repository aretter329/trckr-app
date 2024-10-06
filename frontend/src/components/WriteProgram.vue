<script setup>
import { ref } from 'vue';
import { useMutation } from "@vue/apollo-composable";
import { useUserStore } from "@/store/user";
import { ADD_PROGRAM, ADD_DAY, ADD_WORKOUT, ADD_EXERCISE, ADD_SET } from '@/mutations';

const title = ref('');
const notes = ref('');
const userStore = useUserStore();
const tags = ref([]);
const sets = ref([{ weight: '', reps: '' }]);
const days = ref([]);
const exercise_states = ref([]);
const day_states = ref([]);
const blocks = [1,2,3,4,5,6];
const program_id = ref();

const addSet = (exercise) => {
  let order = exercise.sets.length + 1;
  exercise.sets.push({ order: order, weight: '', reps: '' });
};

const deleteSet = (index) => {
  sets.value.splice(index, 1);
};

const addExercise = (workout) => {
  workout.exercises.push({ name: '', 
    sets: [{
      order: 1,
      weight: '',
      reps: '',
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
const addDay = (index) => {
  const day_number = days.value.length + 1;
  days.value.push({ name: `Day ${day_number}`, number: day_number, workouts: [] });
  day_states.value.push(true);
};

const deleteDay = (number) => {
  const dayIndex = days.value.findIndex(day => day.number === number);
  if (dayIndex !== -1) {
    days.value.splice(dayIndex, 1);
  }
  //need to fix bug here for numbering days after deleting an earlier day
};

const addWorkout = (day) => {
  let order = day.workouts.length + 1;
  day.workouts.push({ type: 'strength', order: order, exercises: [], blocks: [] });
};

const deleteWorkout = (day, index) => {
  day.workouts.splice(index, 1);
};

const createProgram = useMutation(ADD_PROGRAM, {
  variables() {
    return {
      title: title.value,
      notes: notes.value,
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
      notes: notes.value,
      slug: title.value.toLowerCase().replace(/\s+/g, '-'),
      author: userStore.getUser.username, // Get the current user
      tags: tags.value
    });

    program_id.value = response.data.createProgram.program.id;
    console.log(program_id.value);
    addDays();
    /*
    title.value = '';
    notes.value = ''; */
  } catch (error) {
    console.error(error);
  }
};

const makeDay = async (day) => {
  try {
    const response = await createDay.mutate({
      name: day.name,
      programId: program_id.value,
      orderInProgram: day.number

    });
    let day_id = response.data.createDay.day.id;
    for (let workout of day.workouts) {
      makeWorkout(workout, day_id);
    }
    
  } catch (error) {
    console.error(error);
  }
};

const addDays = () => {
  days.value.forEach(day => {
    makeDay(day);
  });
};

const createDay = useMutation(ADD_DAY, {
  variables() {
    return {
      name: '',
      program: program_id.value,
      orderInProgram: ''
    };
  }
});

const makeWorkout = async (workout, day_id) => {
  try {
    const response = await createWorkout.mutate({
      type: workout.type,
      dayId: day_id,
      orderInDay: workout.order
    });
    
    let workout_id = response.data.createWorkout.workout.id;
    for (let exercise of workout.exercises) {
      makeExercise(exercise, workout_id);
    }
    
  } catch (error) {
    console.error(error);
  }
};

const createWorkout = useMutation(ADD_WORKOUT, {
  variables() {
    return {
      type: '',
      dayId: '',
      orderInDay: ''
    };
  }
});

const makeExercise = async (exercise, workout_id) => {
  try {
    const response = await createExercise.mutate({
      name: exercise.name,
      workoutId: workout_id,
      block: exercise.block,
      description: exercise.description,
      orderInBlock: exercise.order
    });
    let exercise_id = response.data.createExercise.exercise.id;
    for (let set of exercise.sets) {
      makeSet(set, exercise_id);
    }
  } catch (error) {
    console.error(error);
  }
};

const createExercise = useMutation(ADD_EXERCISE, {
  variables() {
    return {
      name: '',
      workoutId: '',
      block: '',
      description: '',
    };
  }
});

const makeSet = async (set, exercise_id) => {
  try {
    const response = await createSet.mutate({
      weight: set.weight,
      reps: set.reps,
      exerciseId: exercise_id,
      number: set.order
    });
  } catch (error) {
    console.error(error);
  }
};

const createSet = useMutation(ADD_SET, {
  variables() {
    return {
      weight: '',
      reps: '',
      exerciseId: '',
      number: ''
    };
  }
});




</script>

<template>

  <div class="container">
    <input type="text" id="title" v-model="title" placeholder="Program Name" style="width: 300px"/>
    <div class="days">
      <div class="day-container" v-for="day, index in days" :key="index">
        <div class="title-button" style="display: flex;">
          {{ day.name }}
          <button class="edit-button" @click="deleteDay(day.number)">(delete day)</button>
        </div>
        
          
          <div class="workout-container" v-for="(workout, index) in day.workouts" :key="index" :class="workout.type">
            <div class="centered-row">
              <select id="workout-type" v-model="workout.type" style="width: 100px;">
                <option value="strength">Strength</option>
                <option value="cardio">Cardio</option>
              </select>
              <button @click="deleteWorkout(day, index)" class="delete-button">delete workout</button>
            </div>
            <div class="exercise-container" v-for="exercise, index in workout.exercises" :key="index" :class="`block${exercise.block}`">            
              <div v-if="exercise_states[index]" style="display: flex;">
                <p style="margin-left: 20px;">
                  {{ exercise.name }} 
                  <button class="edit-button" @click="expandExercise(index)">edit</button>
                  <button class="delete-exercise delete-button" @click="deleteExercise(workout, index)">delete</button>
                    <br/> 
                  <div style="font-size: 12px;"> {{ exercise.sets.map(set => `${set.reps} @ ${set.weight}`).join(', ') }} </div>
                </p>
                
              </div>
              <div v-else>
                <input type="text" v-model="exercise.name" placeholder="Exercise Name" style="width: 150px;"/>
                <input type="text" v-model="exercise.description" placeholder="Description" style="width: 150px;"/> 
                Block:<select v-model="exercise.block">
                  <option v-for="block in blocks" :value="block">{{ block }}</option>
                </select>
                

                <table>
                  <tr>
                    <td v-for="set in exercise.sets" :key="set.index">
                      <input type="number" v-model="set.weight" placeholder="weight"/>
                    </td>
                    <button @click="addSet(exercise)">+</button>
                  </tr>
                  <tr>
                    <td v-for="set in exercise.sets" :key="set.index">
                      <input type="number" v-model="set.reps" placeholder="reps"/>
                    </td>
                  </tr>
                  <tr>
                    <td v-for="set in exercise.sets" :key="set.index">
                      <button class="delete-button" @click="deleteSet(set.index)">(delete set)</button>
                    </td>
                  </tr>
                </table>
                <button @click="expandExercise(index)">done</button>
              </div>
            </div>
            <button style="border: none" @click="addExercise(workout)">add exercise</button>
          </div>
          <button style="width: 100px;" @click="addWorkout(day)">Add Workout</button>
        
      </div>
      <button style="height: 35px;" @click="addDay(index)">Add Day</button>
    </div> 
    {{ days }}
    <textarea style="width: 50%" id="notes" v-model="notes" placeholder="Notes"></textarea>
    <button type="submit" @click="addProgram()">Save</button>
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
  
  button:hover {
    cursor: pointer;
    font-weight: bold;
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
    width: 350px;
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

  button{
    border: none
  }

  .centered-row{
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .exercise-container{
    background-color: white;
    margin: 0px 5px 5px 5px;
    border-radius: 5px;
  
  }

  .workout-container{
    display: flex;
    flex-direction: column;
    margin: 5px;
    width: 95%;
    border-radius: 5px;
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