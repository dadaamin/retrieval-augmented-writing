<template>
    <div class="rag-text-chunk">
        <p>{{ text }}</p>
    </div>
</template>

<script>
export default {
    name: "RagTextChunkComponent",
    props: {
        text: String,
    },
};
</script>

<style scoped>
.rag-text-chunk {
    background-color: #f2f2f2; /* Light grey background */
    border-radius: 25px; /* Rounded corners */
    padding: 20px; /* Padding inside the box */
    margin: 10px 0; /* Spacing between boxes */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Optional: adds a subtle shadow */
    max-width: 80%; /* Maximum width of the text box */
    word-wrap: break-word; /* Ensure long words do not overflow */
}

p {
    margin: 0; /* Remove default paragraph margin */
}
</style>
