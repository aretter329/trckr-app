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
const currentExercise = ref({ name: '', sets: [{ weight: '', reps: '' }], block: 1 });
const currentBlock = ref({ name: '', exercises: [] });
//we may not need to keep track of order here if using draggable
const addSet = () => {
  currentExercise.value.sets.push({ order: '', weight: '', reps: '' });
};

const deleteSet = (index) => {
  currentExercise.value.sets.splice(index, 1);
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

const deleteExercise = (block, index) => {
  block.exercises.splice(index, 1);
};

const appendExercise = () => {
 currentBlock.value.exercises.push(currentExercise.value);
  currentExercise.value = { name: '', sets: [{ weight: '', reps: '' }], block: 1 };
}

const expandExercise = (index) => {
  currentExercise.value = props.workout.exercises[index];
  props.workout.exercises.splice(index, 1); 
}

const addBlock = () => {
  const length = props.workout.blocks.length;
  props.workout.blocks.push({ name: `Block ${length + 1}`, exercises: [] });
  currentBlock.value = props.workout.blocks[length];
}

</script>

<template>
  <div class='container'> 
  <div v-for="block in workout.blocks" class="block">
    <h3>{{ block.name }}</h3>
    <draggable v-model="block.exercises" tag="ul" group="exercises">
      <template #item="{element: exercise, index}">
        <li>
          <div style="display: flex;" class='exercise-row'>
            <p style="margin-left: 20px;">
              {{ exercise.name }} 
              <button class="edit-button" @click="expandExercise(index)">edit</button>
              <button class="delete-exercise delete-button" @click="deleteExercise(block, index)">remove</button>
                <br/> 
              <div style="font-size: 12px;"> {{ exercise.sets.map(set => `${set.reps} @ ${set.weight}`).join(', ') }} </div>
            </p>    
          </div>
        </li>
      </template>
    </draggable>
  </div>

  <button @click="addBlock" style="width: 100px">add block</button>
  <div class="exercise-container">            
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
          <td v-for="index in currentExercise.sets" :key="index">
            <button class="delete-button" @click="deleteSet(index)">(delete)</button>
          </td>
        </tr>
      </table>
      <input type="text" v-model="currentExercise.description" placeholder="Notes" style="width: 150px;"/> 

      <button @click="appendExercise">Add</button>
    </div>
  </div>
</template>

<style scoped>

.container{
  display: flex;
  flex-direction: column;
  align-items: center;
}
.exercise-container{
  border: 1px solid #ccc;
  padding: 10px;
  margin: 10px;
  border-radius: 5px;
  background-color: rgb(238, 236, 236);
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



</style>