<template>
    <InputGroup class="p-2">
        <Button
            :label="label"
            style="min-width: 10rem; max-width: 15rem"
            :severity="isActive ? 'primary' : 'secondary'"
            @click="toggleBlock"
        />
        <InputText
            :disabled="!isActive"
            v-if="type == 'text'"
            v-model="fieldValue"
            type="text"
            @input="invalidateField"
        />
        <Button
            :disabled="!isActive"
            :severity="isAccepted ? 'success' : 'secondary'"
            icon="pi pi-check-circle"
            @click="acceptField"
        />
    </InputGroup>
</template>

<script setup lang="ts">
import { ref, defineEmits } from "vue";
const fieldValue = ref("");
const isAccepted = ref(false);
const isActive = ref(false);

const name = "DocumentationField";

export interface Props {
    label: string;
    type?: string;
    index?: number;
}

const props = withDefaults(defineProps<Props>(), {
    type: "text",
    isActive: false,
    index: 0,
});

// Define the `selectField` event this component can emit
const emit = defineEmits(["selectField"]);

function toggleBlock() {
    isActive.value = true;
    emit("selectField", { index: props.index });
}

function invalidateField() {
    isAccepted.value = false;
}

function acceptField() {
    isAccepted.value = true;
}
</script>

<style lang="scss" scoped>
.invisible-block-ui .p-blockui {
    background: transparent !important;
}
</style>
