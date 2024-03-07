<template>
    <slot>There are no document fields to display.</slot>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useSlots, useAttrs } from "vue";
import DocumentationField from "@/layout/TumorBoardDocumentation/DocumentationField.vue";

const slotContent = ref(null);
const slots = useSlots();

onMounted(() => {
    slotContent.value = slots.default ? slots.default() : [];
    // Now slotContent.value contains the VNodes of your slot content
    // Note: Direct manipulation or iteration over these VNodes for dynamic rendering purposes is not typical Vue practice
});

function test() {
    slotContent.value.forEach((vnode, index) => {
        // This is a highly theoretical example; actual structure might vary
        if (vnode.type === DocumentationField) {
            vnode.props.index = index;
            console.log(vnode);
            console.log("DocumentationField label:", vnode.props.index);
        }
    });
}
</script>
