<script setup>
import { useUserStore } from "@/store/user";
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { ref } from "vue";
import WODs from '../components/WODs.vue';

const userStore = useUserStore();
const router = useRouter();
const user = ref({
  isAuthenticated: false, 
  token: userStore.getToken || "", 
  info: userStore.getUser || {}
})

/*content: change font color 
  highlight: change background color
  fillMode: light, dark, none
  color: green, red, blue, yellow, orange, purple, pink, teal, cyan, lime, amber, brown, grey, white, black
  dot: puts dot below date
  POPOVER  can have a brief description of the workout (this is only helpful on desktop)
  */


onMounted(() => {
  if (!user.value.token) {
    router.push("/login");
  }
  else{
    user.value.isAuthenticated = true; 
  }
});

</script> 

<template>
  <h1> welcome to home page </h1>

  <div class="wod-container"> 
    <WODs />
   
  </div>
 
</template>

<style scoped>
  * {
    text-align: center;
  }
  
  .wod-container {
    border: 3px solid green;
    margin: auto;
    padding: 10px;
    width: 50%;
  }
</style>