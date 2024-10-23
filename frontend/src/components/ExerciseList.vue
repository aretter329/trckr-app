<script setup> 
import { ref } from 'vue';
import draggable from 'vuedraggable';


const props = defineProps({
  workout: {
    type: Object,
    required: true,
  }
});

const sets = ref([{ weight: '', reps: '' }]);
const currentExercise = ref(props.workout.blocks[0].exercises[0]);
const currentBlock = ref(props.workout.blocks[0]);
//we may not need to keep track of order here if using draggable
const addSet = () => {
  currentExercise.value.sets.push({ order: '', weight: '', reps: '' });
};

const deleteSet = (index) => {
  currentExercise.value.sets.splice(index, 1);
};

const deleteExercise = (block, index) => {
  block.exercises.splice(index, 1);
};

const deleteBlock = (index) => {
  props.workout.blocks.splice(index, 1);
};

const saveExercise = () => {
  if (currentExercise.value.name.trim() === '') {
    const index = currentBlock.value.exercises.indexOf(currentExercise.value);
    currentBlock.value.exercises.splice(index, 1);
  }
  currentExercise.value = {};
}

const expandExercise = (exercise) => {
  currentExercise.value = exercise;
}

const addBlock = () => {
  const length = props.workout.blocks.length;
  props.workout.blocks.push({ name: `Block ${length + 1}`, exercises: [] });
  currentBlock.value = props.workout.blocks[length];
}

const addExercise = (block) => {
  saveExercise();
  const baseExercise = { name: '', sets: [{ weight: '', reps: '' }] };
  currentBlock.value = block;
  currentBlock.value.exercises.push(baseExercise);
  currentExercise.value = baseExercise;
}

</script>

<template>
  <div class='container'> 
  <div v-for="(block, index) in workout.blocks" :class="['block']">
    <h3>Block {{ index+1 }}</h3>
    <button class="delete-block delete-button" @click="deleteBlock(index)">delete block</button>
    <draggable v-model="block.exercises" tag="ul" group="exercises">
      <template #item="{element: exercise, index}">
        <li>
          <!-- non-edit mode --> 
          <div v-if="(currentExercise != exercise)" class="centered-row">
            <div>  {{exercise.name}} <br/> <p style="font-size: 12px;">{{ exercise.sets.map(set => `${set.reps} @ ${set.weight}`).join(', ') }}</p> </div>
            <button class="edit-button" @click="expandExercise(exercise)">edit</button>
            <button class="delete-exercise delete-button" @click="deleteExercise(block, index)">remove</button>
          </div>
          <div v-else class="exercise-container">
          <!--- edit mode -->
            <input type="text" v-model="currentExercise.name" placeholder="Exercise Name" style="width: 150px;"/>
            
            <table>
              <tr>
                <td v-for="set, index in currentExercise.sets" :key="index">
                  <input class="set-detail" type="number" v-model="set.weight" placeholder="weight"/>
                </td>
                <button @click="addSet">+</button>
              </tr>
              <tr>
                <td v-for="set, index in currentExercise.sets" :key="index">
                  <input class="set-detail" type="number" v-model="set.reps" placeholder="reps"/>
                </td>
              </tr>
              <tr>
                <td v-for="set, index in currentExercise.sets" :key="index">
                  <button class="delete-button" @click="deleteSet(index)">(delete {{ index }})</button>
                </td>
              </tr>
            </table>
            <input type="text" v-model="currentExercise.description" placeholder="Notes" style="width: 150px;"/> 

            <button @click="saveExercise">Save</button>
         
          </div>
        </li>
      </template>
      
    </draggable>
    <button @click="addExercise(block)"> + </button>
  </div>

  <button @click="addBlock" style="width: 100px">add block</button>
  
  </div>
</template>

<style scoped>

.container{
  display: flex;
  flex-direction: column;
  align-items: center;
}
.exercise-container{
  width: 100%;
  overflow-x: auto;
} 

ul{
  list-style-type: none;
  padding: 0;
}

.set-detail{
  width: 70px;
}

li{
  border: 1px solid #ccc;
  background-color: white;
  border-radius: 5px;
  padding: 10px;
  margin: 5px;
}

.centered-row{
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.block{
  background-color: white; 
  width: 100%;
  margin: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: rgb(238, 236, 236);
  padding: 10px;
}

.exercise-row{
  display: flex;
  justify-content: space-between;
  margin: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: rgb(240, 240, 240);;
}
.block:nth-child(5n+1) {
  border-left: var(--persian-blue) 5px solid;
}

.block:nth-child(5n+2) {
  border-left: var(--mikado-yellow) 5px solid;
}

.block:nth-child(5n+3) {
  border-left: var(--lime-green) 5px solid;
}

.block:nth-child(5n+4) {
  border-left: var(--uranian-blue) 5px solid;
}

.block:nth-child(5n+5) {
  border-left: var(--flame-orange) 5px solid;
}


</style>