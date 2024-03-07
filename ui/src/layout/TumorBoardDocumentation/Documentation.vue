<template>
    <div class="w-full h-full p-2 border-1 border-200 border-round bg-white">
        <DocumentationField label="Name"></DocumentationField>
        <DocumentationField label="Diagnose"></DocumentationField>
        <DocumentationField
            label="Diagnose nach der Nachbehandlung"
        ></DocumentationField>
    </div>
</template>

<script setup>
import DocumentationField from "@/layout/TumorBoardDocumentation/DocumentationField.vue";
</script>
