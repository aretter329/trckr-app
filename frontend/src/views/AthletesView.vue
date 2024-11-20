<script setup>
import { ref } from 'vue';
import { useQuery, useMutation } from "@vue/apollo-composable";
import { ADD_ATHLETE, CREATE_WORKOUT_GROUP, ADD_ATHLETE_TO_GROUP } from '@/mutations';
import { useUserStore } from "@/store/user";
import gql from 'graphql-tag';

const userStore = useUserStore();
const athleteUsername = ref('');
const showGroupOptions = ref({});
const selectedGroup = ref({});
const newGroupName = ref('');

const { result, loading, error } = useQuery(gql` 
  query{
    allAthletesByCoach(coachUsername: "${userStore.getUser.username}") {
      id
      username
      coach {
        id
        username
      }
  }
  }`,
  {
    variables() {
      return {
        coachUsername: userStore.getUser.username
      };
    }
  }
);

const { result: groups } = useQuery(gql` 
  query{
    groupsByCoach(coach: "${userStore.getUser.username}") {
      name
      id
      coach {
        username
      }
      athletes{
        id
        username
      }
  }
  }`,
  {
    variables() {
      return {
        coach: userStore.getUser.username
      };
    }
  }
);

const addAthlete = async () => {
  try{
    await addAthleteMutation.mutate(
      {
        athleteUsername: athleteUsername.value,
        coachUsername: userStore.getUser.username
      }
    );
  }
  catch (error) {
    console.error(error);
  }
  athleteUsername.value = '';

};

const addAthleteMutation = useMutation(ADD_ATHLETE, {
  variables() {
    return {
      athleteUsername: athleteUsername.value,
      coachUsername: userStore.getUser.username
    };
  }
});


const confirmGroupSelection = async (athleteId) => {
  showGroupOptions[athleteId] = false;
  console.log(athleteId, selectedGroup.value[athleteId]);

  try{
    await addAthleteToGroupMutation.mutate(
      {
        athleteId: athleteId,
        groupId: selectedGroup.value[athleteId]
      }
    );
  }
  catch (error) {
    console.error(error);
  }
};

const addAthleteToGroupMutation = useMutation(ADD_ATHLETE_TO_GROUP);

const createNewGroup = async () => {
  try{
    await createNewGroupMutation.mutate(
      {
        name: newGroupName.value,
        coach: userStore.getUser.username
      }
    );
  }
  catch (error) {
    console.error(error);
  }

};

const createNewGroupMutation = useMutation(CREATE_WORKOUT_GROUP, {
  variables() {
    return {
      name: newGroupName.value,
      coach: userStore.getUser.username
    };
  }
});









</script>

<template>
  <div class="centered-content">
  
  <div>
    <input type="text" v-model="athleteUsername" placeholder="Athlete username">
    <button @click="addAthlete">Add Athlete</button>
  </div>

  
  <h2>Groups and Members</h2>
  <div v-if="result && result.allAthletesByCoach && groups && groups.groupsByCoach">
    <div v-for="group in groups.groupsByCoach" :key="group.id">
    <h3>{{ group.name }}</h3>
    <ul>
      <li v-for="athlete in group.athletes" :key="athlete.id">
        {{ athlete.username }}
      </li>
    </ul>

    </div>
  </div>

  <div>
    <input type="text" v-model="newGroupName" placeholder="New group name">
    <button @click="createNewGroup">Create Group</button>
  </div>

  <h2> All atheltes </h2>

  <div v-if="result && result.allAthletesByCoach && groups && groups.groupsByCoach">
    <div v-for="athlete in result.allAthletesByCoach" :key="athlete.id">
      {{ athlete.username }}
      <button @click="showGroupOptions[athlete.id]=true">Add to group</button>
      <template v-if="showGroupOptions[athlete.id]">
        <select v-model="selectedGroup[athlete.id]">
          <option v-for="group in groups.groupsByCoach" :value="group.id">{{ group.name }}</option>
        </select>
        <button @click="confirmGroupSelection(athlete.id)">Confirm</button>
      </template>
    </div>
  </div>


  {{ selectedGroup }}
</div>

</template>