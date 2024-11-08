<script setup>
import ProgramList from "../components/ProgramList.vue";
import { useQuery, useMutation } from "@vue/apollo-composable";
import gql from "graphql-tag";
import { ref } from 'vue';
import WriteProgram from "@/components/WriteProgram.vue";
import { useUserStore } from "@/store/user";
import LoggedWorkouts from "../components/LoggedWorkouts.vue";

const tagName = ref('');
const message = ref('');
const writeProgram = ref(false);
const userStore = useUserStore();
const username = userStore.getUser.username;

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

const { result: assignedPrograms, loading1, error1 } = useQuery(gql` 
  query{
    programsByAthlete(athleteUsername: "${username}") {
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
        athleteUsername: username
      };
    }
  }
);

const { result: loggedWorkouts, loading2, error2 } = useQuery(gql` 
  query{
    loggedWorkoutsByAthlete(athleteUsername: "${username}") {
      athlete{
      username
      }
      date
      assignedDate
      notes
      id
      workout{
        id 
        type
        orderInDay
        blocks{
          id
          name
          orderInWorkout
          exercises{
            id
            name
            description 
            orderInBlock
            sets{
              id
              reps
              weight
              number
            }
          }
        }
      }
    }
  }`,
  {
    variables() {
      return {
        athleteUsername: username
      };
    }
  }
);




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
      <button @click="writeProgram = !writeProgram">Write a Program</button>
      <div v-show="writeProgram" style="width: 100%">
        <WriteProgram/>
      </div>
      
      <h2> Your Programs </h2>
      <div v-if="loading">Loading...</div>
      <div v-else-if="error" class="warn">{{ error }}</div>
      <div v-else-if="authoredPrograms" style="width: 100%">
      <ProgramList 
        :programs="authoredPrograms.programsByAuthor" 
        :showAuthor="false"
        :allowAssignment="true"/>
      </div>

      <h2> Assigned to you </h2>
      <div v-if="loading1">Loading...</div>
      <div v-else-if="error1" class="warn">{{ error }}</div>
      <div v-else-if="assignedPrograms" style="width: 100%">
      <ProgramList 
        :programs="assignedPrograms.programsByAthlete" 
        :showAuthor="false"
        :allowAssignment="false"/>
      </div>

      <div v-if="loggedWorkouts" style="width: 100%">
      <LoggedWorkouts 
        :loggedWorkouts="loggedWorkouts.loggedWorkoutsByAthlete"
      />
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
</style>