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

const { result, refetch: refetchAthletes, error } = useQuery(gql` 
  query{
    allAthletesByCoach(coachUsername: "${userStore.getUser.username}") {
      id
      username
      firstName
      lastName
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

const { result: groups, refetch: refetchGroups } = useQuery(gql` 
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
        firstName
        lastName
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
  refetchAthletes();
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
  showGroupOptions.value[athleteId] = false;
  refetchGroups();
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
  refetchGroups();

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
  <div class="main-content">
    <div class="sub-section"> 
      <h2>Event Groups</h2>
      <div>
        <input type="text" v-model="newGroupName" placeholder="New group name">
        <button class="simple-button" @click="createNewGroup">Create Group</button>
      </div>
      <div style="width: 100%" v-if="result && result.allAthletesByCoach && groups && groups.groupsByCoach">
        <div class='event-group' v-for="group in groups.groupsByCoach" :key="group.id">
        <h3>{{ group.name }}</h3>
        <ul>
          <li v-for="athlete in group.athletes" :key="athlete.id">
            {{ athlete.firstName && athlete.lastName ? athlete.firstName + ' ' + athlete.lastName : athlete.username }} 
          </li>
        </ul>

        </div>
      </div>
    </div>
  
    <div class="sub-section" v-if="result && result.allAthletesByCoach && groups && groups.groupsByCoach">
      <h2> All athletes </h2>
      <div>
        <input type="text" v-model="athleteUsername" placeholder="Athlete username">
        <button class='simple-button' @click="addAthlete">Add Athlete</button>
      </div>
      <div v-for="athlete in result.allAthletesByCoach" :key="athlete.id">
        <RouterLink :to="{ name: 'athlete', params: { athleteUsername: athlete.username } }">
          {{ athlete.firstName && athlete.lastName ? athlete.firstName + ' ' + athlete.lastName : athlete.username }}
        </RouterLink>
        <button style="margin-left:5px;" @click="showGroupOptions[athlete.id]=true">Add to group</button>
        
        <template v-if="showGroupOptions[athlete.id]">
          <select v-model="selectedGroup[athlete.id]">
            <option v-for="group in groups.groupsByCoach" :value="group.id">{{ group.name }}</option>
          </select>
          <button @click="confirmGroupSelection(athlete.id)">Confirm</button>
        </template>
      </div>
    </div>
</div>

</template>

<style scoped>

.main-content {
  display: flex;
  flex-direction: row;
  justify-content: center;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 5px;
}

li:last-child {
  border-bottom: none;
}

h3{
  border-bottom: 2px solid white; 
  text-align: center;
}

.sub-section{
  background: lightgray;
  border: 3px solid gray;  
  margin-left: 50px; 
  margin-right: 50px;
  padding: 0px 80px 0px 80px; 
  display: flex; 
  flex-direction: column;
  align-items: center; 
  border-radius: 10px;  
}

.simple-button{
  background-color: var(--midnight-blue);
  border: none; 
  color: white; 
}

input{ 
  height: 30px;
  border: 2px solid var(--midnight-blue); 
  border-radius: 5px;
}

.event-group{
  display: flex; 
  flex-direction: column;
  justify-content: flex-start;
  padding: 5px; 
  margin: 5px;
}


</style>