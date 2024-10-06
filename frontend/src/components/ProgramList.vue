<script setup>
import AuthorLink from "./AuthorLink.vue";
import { defineProps, ref } from "vue";
import ProgramDaysBoxes from "./ProgramDaysBoxes.vue";
import { useMutation } from "@vue/apollo-composable";
import { ASSIGN_PROGRAM } from "@/mutations";

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
  allowAssignment: {
    type: Boolean,
    required: false,
    default: true,
  },
});

const collapsedPrograms = ref([]);
function formatDate(originalDate) {
    // Create a Date object from the input string
    const date = new Date(originalDate);

    // Check if the date is valid
    if (isNaN(date.getTime())) {
        throw new Error('Invalid date format');
    }

    // Get day, month and year
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
    const year = date.getFullYear();

    // Return formatted date
    return `${month}/${day}/${year}`;
}

function isCollapsed(slug) {
    return collapsedPrograms.value.includes(slug);
};

function toggleCollapse(slug, id) {
    if (isCollapsed(slug)) {
        collapsedPrograms.value = collapsedPrograms.value.filter(s => s !== slug);

    } else {
        collapsedPrograms.value.push(slug);
    }
};


const assignToAthlete = async (program_id, athlete) => {
  try {
    const response = await assignProgramMutation.mutate({
      programId: program_id,
      athleteUsername: athlete
    });
    console.log(response);
  } catch (error) {
    console.error(error);
  }
}

const assignProgramMutation = useMutation(ASSIGN_PROGRAM, {
  variables(){
    return {
      programId: '',
      athleteUsername: ''
    }
  }
})
</script>

<template>
  <div>
    <div v-for="program in props.programs" :key="program.slug" class="program">
      <div class="program-row">
        <div class="program-title">
          {{ program.title }}
        </div>
        <div class="program-tags">
          {{ program.tags.map(tag => tag.name).join(', ') }}
        </div>

        <button v-show="allowAssignment" @click="assignToAthlete(program.id, 'athlete1')">Assign Program</button>
        <div class="program-date">
          {{ formatDate(program.dateCreated) }}
        </div>

        <button @click="toggleCollapse(program.slug, program.id)">
          {{ !isCollapsed(program.slug) ? 'Show Details' : 'Hide Details' }}
        </button>

        <div v-if="showAuthor" class="program-author">
          <AuthorLink :author="program.author" />
        </div>
      </div>
      <div v-if="isCollapsed(program.slug)" class="program-details">
        <ProgramDaysBoxes :program_id="program.id"/>
        Notes: {{ program.body }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.program-row {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  cursor: pointer;
}

.program-details {
  padding: 10px;
}

.program{
  border: 1px solid #ccc;
  padding: 10px;
  margin: 10px;
  border-radius: 5px;
  background-color: rgb(238, 236, 236);
}

.program-title{  
  font-weight: bold; 
}

</style>