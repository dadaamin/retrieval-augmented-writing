import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import PrimeVue from "primevue/config";
import Splitter from "primevue/splitter";
import SplitterPanel from "primevue/splitterpanel";
import ScrollPanel from "primevue/scrollpanel";
import Panel from "primevue/panel";
import Toolbar from "primevue/toolbar";
import Card from "primevue/card";
import Listbox from "primevue/listbox";
import BlockUI from "primevue/blockui";
import Toast from "primevue/toast";
import InputText from "primevue/inputtext";
import Button from "primevue/button";
import Fieldset from "primevue/fieldset";
import Avatar from "primevue/avatar";
import InputGroup from "primevue/inputgroup";
import InputGroupAddon from "primevue/inputgroupaddon";
import ColorPicker from "primevue/colorpicker";

import DraggableDirective from "@/directives/DraggableDirective";
import DroppableDirective from "@/directives/DroppableDirective";

import "@/assets/styles.scss";

const app = createApp(App);
app.use(PrimeVue);
app.use(store);
app.use(router);

// Register Components
app.component("Splitter", Splitter);
app.component("SplitterPanel", SplitterPanel);
app.component("ScrollPanel", ScrollPanel);
app.component("Panel", Panel);
app.component("Toolbar", Toolbar);
app.component("Card", Card);
app.component("Listbox", Listbox);
app.component("BlockUI", BlockUI);
app.component("Toast", Toast);
app.component("InputText", InputText);
app.component("Button", Button);
app.component("Fieldset", Fieldset);
app.component("Avatar", Avatar);
app.component("InputGroup", InputGroup);
app.component("InputGroupAddon", InputGroupAddon);
app.component("ColorPicker", ColorPicker);

// Register directives
app.directive("draggable", DraggableDirective);
app.directive("droppable", DroppableDirective);

app.mount("#app");
