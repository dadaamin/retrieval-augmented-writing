<template>
  <Listbox
    v-model="selectedFiles"
    multiple
    filter
    :options="files"
    option-label="filename"
    option-value="id"
  >
    <template #option="opt">
      <div class="flex align-items-end">
        <div class="flex-grow-1">{{ opt.option.filename }}</div>
        <div class="text-xs text-500">
          {{ timeFilter(opt.option.created_at) }}
        </div>
      </div>
    </template></Listbox
  >
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import ApiService from "@/services/ApiService.ts";
import moment from "moment";

const files = ref([]);
const selectedFiles = ref([]);

function timeFilter(date) {
  return moment(date).format("DD.MM.YYYY");
}

const props = defineProps(["patientId"]);

async function fetchData() {
  try {
    const response = await ApiService.getDocuments(props.patientId);
    files.value = await response.json();
  } catch (error) {
    console.error("API call failed:", error);
  }
}

onMounted(() => {
  fetchData();
});
</script>
