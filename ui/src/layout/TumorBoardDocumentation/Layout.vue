<template>
    <!-- <div class="w-full gap-3 flex align-items-stretch"> -->
    <!-- <FileView class="w-2 border-200" /> -->
    <Splitter
        class="w-full border-none bg-none"
        style="background: transparent"
    >
        <SplitterPanel
            :size="20"
            :min-size="10"
            class="flex align-items-stretch"
        >
            <FileView
                :patient-id="patientId"
                class="w-full border-200"
            ></FileView>
        </SplitterPanel>
        <SplitterPanel
            style="margin-left: 1rem"
            :size="80"
            :min-size="20"
            :unstyled="false"
        >
            <Splitter class="gap-2" style="background: transparent">
                <SplitterPanel class="flex">
                    <FileIndexing :patient-id="patientId"></FileIndexing>
                </SplitterPanel>
                <SplitterPanel>
                    <Documentation></Documentation>
                </SplitterPanel>
            </Splitter>
        </SplitterPanel>
    </Splitter>
    <!-- </div> -->
</template>

<script setup>
import { ref } from "vue";
import FileView from "@/layout/TumorBoardDocumentation/FileView.vue";
import FileIndexing from "@/layout/TumorBoardDocumentation/FileIndexing.vue";
import Documentation from "@/layout/TumorBoardDocumentation/Documentation.vue";

// const props = defineProps(["patientId"]);
const patientId = ref(
    "Patient/70cd56ad887462a0bff46c879ea4dfb478b1035e07da61596ba75a526105aad3"
);
</script>
