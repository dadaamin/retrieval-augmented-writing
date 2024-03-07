<template>
    <div
        class="w-full h-full p-2 p-splitter border-1 border-200 flex flex-column"
    >
        <DocumentationFieldGroup>
            <DocumentationField label="Name" />
            <DocumentationField label="Diagnose" />
            <DocumentationField label="Diagnose nach der Nachbehandlung" />
        </DocumentationFieldGroup>
    </div>
</template>

<script setup>
import DocumentationField from "@/layout/TumorBoardDocumentation/DocumentationField.vue";
import DocumentationFieldGroup from "@/layout/TumorBoardDocumentation/DocumentationFieldGroup.vue";
</script>
