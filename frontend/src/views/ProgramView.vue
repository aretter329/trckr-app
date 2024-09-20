<script setup>
import AuthorLink from "../components/AuthorLink.vue";
import { useRoute } from "vue-router";
import { useQuery } from "@vue/apollo-composable";
import gql from "graphql-tag";

const dateFormatter = new Intl.DateTimeFormat("en-US", { dateStyle: "full" });
const displayableDate = (date) => dateFormatter.format(new Date(date));
const route = useRoute();
const slug = route.params.slug;
const { result, loading, error } = useQuery(gql`
  query {
    programsBySlug(
      slug: "${slug}"
    ) {
        title
        published
        slug
        body
        author {
          user {
            username
            firstName
            lastName
          }
        }
        tags {
          name
        }
    }
  }
`);
</script>

<template>
  <div v-if="loading">Loading...</div>
  <div v-else-if="error" class="warn">{{ error.message }}</div>
  <section v-else :set="program = result.programsBySlug">
    <h2>{{ program.title }}</h2>
    <aside>
      Written by <AuthorLink :author="program.author" />
      <h4>Tags</h4>
      <ul>
        <li v-for="tag in program.tags" :key="tag.name">
          <RouterLink :to="{ name: 'tag', params: { tag: tag.name } }">
            {{ tag.name }}
          </RouterLink>
        </li>
      </ul>
    </aside>
    <article>{{ program.body }}</article>
  </section>
</template>

