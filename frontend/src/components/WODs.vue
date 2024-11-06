<script setup> 
import { useQuery } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { ref } from 'vue';
import WorkoutDisplay from './WorkoutDisplay.vue';




</script> 


<template> 
  <div class="main-content"> 
    <h1> Today's Workout </h1>
  </div>
</template> 

<style scoped> 
.main-content{ 
  border: 1px solid black;
  margin: auto;
}

</style>