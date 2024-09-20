<script setup>
import { ref } from 'vue';
import { useQuery, useMutation } from "@vue/apollo-composable";
import gql from "graphql-tag";

const title = ref('');
const body = ref('');

const CREATE_PROGRAM = gql`
  mutation CreateProgram($title: String!, $body: String!, $slug: String!) {
    createProgram(title: $title, body: $body, slug: $slug) {
      program {
        id
        title
        body
        slug
      }
    }
  }
`;

const createProgram = useMutation(CREATE_PROGRAM, {
  variables() {
    return {
      title: title.value,
      body: body.value,
      slug: title.value.toLowerCase().replace(/\s+/g, '-')
    };
  }
});

const addProgram = async () => {
  try {
    const response = await createProgram.mutate({
      title: title.value,
      body: body.value,
      slug: title.value.toLowerCase().replace(/\s+/g, '-'),
      author: getCurrentUser() // Get the current user
    });
    title.value = '';
    body.value = '';
  } catch (error) {
    console.error(error);
  }
  console.log(response);
};

</script>

<template>

  <div>
    <h2>Write a Program</h2>
    <form @submit.prevent="addProgram">
      <label for="title">Title</label>
      <input type="text" id="title" v-model="title" />
      <label for="body">Body</label>
      <textarea id="body" v-model="body"></textarea>
      <button type="submit">Submit</button>
    </form>
  </div>
  
</template>