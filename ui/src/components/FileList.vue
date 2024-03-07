<template>
    <div class="side-panel">
        <div class="file-header">
            <span class="filename-header">Filename</span>
            <span class="date-header">Creation Date</span>
        </div>
        <FileItem
            v-for="file in files"
            :key="file.name"
            :file="file"
            :class="{
                selected: selectedFile && selectedFile.name === file.name,
            }"
            @select="selectFile"
        />
    </div>
</template>

<script>
import FileItem from "./FileItem.vue";
export default {
    components: {
        FileItem,
    },
    data() {
        return {
            selectedFile: null,
            files: [
                { name: "File1.txt", creationDate: "2024-02-28" },
                { name: "File2.txt", creationDate: "2024-02-27" },
                { name: "File3.txt", creationDate: "2024-02-26" },
                { name: "File4.txt", creationDate: "2024-02-25" },
            ],
        };
    },
    methods: {
        selectFile(file) {
            this.selectedFile = file;
        },
    },
};
</script>

<style>
.side-panel {
    width: 200px;
    /* Adjust the width as necessary */
    background-color: #f0f0f0;
    /* Light grey background */
    border-right: 1px solid #ddd;
    /* Border on the right */
    height: 100vh;
    /* Full viewport height */
    overflow-y: auto;
    /* Enable scrolling if content is too long */
}

.file-header {
    font-weight: bold;
    text-decoration: underline;
    display: flex;
    justify-content: space-between;
    padding: 5px;
}

.filename-header,
.date-header {
    display: inline-block;
    width: 50%;
    /* Adjust the width as necessary */
}
</style>
