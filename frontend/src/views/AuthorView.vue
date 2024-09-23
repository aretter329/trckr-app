<script setup>
import ProgramList from "../components/ProgramList.vue";

import { useRoute } from "vue-router";
import { useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";

const route = useRoute();
const username = route.params.username;
const { result, loading, error } = useQuery(gql`
query {
    authorByUsername(
      username: "${username}"
    ) {
        
        username
        
        programSet {
          title
          slug
        }
      }
  }
`);

</script>

<template>
  <div v-if="loading">Loading...</div>
  <div v-else-if="error">{{ error.message }}</div>
  <section v-else :set="author = result.authorByUsername">
    <h2>{{ author.username }}</h2>
    
    <h3>Posts</h3>
    <ProgramList
      v-if="author.programSet"
      :programs="author.programSet"
      :showAuthor="false"
    />
    <p v-else>The author hasn't posted yet.</p>
  </section>
</template>

<style scoped>
  h2 {
    color: red;
  }
</style>