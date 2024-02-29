<template>
  <div id="app">
    <HeaderComponent :title="'Patient XYZ'" />
    <div class="content">
      <SidebarComponent />
      <div class="main-content">
        <RagWindowComponent />
        <WritingWindowComponent />
      </div>
    </div>
  </div>
</template>

<script>
import HeaderComponent from "./components/Header.vue";
import SidebarComponent from "./components/Sidebar.vue";
import RagWindowComponent from "./components/RagWindow.vue";
import WritingWindowComponent from "./components/WritingWindow.vue";

export default {
  name: "App",
  components: {
    HeaderComponent,
    SidebarComponent,
    RagWindowComponent,
    WritingWindowComponent,
  },
};
</script>

<style>
#app {
  min-height: 100vh; /* Make the app fill the full viewport height */
  display: flex;
  flex-direction: column;
}

html,
body {
  margin: 0;
  padding: 0;
}

.content {
  display: flex;
  flex: 1; /* Make content stretch to fill available space */
  border-top: 1px solid #ccc; /* Border between header and content */
}

.sidebar-component,
.main-content {
  border-right: 1px solid #ccc; /* Border between sidebar and main content */
}

.main-content {
  display: flex;
  justify-content: space-between;
  flex: 1; /* Stretch main content to fill available space */
}

.main-content > * {
  border-left: 1px solid #ccc; /* Border between chat window and form */
  flex: 1; /* Make each child (chat and form) take equal space */
}
</style>
