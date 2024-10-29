<script setup>
import { ref } from 'vue';
import { useMutation } from "@vue/apollo-composable";
import { useUserStore } from "@/store/user";
import { LOG_WORKOUT } from '@/mutations';
const userStore = useUserStore();

const props = defineProps({
  workout: {
    type: Object,
    required: true,
  }
});

const date = ref();

const loggedWorkout = useMutation(LOG_WORKOUT, {
  variables() {
    return {
      athleteUsername: userStore.getUser.username,
      workoutId: props.workout.id,
      sets: sets.value,
      notes: ''
    };
  }
});

const logWorkout = async () => {
  date.value = new Date().toISOString();
  try {
    const response = await loggedWorkout.mutate({
      athleteUsername: userStore.getUser.username,
      workoutId: props.workout.id,
      sets: sets.value,
      notes: ''
    });

    console.log(response);
  } catch (error) {
    console.error(error);
  }
};


const sets = ref(props.workout.blocks.flatMap(block => block.exercises.flatMap(exercise => exercise.sets.map(set => ({
  setId: set.id
})))));

const showModal = ref(false);

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const currentBlock = ref(props.workout.blocks[0]);
</script>

<template>
  <div>
    <button @click="openModal">Log workout</button>

    <div v-if="showModal" class='modal' style="display: flex">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <div v-for="block in workout['blocks']" class="p-block-div block" @click="currentBlock=block">
          <div v-for="exercise in block['exercises']" class="exercise">
            {{ exercise['name'] }}
            <table v-show="block == currentBlock">
                <tr>
                <td> Weight </td>
                <td v-for="set in exercise['sets']">
                  <input type="number" :placeholder="set['weight']" v-model="sets.find(s => s.setId === set.id).weightCompleted" />
                
                </td>
              </tr>
                <tr>
                <td> Reps </td>
                <td v-for="set in exercise['sets']">
                  <input type="number" :placeholder="set['reps']"  v-model="sets.find(s => s.setId === set.id).repsCompleted"/>
                </td>
              </tr> 
              Notes: {{ exercise['description'] }}
            </table>           
          </div>
        </div> 
        {{  sets }}
        <button @click="logWorkout()">Complete workout</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal {
  display: none; 
  position: fixed; 
  z-index: 1; 
  left: 0;
  top: 0;
  width: 100%; 
  height: 100%; 
  overflow: auto; 
  background-color: rgba(0, 0, 0, 0.4); 
}

.modal-content {
  background-color: #fefefe;
  margin: 5% auto; 
  padding: 20px;
  border: 1px solid #888;
  width: 80%; 
}

/* Style for the close button */
.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

input{
  width: 50px;
}

/* Style for the blocks */
.block {
  width: 90%;
  margin: auto;
  margin-top: 10px;
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