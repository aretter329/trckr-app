<script setup>
import AuthorLink from "./AuthorLink.vue";
import { RouterLink } from "vue-router";
import { defineProps, ref } from "vue";
import ProgramDaysBoxes from "./ProgramDaysBoxes.vue";

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

const days = {
  0: {
    name: "Day 1",
    //workouts will be based on type? 
    workouts: [
      {
        title: "Workout 1",
        type: {
          color: "--atomic-tangerine",
          name: "Lift",
        },
        exercises: [
          {
            title: "Squats",
            sets: 3,
            reps: 10,
          },
          {
            title: "Bench Press",
            sets: 3,
            reps: 10,
          },
        ],
      },
      {
        title: "Workout 2",
        type: {
          color: "--uranian-blue",
          name: "Plyos",
        },
        exercises: [
          {
            title: "Jump Squats",
            sets: 3,
            reps: 10,
          },
          {
            title: "Box Jumps",
            sets: 3,
            reps: 10,
          },
        ],
      },
    ],
  },
  1: {name: "Day 2",
    workouts: [
      {
        title: "Workout 1",
        type: {
          color: "--atomic-tangerine",
          name: "Lift",
        },
        exercises: [
          {
            title: "Squats",
            sets: 3,
            reps: 10,
          },
          {
            title: "Bench Press",
            sets: 3,
            reps: 10,
          },
        ],
      },
      {
        title: "Workout 2",
        type: {
          color: "--uranian-blue",
          name: "Plyos",
        },
        exercises: [
          {
            title: "Jump Squats",
            sets: 3,
            reps: 10,
          },
          {
            title: "Box Jumps",
            sets: 3,
            reps: 10,
          },
        ],
      },
    ],
  },
};


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

function toggleCollapse(slug) {
    if (isCollapsed(slug)) {
        collapsedPrograms.value = collapsedPrograms.value.filter(s => s !== slug);
    } else {
        collapsedPrograms.value.push(slug);
    }
};

</script>

<template>
  <div>
    <div v-for="program in props.programs" :key="program.slug" class="program">
      <div class="program-row" @click="toggleCollapse(program.slug)">
        <div class="program-title">
          {{ program.title }}
        </div>
        <div class="program-tags">
          {{ program.tags.map(tag => tag.name).join(', ') }}
        </div>
        <div class="program-date">
          {{ formatDate(program.dateCreated) }}
        </div>
        <div v-if="showAuthor" class="program-author">
          <AuthorLink :author="program.author" />
        </div>
      </div>
      <div v-if="isCollapsed(program.slug)" class="program-details">
        <ProgramDaysBoxes :days="days" />
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