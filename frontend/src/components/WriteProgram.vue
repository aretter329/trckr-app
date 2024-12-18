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
const errorMessage = ref('');
const navBack = ref(false);

const props = defineProps({
  existingSlugs: {
    type: Array,
    required: false,
  }
});

const emit = defineEmits(['nav-back']);

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

watch(() => navBack.value, (newVal) => {
  if(newVal){
    emit('nav-back');
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
  let slug = title.value.toLowerCase().replace(/\s+/g, '-');
  console.log('slug:', slug);
  if (props.existingSlugs.includes(slug)) {
    console.log('slug already exists');
    errorMessage.value = 'Program with this title already exists';
    return;
  }
  try {
    const response = await createProgram.mutate({
      title: title.value,
      notes: notes.value,
      slug: slug,
      author: userStore.getUser.username, // Get the current user
      tags: tags.value,
      assignedAthletes: [],
      days: days_input
    });

    program_id.value = response.data.createProgram.program.id;
    navBack.value = true;
    
    //addDays();
    /*
    title.value = '';
    notes.value = ''; */
  } catch (error) {
    console.error(error);
  }
  errorMessage.value = '';
};

</script>

<template>

  <div class="container">
    <div style="display: flex; padding-bottom: 10px;">
      <button class='simple-button' @click="navBack = true">Back to Program List</button>
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
      <div>  
        <input v-model="numDays" type="number" style="width: 40px; font-size: 22px"/>
        <span style="font-size: 22px; font-weight: bold;"> Days </span> 
          
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
         
        <button class='simple-button' v-if="currentDay == day" @click="addWorkout(day)">Add Workout</button>
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
    <div class="bottom-row" style="width: 50%;">
      <textarea style="width: 100%" id="notes" v-model="notes" placeholder="Notes"></textarea>
      <button type="submit" class="simple-button" @click="addProgram()">Save</button>
      <p> {{ errorMessage }} </p>
    </div>
  </div>
</template>

<style scoped>

  .container{
    height: 83vh;
    width: 80vw;
    display: flex;
    flex-direction: column;
    border-radius: 5px;
  }
  
  label {
    display: block;
    margin-top: 1rem;
  } 

  td{
    width: 75px;
  }

  .days{
    display: flex;
    align-items: center;
    overflow-x: scroll;
    max-width: 80vw;
    height: 90%;
  }

  .day-container{ 
    background-color: lightgray;
    border: 2px solid gray; 
    border-radius: 5px;
    min-width: 150px;
    max-width: 400px;
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
    max-width: 380px;
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
    padding-top: 10px;  
    position: absolute;
    bottom: 3%;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .day-title{
    display: flex; 
    flex-direction: row;
    justify-content: space-between;
  }
  
  .simple-button{ 
    background: var(--midnight-blue);
    color: white; 
  }
</style>