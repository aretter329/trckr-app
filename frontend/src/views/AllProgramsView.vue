<script setup>
import ProgramList from "../components/ProgramList.vue";
import { useQuery, useMutation } from "@vue/apollo-composable";
import gql from "graphql-tag";
import { ref } from 'vue';
import WriteProgram from "@/components/WriteProgram.vue";
import { useUserStore } from "@/store/user";

const tagName = ref('');
const message = ref('');
const writeProgram = ref(false);
const userStore = useUserStore();
const username = userStore.getUser.username;

const { result, loading, error } = useQuery(gql` 
  query{
    programsByAuthor(username: "${username}") {
      title
      slug
      dateCreated
      notes
      id
      tags {
        name
      }
      author {
        username
        firstName
        lastName
      }
  }
  }`,
  {
    variables() {
      return {
        username: username
      };
    }
  }
);

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
  <div class="container">
  <h2>Your Programs</h2><div style="width: 100%;">
  <button @click="writeProgram = !writeProgram">Write a Program</button>
  <div v-show="writeProgram">
    <WriteProgram/>
  </div>
  <div v-if="loading">Loading...</div>
  <div v-else-if="error" class="warn">{{ error }}</div>
  
  <ProgramList v-else 
      :programs="result.programsByAuthor" 
      :showAuthor="false"/>
    </div>
  
  
   
    <!--
    <div>
      <input v-model="tagName" placeholder="Enter tag name" />
      <button @click="addTag">Add Tag</button>
      <p v-if="message">{{ message }}</p>
    </div>
    -->

  

</div>
</template>

<style scoped>

  .container{
    display: flex; 
    flex-direction: column; 
    align-items: center;
  }
</style>