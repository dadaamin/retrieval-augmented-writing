<template>
    <div class="file" @click="selectFile">
        <span class="filename">{{ file.name }}</span>
        <span class="creation-date">{{ file.creationDate }}</span>
    </div>
</template>

<script>
export default {
    props: {
        file: {
            type: Object,
            required: true,
        },
    },
    methods: {
        selectFile() {
            this.$emit("select", this.file);
        },
    },
};
</script>

<style scoped>
.file {
    cursor: pointer;
    padding: 5px 0; /* Example padding */
}

.file:not(.selected):hover {
    background-color: #e0e0e0; /* Light grey background on hover */
}

.selected {
    background-color: #007bff; /* Highlight color for selected files */
    color: white; /* White text for contrast */
}

.side-panel {
    width: 200px; /* Adjust the width as necessary */
    background-color: #f0f0f0; /* Light grey background */
    border-right: 1px solid #ddd; /* Border on the right */
    height: 100vh; /* Full viewport height */
    overflow-y: auto; /* Enable scrolling if content is too long */
}

.side-panel div {
    list-style: none; /* Remove default list styling */
    padding: 0; /* Remove default padding */
    margin: 0; /* Remove default margin */
}

.side-panel div {
    padding: 10px; /* Add some padding */
    cursor: pointer; /* Change cursor to indicate clickable items */
}

.file-header {
    font-weight: bold;
    text-decoration: underline;
}

.filename-header,
.date-header {
    display: inline-block;
    width: 50%; /* Adjust the width as necessary */
}

.file {
    cursor: pointer;
    padding: 5px 0; /* Example padding */
}

.side-panel {
    display: flex;
    flex-direction: column;
}

.file-header,
.file {
    display: flex;
    justify-content: space-between;
    padding: 5px;
}

.filename-header,
.filename {
    flex: 1;
}

.date-header,
.creation-date {
    flex: 1;
    text-align: right;
}
</style>
