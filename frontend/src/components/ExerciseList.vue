<script setup> 
import { ref, computed, watch } from 'vue';
import draggable from 'vuedraggable';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faPhone } from '@fortawesome/free-solid-svg-icons';
import { useUserStore } from "@/store/user";
import { useMutation, useQuery } from "@vue/apollo-composable";
import { ADD_EXERCISE_NAME } from '@/mutations';
import gql from 'graphql-tag';
import SearchBar from './SearchBar.vue';
import { add } from 'date-fns';

const userStore = useUserStore();
const username = userStore.getUser.username;
const showList = ref(false);
const numSets = ref('');
const numBlocks = ref('');
const props = defineProps({
  workout: {
    type: Object,
    required: true,
  },
  currentDay: {
    type: Boolean,
    required: true,
  }
});

const sets = ref([{ weight: '', reps: '' }]);
const currentExercise = ref(props.workout.blocks[0].exercises[0]);
const currentBlock = ref(props.workout.blocks[0]);

/* REPLACED WITH #BLOCKS AND #SETS INPUTS


const deleteSet = (index) => {
  currentExercise.value.sets.splice(index, 1);
};

const deleteBlock = (index) => {
  props.workout.blocks.splice(index, 1);
};
*/

const addSet = () => {
  currentExercise.value.sets.push({ order: '', weight: '', reps: '' });
};

const deleteExercise = (block, index) => {
  block.exercises.splice(index, 1);
};



const saveExercise = () => {
  if (currentExercise.value.name.trim() === '') {
    const index = currentBlock.value.exercises.indexOf(currentExercise.value);
    currentBlock.value.exercises.splice(index, 1);
  }
  currentExercise.value = props.workout.blocks[0].exercises[0];
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

const { mutate: addExerciseNameMutation } = useMutation(ADD_EXERCISE_NAME);

const addExerciseName = async (name) => {
  try {
    const response = await addExerciseNameMutation({
      name: name,
      author: username,
    });
    console.log(response);
  } catch (error) {
    console.error(error);
  }
};

const { result: exerciseNames, loading, error } = useQuery(gql` 
  query{
    exerciseNamesByAuthor(author: "${username}") {
      name
    }
  }`,
  {
    variables() {
      return {
        author: username
      };
    }
  }
);

watch(() => numBlocks.value, (newVal) => {
  if (newVal > props.workout.blocks.length) {
    for (let i = props.workout.blocks.length; i < newVal; i++) {
      addBlock();
    }
  }
  else {
    props.workout.blocks = props.workout.blocks.slice(0, newVal);
  }
});

const updateSets = (exercise) => {
  if (exercise.numSets > exercise.sets.length) {
    for (let i = exercise.sets.length; i < exercise.numSets; i++) {
      exercise.sets.push({ weight: '', reps: '' });
    }
  }
  else {
    exercise.sets = exercise.sets.slice(0, exercise.numSets);
  }
};


</script>

<template>
  <div class='main-container'>
    <div v-if="currentDay"> 
      # Blocks 
      <select v-model="numBlocks">
        <option v-for="n in 11" :key="n-1" :value="n-1">{{ n-1 }}</option>
      </select>
    </div>

    <div v-for="(block, index) in workout.blocks" class="p-block-div">
      <draggable v-model="block.exercises" tag="ul" group="exercises" itemKey="">
        <template #item="{element: exercise, index}">
          <li>
            <!-- non-edit mode <button  
             @click="expandExercise(exercise)">edit</button>
              <button @click="deleteExercise(block, index)"><font-awesome-icon icon="trash"/></button>
            -->
            <div v-if="!currentDay" class="title-row">
              <div>  
                {{exercise.name}} 
                <br/> 
                <p style="font-size: 12px;">
                  {{ exercise.sets.length }} x {{ exercise.sets.map(set => set.reps).join(', ') }}
                </p> 
              </div>
              
            </div>
            <div v-else class="exercise-container editing">
              <!--- edit mode -->
              Exercise <SearchBar 
                        :selectedItem="exercise"
                        :items="exerciseNames.exerciseNamesByAuthor" 
                        @update:selectedItem="currentExercise.name = $event.name"/>
              <br/>
              
              <div class="sets" v-if="exercise.name">
                <label> # Sets </label>
                <select v-model="exercise.numSets" @change="updateSets(exercise)">
                  <option v-for="n in 21" :key="n-1" :value="n-1">{{ n-1 }}</option>
                </select>
                <table v-if="exercise.numSets > 0">
                  <tr>
                    <td>Weight </td>
                    <td v-for="set, index in exercise.sets" :key="index">
                      <input class="set-detail" type="number" v-model="set.weight" />
                    </td>
                  </tr>
                  <tr>
                    <td>Reps</td>
                    <td v-for="set, index in exercise.sets" :key="index">
                      <input class="set-detail" type="number" v-model="set.reps"/>
                    </td>
                  </tr>
                  <tr>
                   
                  </tr>
                </table>
              </div>
            </div>
          </li>
        </template>
      </draggable>
      <button v-if="currentDay" @click="addExercise(block)"><font-awesome-icon icon="plus"/></button>
    </div>

  </div>

  <!--<div class="title-row">
         LOGIC TO ADD NEW EXERCISE NAME-- NOT SURE WHERE TO PUT YET 
        <input type="text" v-model="newExerciseName" placeholder="New Exercise Name" />
        <button @click="addExerciseName(newExerciseName)">Add Exercise</button>
        <font-awesome-icon icon="trash" @click="deleteBlock(index)"/>
      </div>-->

       <!--
                <input type="text" v-model="currentExercise.description" placeholder="Notes" style="width: 150px;"/> 

                <button @click="saveExercise">Save</button>
                
                <button @click="addBlock" style="width: 100px">add block</button>
                -->
     <!-- NOT NEEDED DUE TO SET # INPUT                
                    <button @click="addSet">+</button>
                    <td v-for="set, index in currentExercise.sets" :key="index">
                      <button class="delete-button" @click="deleteSet(index)">delete</button>
                    </td>
                  -->
</template>

<style scoped>

.main-container{
  display: flex;
  flex-direction: column;
  align-items: center;
  width: auto; 
  background-color: white;
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

.exercise-row{
  display: flex;
  justify-content: space-between;
  margin: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: rgb(240, 240, 240);;
}

.exercise-name{
  cursor: pointer;
  padding: 0;
  border: none; 
  border-radius: 0;
}

.exercise-name:hover{
  background-color: #f7f5f5b2;
}

.search-list{
  max-height: 50px;
  overflow-y: scroll;
  background-color: lightgray;
  width: 150px;
}

.set-detail{
  width: 50px;
}



</style>