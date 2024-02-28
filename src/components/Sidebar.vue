<template>
  <div :class="{ 'sidebar-closed': !isOpen, 'sidebar-open': isOpen }">
    <button @click="toggleSidebar">☰</button>
    <ul v-if="isOpen">
      <li v-for="(document, index) in documents" :key="index">
        {{ document.title }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "SidebarComponent",
  data() {
    return {
      isOpen: false,
      documents: [
        { title: "Document 1" },
        { title: "Document 2" },
        // Add more documents as needed
      ],
    };
  },
  methods: {
    toggleSidebar() {
      this.isOpen = !this.isOpen;
    },
  },
};
</script>

<style>
.sidebar-open {
  /* Add your open sidebar styles */
  border-right: 1px solid #ccc; /* Example if you want a border on the right when open */
}

.sidebar-closed {
  /* Styles for when the sidebar is closed */
}
</style>
