<script setup>
import ProgramList from "../components/ProgramList.vue";
import { useQuery, useMutation } from "@vue/apollo-composable";
import gql from "graphql-tag";
import { ref } from 'vue';
import WriteProgram from "@/components/WriteProgram.vue";

const { result, loading, error } = useQuery(gql`
  query {
    allPrograms {
      title
      slug
      author {
        username
        firstName
        lastName
      }
    }
  }
`);


const CREATE_TAG = gql`
  mutation CreateTag($name: String!){
    createTag(name: $name) {
      tag {
        id
        name
      }
    }
  }
`;

// Reactive state
const tagName = ref('');
const message = ref('');

// Use the mutation
const createTag = useMutation(CREATE_TAG, {
  variables() {
    return {
      name: tagName.value
    };
  }
});

// Function to add a tag
const addTag = async () => {
  console.log('tag name:', tagName.value)
  try {
    const response = await createTag.mutate({
      name: tagName.value // Pass the tag name as a variable
    });
    message.value = `Tag created: ${response.data.createTag.tag.name}`;
    tagName.value = ''; // Clear input after adding
  } catch (error) {
    message.value = `Error: ${error.message}`;
  }
};


</script>

<template>
  <!--
  <h2>Recent Programs</h2>
  <div v-if="loading">Loading...</div>
  <div v-else-if="error" class="warn">{{ error }}</div>
  <ProgramList v-else :programs="result.allPrograms" />
  
  
  
    <div>
      <input v-model="tagName" placeholder="Enter tag name" />
      <button @click="addTag">Add Tag</button>
      <p v-if="message">{{ message }}</p>
    </div>
  -->
<WriteProgram/>

</template>

<style scoped>
  h2 {
    color: blue;
  }
</style>