<script setup> 
import { ref, computed, watch } from 'vue';

const props = defineProps({
  items: {
    type: Object,
    required: true,
  },
  selectedItem: {
    type: Object,
    required: false,
  }
});

const emit = defineEmits(['update:selectedItem']);

const search = ref(props.selectedItem ? props.selectedItem.name : '');
const showList = ref(false);
const keepOpen = ref(false);

const filteredItems = computed(() => {
  return props.items.filter(i => 
  {return i.name.toLowerCase().indexOf(search.value.toLowerCase()) != -1});
});

watch(keepOpen, (newVal, oldVal) => {
  if (newVal) {
    showList.value = true;
  }
  else {
    showList.value = false;
  }
});

const selectItem = (item) => {
  search.value = item.name;
  keepOpen.value = false;
  emit('update:selectedItem', item);
};

</script>

<template>
  <input type="text" 
         v-model="search" 
         style="width: 150px;"  
         @click="keepOpen = true"
        />

  <ul v-if="showList" class="search-list">
    <li class="item" 
        v-for="item in filteredItems" 
        :key="item.name" 
        @click="selectItem(item)">
      {{ item.name }}
    </li>
  </ul>
</template>



<style scoped>
  .search-list{
    list-style-type: none;
    padding: 0;
    width: 150px;
  }
  .item{
    cursor: pointer;
  }
  .item:hover{
    background-color: lightgray;
  }

  input{
    width: 150px;
  }
</style>