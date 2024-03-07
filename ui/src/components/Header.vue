<template>
    <header>
        <h1>{{ title }}</h1>
    </header>
</template>

<script>
export default {
    name: "HeaderComponent",
    props: {
        title: {
            type: String,
            default: "Default Title", // Provide a default title
        },
    },
};
</script>

<style>
/* Add your styles here */
</style>
