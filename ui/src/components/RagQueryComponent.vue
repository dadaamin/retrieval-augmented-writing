<template>
    <div class="rag-query-component">
        <div class="messages">
            <div
                v-for="(message, index) in messages"
                :key="index"
                class="message"
                :class="{ mine: message.mine }"
            >
                {{ message.text }}
            </div>
        </div>
        <div class="input-area">
            <input
                v-model="newMessage"
                type="text"
                @keyup.enter="sendMessage"
            />
            <button @click="sendMessage">Send</button>
        </div>
    </div>
</template>

<script>
export default {
    name: "RagQueryComponent",
    data() {
        return {
            newMessage: "",
            messages: [],
        };
    },
    methods: {
        sendMessage() {
            if (!this.newMessage.trim()) return;

            this.messages.push({ text: this.newMessage, mine: true });
            this.newMessage = ""; // Clear input after sending
        },
    },
};
</script>

<style scoped>
.rag-query-component {
    display: flex;
    flex-direction: column;
}

.messages {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
}

.message {
    margin: 5px;
    padding: 10px;
    background-color: #f0f0f0;
    border-radius: 10px;
}

.mine {
    align-self: flex-end;
    background-color: #dcf8c6;
}

.input-area {
    display: flex;
    padding: 10px;
}

.input-area input {
    flex: 1;
    margin-right: 10px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 20px;
}

.input-area button {
    padding: 10px 20px;
    border: none;
    border-radius: 20px;
    background-color: #4caf50;
    color: white;
    cursor: pointer;
}

.input-area button:hover {
    background-color: #45a049;
}
</style>
