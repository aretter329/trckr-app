<script setup>
import { ref } from 'vue';
import { useMutation } from "@vue/apollo-composable";
import { useUserStore } from "@/store/user";
import { ADD_PROGRAM } from '@/mutations';
import ExerciseList from '@/components/ExerciseList.vue';
import VueDatePicker from '@vuepic/vue-datepicker';

import '@vuepic/vue-datepicker/dist/main.css'

const title = ref('');
const notes = ref('');
const userStore = useUserStore();
const tags = ref([]);
const days = ref([{ name: 'Day 1', number: 1, workouts: [{ type: 'strength', order: 1, blocks: [{name: 'Block 1', exercises: [{name:'', sets:[{order: '', weight:'', reps:''}]}]}] }] }]);
const day_states = ref([]);
const program_id = ref();

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
  day.workouts.push({ type: 'strength', order: order, blocks: [{name: 'Block 1', exercises: [{name:'', sets:[]}]}] });
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

const formatDays = () => {
  let formatted_days = [];
  days.value.forEach((day, index) => {
    let formatted_day = {
      name: day.name,
      orderInProgram: index,
      workouts: []
    };
    day.workouts.forEach((workout, index) => {
      let formatted_workout = {
        type: workout.type,
        orderInDay: index,
        blocks: []
      };
      workout.blocks.forEach((block, index) => {
        let formatted_block = {
          name: block.name,
          orderInWorkout: index,
          exercises: []
        };
        block.exercises.forEach((exercise, index) => {
          let formatted_exercise = {
            name: exercise.name,
            description: exercise.description,
            orderInBlock: index,
            sets: []
          };
          exercise.sets.forEach((set, index) => {
            let formatted_set = {
              weight: set.weight,
              reps: set.reps,
              number: index
            };
            formatted_exercise.sets.push(formatted_set);
          });
          formatted_block.exercises.push(formatted_exercise);
        });
        formatted_workout.blocks.push(formatted_block);
      });
      formatted_day.workouts.push(formatted_workout);
    });
    formatted_days.push(formatted_day);
  });
  return formatted_days;
};

const addProgram = async () => {
  let days_input = formatDays();
  console.log(days_input);
  try {
    const response = await createProgram.mutate({
      title: title.value,
      notes: notes.value,
      slug: title.value.toLowerCase().replace(/\s+/g, '-'),
      author: userStore.getUser.username, // Get the current user
      tags: tags.value,
      assignedAthletes: [],
      days: days_input
    });

    program_id.value = response.data.createProgram.program.id;
    console.log(program_id.value);
    //addDays();
    /*
    title.value = '';
    notes.value = ''; */
  } catch (error) {
    console.error(error);
  }
};
</script>

<template>

  <div class="container">
    {{ days}}
    <input type="text" id="title" v-model="title" placeholder="Program Name" style="width: 300px"/>
    <div class="days">
      <div class="day-container" v-for="day, index in days" :key="index">
        <div class="title-row">
          <span style="flex-grow: 1; text-align: center;"> Day {{ index + 1 }} </span>
          <button class="right-button" @click="deleteDay(day.number)">(delete day)</button>
        </div>
         
        <!-- the colored row; workout type drop down, delete button-->
          <div class="workout-container" v-for="(workout, index) in day.workouts" :key="index" :class="workout.type">
            <div class="centered-row">
              <select id="workout-type" v-model="workout.type" style="width: 100px;">
                <option value="strength">Strength</option>
                <option value="cardio">Cardio</option>
                <option value="rest">Rest</option>
              </select>
                <VueDatePicker v-model="workout.date"></VueDatePicker>
              <button @click="deleteWorkout(day, index)" class="delete-button">delete workout</button>
            </div>
            <ExerciseList :workout="workout"/>
          </div>
         
        <button style="width: 100px;" @click="addWorkout(day)">Add Workout</button>
        
      </div>
      <button style="height: 35px;" @click="addDay(index)">Add Day</button>
    </div> 
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

  #workout-type{
    margin: 10px;
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
    background-color: var(--cardio-color);
  }

  .strength{ 
    background-color: var(--strength-color);
  }

  .rest{
    background-color: gray;
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

  

  form{
    display: flex; 
    flex-direction: column;
    align-items: center;
  }
  
</style>