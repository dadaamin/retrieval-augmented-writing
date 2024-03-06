<template>
  <Listbox
    multiple
    filter
    v-model="selectedFiles"
    :options="files"
    optionLabel="filename"
    optionValue="id"
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

<script setup>
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
    files.value = response.data;
    // Process your data here
  } catch (error) {
    console.error("API call failed:", error);
  }
}

onMounted(() => {
  fetchData();
});
</script>
