<script setup>
import AuthorLink from "./AuthorLink.vue";
import { RouterLink } from "vue-router";

const props = defineProps({
  programs: {
    type: Array,
    required: true,
  },
  showAuthor: {
    type: Boolean,
    required: false,
    default: true,
  },
});
</script>

<template>
  <ol class="program-list">
    <li class="program" v-for="program in programs" :key="program.slug">
      <RouterLink :to="{ name: 'program', params: { slug: program.slug } }">
        {{ program.title }}
      </RouterLink>
      <span v-if="showAuthor"> by <AuthorLink :author="program.author" /> </span>
    </li>
  </ol>
</template>