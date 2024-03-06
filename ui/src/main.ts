import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import PrimeVue from "primevue/config";
import Button from "primevue/button";

import "@/assets/styles.scss";

const app = createApp(App);
app.use(PrimeVue);
app.use(store);
app.use(router);

app.component("Button", Button);

app.mount("#app");
