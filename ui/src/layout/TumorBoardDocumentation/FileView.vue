<template>
    <Listbox
        v-model="selectedFiles"
        multiple
        filter
        :options="files"
        option-label="id"
        option-value="document_id"
        :virtual-scroller-options="{ itemSize: 38 }"
        list-style="height:100%"
    >
        <template #option="opt">
            <div class="flex align-items-end">
                <div class="flex-grow-1">{{ opt.option.resource_type }}</div>
                <div class="text-xs text-500">
                    {{ timeFilter(opt.option.last_updated) }}
                </div>
            </div>
        </template></Listbox
    >
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import ApiService from "@/services/ApiService";
import moment from "moment";

const files = ref([]);
const selectedFiles = ref([]);

function timeFilter(date: string) {
    return moment(date).format("DD.MM.YYYY");
}

const props = defineProps(["patientId"]);

async function fetchData() {
    try {
        const response = await ApiService.getDocuments(props.patientId);
        const documents = await response.json();
        documents.sort(
            (a: { last_updated: string }, b: { last_updated: string }) =>
                new Date(b.last_updated).getTime() -
                new Date(a.last_updated).getTime()
        );
        files.value = documents;
    } catch (error) {
        console.error("API call failed:", error);
    }
}

onMounted(() => {
    fetchData();
});
</script>
