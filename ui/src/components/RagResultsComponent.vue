<template>
    <div class="rag-results-component">
        <RagTextChunkComponent text="This is a rounded text box." />
        <RagTextChunkComponent
            text="Another example of a rounded text box with longer text. Vue.js makes creating reusable components like this quite straightforward and efficient."
        />
    </div>
</template>

<script>
import RagTextChunkComponent from "./RagTextChunkComponent.vue";

export default {
    name: "RagResulstComponent",
    components: {
        RagTextChunkComponent,
    },
};
</script>

<style>
.rag-results-component {
    flex: 1;
}
/* Add your styles here */
</style>
