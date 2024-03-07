<template>
    <BlockUI
        :blocked="!isActive"
        :unstyled="false"
        @click="toggleBlock"
        class="invisible-block-ui"
    >
        <InputGroup class="p-2">
            <Button
                :label="label"
                style="min-width: 10rem; max-width: 15rem"
                :severity="isActive ? 'primary' : 'secondary'"
                @click="emit('selectField')"
            />
            <InputText
                v-if="type == 'text'"
                v-model="fieldValue"
                type="text"
                @input="invalidateField"
            />
            <Button
                :severity="isAccepted ? 'success' : 'secondary'"
                icon="pi pi-check-circle"
                @click="acceptField"
            />
        </InputGroup>
    </BlockUI>
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
    console.log("test");
}

function invalidateField() {
    isAccepted.value = false;
}

function acceptField() {
    isAccepted.value = true;
}
</script>

<style>
.invisible-block-ui .p-blockui {
    background: transparent !important;
}
</style>
