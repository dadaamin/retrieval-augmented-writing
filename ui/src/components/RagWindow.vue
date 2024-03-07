<template>
    <div class="rag-window">
        <RagResultsComponent></RagResultsComponent>
        <RagQueryComponent></RagQueryComponent>
    </div>
</template>

<script>
import RagResultsComponent from "./RagResultsComponent.vue";
import RagQueryComponent from "./RagQueryComponent.vue";

export default {
    name: "RagWindowComponent",
    components: {
        RagResultsComponent,
        RagQueryComponent,
    },
};
</script>

<style>
/* Assuming you want both to equally fill the vertical space */
.rag-window,
.html-form {
    flex: 1;
    overflow: auto; /* If you want internal scrolling */
    display: flex;
    flex-direction: column;
}
</style>
