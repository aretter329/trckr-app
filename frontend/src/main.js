import './assets/main.css'
import { createApp, provide, h } from "vue";
import App from './App.vue'
//import { useAuthStore } from "./store/auth";
import router from './router'
import {
  ApolloClient,
  createHttpLink,
  InMemoryCache,
} from "@apollo/client/core";
import { DefaultApolloClient } from "@vue/apollo-composable";
import { createPinia } from 'pinia'
import { library } from "@fortawesome/fontawesome-svg-core";
import { faTrash, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { setupCalendar, Calendar, DatePicker } from 'v-calendar';
import 'v-calendar/style.css';

library.add(faTrash);
library.add(faPlus);


const httpLink = createHttpLink({
  uri: "http://localhost:8000/graphql/",
});

const cache = new InMemoryCache();

const apolloClient = new ApolloClient({
  link: httpLink,
  cache: cache,
});

//this is the alternative way to set this up from 
//https://www.thedevspace.io/community/django-vue
//import { apolloClient } from "@/apollo-config";
//createApp(App).use(router).use(apolloClient).mount("#app");

const app = createApp({
  setup() {
    provide(DefaultApolloClient, apolloClient);
  },

  render: () => h(App),
}).component("font-awesome-icon", FontAwesomeIcon);


//createApp(App).use(createPinia()).use(router).use(apolloProvider)
// ^^ not sure why this one uses 'apollo provider' isntead 
app.use(createPinia());
app.use(router)
app.use(setupCalendar, {});


//const authStore = useAuthStore();
//authStore.setCsrfToken();

app.mount('#app')

app.component('VCalendar', Calendar)
app.component('VDatePicker', DatePicker)
