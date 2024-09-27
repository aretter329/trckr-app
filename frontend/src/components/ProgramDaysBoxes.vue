<script setup> 

const props = defineProps({
  days: {
    type: Object,
    required: true,
  }
});



</script>

<template>
  <div class="program-days-boxes">
    <div v-for="day in days" :key="day.id" class="program-day-box">
      <div class="day-name">{{ day.name }}</div> 
      <div v-for="workout in day.workouts" :key="workout.id" class="workout-box"
      :style="'background: var(' + workout.type.color + '); '">
        {{ workout.type.name }}
        <div v-for="exercise in workout.exercises" :key="exercise.id" class="exercise-box">
          {{ exercise.title }} (sets & reps)
        </div>
      </div>
    </div>
  </div>

</template>

<style scoped>
*{
  border-radius: 5px;
}
.program-days-boxes {
  display: flex;
  flex-wrap: wrap;
}

.program-day-box{
  border: 1px solid gray;
  margin: 10px;
  padding: 10px;
  background-color: lightgray;
}

.workout-box{
  margin: 10px;
  padding: 10px;
  border: 1px solid gray;
}
.day-name{
  display: flex; 
  justify-content: center;
}
</style> 