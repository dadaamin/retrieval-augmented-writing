<script setup>
import { useLayout } from "@/layout/composables/layout";
import { computed } from "vue";

const { layoutConfig } = useLayout();

const logoUrl = computed(() => {
  return "https://www.ikim.uk-essen.de/img/Logo-engl-IKIM.png";
  // return `layout/images/${
  //   layoutConfig.darkTheme.value ? "logo-white" : "logo-dark"
  // }.svg`;
});
</script>

<template>
  <div class="layout-footer">
    <img :src="logoUrl" alt="Logo" height="50" class="mr-2" />
  </div>
</template>
<style lang="scss" scoped></style>
