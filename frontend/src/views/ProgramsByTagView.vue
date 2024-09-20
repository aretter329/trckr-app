<script setup>
import ProgramList from "../components/ProgramList.vue";
import { useRoute } from "vue-router";
import { useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";

const route = useRoute();
const tag = route.params.tag;
const { result, loading, error } = useQuery(gql`
  query {
    postsByTag(
      tag: "${tag}"
    ) {
        title
        slug
        author {
          user {
            username
            firstName
            lastName
          }
        }
      }
    }
`);

</script>

<template>
  <div v-if="loading">Loading...</div>
  <div v-else-if="error" class="warn">{{ error.message }}</div>
  <section v-else :set="tagPrograms = result.programsByTag">
    <h2>Posts Tagged With "{{ tag }}"</h2>
    <ProgramList v-if="tagPrograms.length > 0" :programs="tagPrograms" />
    <p v-else>No posts found for this tag</p>
  </section>
</template>

<style scoped>
  h2 {
    color: orange;
  }
</style>