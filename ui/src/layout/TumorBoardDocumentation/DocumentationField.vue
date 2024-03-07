<template>
    <BlockUI :blocked="!isActive" :unstyled="false" @click="toggleBlock">
        <InputGroup class="p-2">
            <Button
                :label="label"
                style="min-width: 10rem; max-width: 15rem"
                :severity="isActive ? 'primary' : 'secondary'"
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
import { ref } from "vue";
const fieldValue = ref("");
const isAccepted = ref(false);
const isActive = ref(false);

export interface Props {
    label: string;
    type?: string;
}

const props = withDefaults(defineProps<Props>(), {
    type: "text",
    isActive: false,
});

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
.p-blockui {
    background: transparent !important;
}
</style>
