<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">
        <div class="nav-link">
          Home
        </div>
      </RouterLink>
      <RouterLink to="/all-programs">
        <div class="nav-link">
          Programs
        </div></RouterLink>
    </nav>
  </header>

  <body>
    <RouterView />
  </body>
  
  
 
</template>

<style scoped>

  header {
    position: fixed; 
    top: 0; 
    left: 0; 
    right: 0;
    background-color: var(--dodger-blue);
  }

  nav {
    text-align: center;
    display: flex;
    justify-content: center;
  }
  
  nav a {
    padding: 0.5rem;
  }

  body{
    padding-top: 2rem;
    background-color: rgb(248, 247, 255)
  }

 
</style>