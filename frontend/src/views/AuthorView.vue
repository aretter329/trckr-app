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
        bio
        user {
          firstName
          lastName
          username
        }
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
    <h2>{{ author.user.username }}</h2>
    <template v-if="author.user.firstName && author.user.lastName">
      <h3>{{ author.user.firstName }} {{ author.user.lastName }}</h3>
    </template>
    <p v-if="author.bio">
      {{ author.bio }}
    </p>
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