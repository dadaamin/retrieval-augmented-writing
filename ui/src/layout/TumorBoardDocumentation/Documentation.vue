<template>
    <div class="w-full h-full p-2 border-1 border-200 border-round bg-white">
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
