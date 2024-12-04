<script setup>
import { ref, watch } from 'vue';
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
const days = ref([]);
const day_states = ref([]);
const program_id = ref();
const numDays = ref('');
const showNotes = ref(false);
const isEditing = ref(false);
const currentDay = ref();

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

watch(() => numDays.value, (newVal) => {
  if (newVal > days.value.length) {
    for (let i = days.value.length; i < newVal; i++) {
      addDay();
    }
  }
  else {
    days.value = days.value.slice(0, newVal);
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
    <div style="display: flex;">
      <input 
        type="text" 
        v-model="title" 
        class='title-input'
        :class="{ editable: isEditing }" 
        @blur="isEditing = false" 
        @focus="isEditing = true" 
        placeholder="Untitled Program"
        @keydown.enter="$event.target.blur()"
      />
      <div> # Days 
        <select v-model="numDays">
          <option v-for="n in 21" :key="n-1" :value="n-1">{{ n-1 }}</option>
        </select>
      </div>
    </div>
    <div class="days">
      <div class="day-container " :class="{ 'current-day': currentDay === day }" v-for="day, index in days" :key="index" @click="currentDay=day">
        <div class="day-title">
          <span> Day {{ index + 1 }} </span>
        </div>

        <div>
          <div class="workout-container" v-for="(workout, index) in day.workouts" :key="index" :class="workout.type">
            <div class="centered-row">
              <div v-if="currentDay == day" class="title-row">
                <select id="workout-type" v-model="workout.type" style="width: 100px;">
                  <option value="strength">Strength</option>
                  <option value="cardio">Cardio</option>
                </select>
                <button @click="deleteWorkout(day, index)" class="delete-button">delete workout</button>
              </div>
            </div>
            <ExerciseList :workout="workout" :currentDay="currentDay == day"/>
          </div>
         
        <button v-if="currentDay == day" style="width: 100px;" @click="addWorkout(day)">Add Workout</button>
      </div>
        
      </div>
      <!-- old logic to add days 
       <button style="height: 35px;" @click="addDay(index)"><font-awesome-icon icon="plus" /></button>
       -->
       <!-- old logic to delete day 
           <button class="right-button" @click="deleteDay(day.number)">(delete day)</button>

           <span style="margin-left: 50px;"> 
            <input type="checkbox" v-model="day.isRestDay" />Rest Day 
          </span>
           -->
    </div> 
    <div class="bottom-row">
      <button v-show="!showNotes" @click="showNotes = true"> Add Note </button>
      <textarea v-if="showNotes" style="width: 50%" id="notes" v-model="notes" placeholder="Notes"></textarea>
      <button type="submit" @click="addProgram()">Save</button>
    </div>
  </div>
</template>

<style scoped>

  .container{
    height: 85vh;
    width: 80vw;
    display: flex;
    flex-direction: column;
  }
  
  label {
    display: block;
    margin-top: 1rem;
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
    align-items: center;
    overflow-x: scroll;
    max-width: 80vw;
    height: 100%;
  }

  .day-container{ 
    background-color:#f7f5f5b2;
    border-radius: 5px;
    min-width: 150px;
    margin: 10px;
    display: flex; 
    height: 100%;
    flex-direction: column;
    align-items: center;

    .delete-button{
      background-color: transparent;
      color: black;
      margin-left: auto;
    }
  }

  .day-container:hover{
    cursor: pointer;
  }

  button{
    border: none
  }

  .current-day{
    min-width: 400px;
    overflow-y: auto;

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

  .title-input {
    font-size: 2rem;
    font-weight: bold;
    text-align: center;
    border: none;
    background: transparent;
    outline: none;
    cursor: pointer; 
  }

  input.editable {
    cursor: text; 
    border-bottom: 2px solid lightgray; 
  }

  input:focus {
    background: #f9f9f9;
  }

  .bottom-row{
    border: 1px solid blue; 
    position: absolute;
    bottom: 10%;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .day-title{
    display: flex; 
    flex-direction: row;
    justify-content: space-between;
  }
  
</style>