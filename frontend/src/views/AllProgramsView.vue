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
const is_coach = userStore.getUser.isCoach; 

const { result: authoredPrograms, loading, error } = useQuery(gql` 
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
    <div style="width: 80%; display: flex; flex-direction: column; align-items: center;">
      <div v-show="writeProgram" style="width: 100%">
        <WriteProgram/>
       </div>

      <div v-if="is_coach" class="list-div">
        <button @click="writeProgram = !writeProgram">Write a Program</button>
        <div v-if="loading">Loading...</div>
        <div v-else-if="error" class="warn">{{ error }}</div>
        <div v-else-if="authoredPrograms" style="width: 100%">
        <ProgramList 
          :programs="authoredPrograms.programsByAuthor" 
          :showAuthor="false"
          :allowAssignment="true"/>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

  .container{
    display: flex; 
    flex-direction: column; 
    align-items: center;
  }

  .list-div{ 
    width: 100%;
    display: flex; 
    flex-direction: column;
    align-items: center;
  }
</style>