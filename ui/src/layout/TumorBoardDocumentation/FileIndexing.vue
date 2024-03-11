<template>
    <Splitter class="h-full border-1 border-200" layout="vertical">
        <SplitterPanel class="flex flex-column p-2 h-6">
            <ScrollPanel class="h-full">
                <TabView v-if="chunks.length > 0">
                    <TabPanel
                        v-for="(chunk, index) in chunks"
                        :key="index"
                        :header="`Ergebnis ${index + 1}`"
                    >
                        <p
                            class="text-sm text-light"
                            style="white-space: pre-wrap"
                        >
                            {{ chunk.text }}
                        </p>
                    </TabPanel>
                </TabView>
            </ScrollPanel>
        </SplitterPanel>
        <SplitterPanel class="flex flex-column gap-1 p-2 h-6">
            <ScrollPanel class="flex-grow-1 h-full">
                <div class="h-full flex flex-column gap-2">
                    <template v-if="chatHistory">
                        <template
                            v-for="(item, index) in chatMessages"
                            :key="index"
                        >
                            <div
                                v-if="index % 2 == 0"
                                class="border-200 border-1 border-round h-2 p-3 flex-grow-0 flex-column w-9 align-self-end"
                            >
                                <span class="text-xs text-300 font-bold"
                                    >User</span
                                >
                                <p>{{ item.content }}</p>
                            </div>
                            <div
                                v-if="index % 2 == 1"
                                class="border-200 border-1 border-round h-2 p-3 flex-grow-0 w-9 align-self-start"
                            >
                                <span class="text-xs text-300 font-bold"
                                    >Mixtral</span
                                >
                                <p>{{ item.content }}</p>
                            </div></template
                        >
                    </template>
                    <div
                        v-if="isProcessingQuery"
                        class="border-200 border-1 border-round h-2 p-3 flex-grow-0 w-9 align-self-start"
                    >
                        <span class="text-xs text-300 font-bold">Mixtral</span>
                        <ProgressBar
                            v-if="!isGeneratingResponse"
                            mode="indeterminate"
                            style="height: 6px"
                        ></ProgressBar>
                        <p>{{ queryResponse }}</p>
                    </div>
                </div>
            </ScrollPanel>
            <div class="flex gap-1">
                <InputText
                    v-model="query"
                    class="flex-grow-1"
                    type="text"
                    @keyup.enter="sendQuery"
                ></InputText>
                <BlockUI :blocked="canSendQuery ? false : true">
                    <Button
                        label="Send"
                        icon="pi pi-send"
                        @click="sendQuery"
                    ></Button>
                </BlockUI>
            </div>
        </SplitterPanel>
    </Splitter>
</template>

<script setup>
import { ref, computed } from "vue";
import ApiService from "@/services/ApiService.ts";
import ChatRequestBuilder from "@/services/types/ChatRequest.ts";
import ScrollPanel from "primevue/scrollpanel";
import TabView from "primevue/tabview";
import TabPanel from "primevue/tabpanel";

const chunks = ref([]);
const query = ref("Wie ist die Diagnose?");
const queryResponse = ref("");
const chatHistory = ref(null);
const isProcessingQuery = ref(false);
const isGeneratingResponse = ref(false);

const props = defineProps(["patientId"]);

async function readStream(reader) {
    let { done, value } = await reader.read();
    while (!done) {
        const response = new TextDecoder().decode(value).trim();
        // When streaming, sometimes more than one response is received at a time. Individual responses are separated by newlines.
        const messages = response.split("\n");
        messages.forEach((message) => {
            const data = JSON.parse(message);
            if (data.source_nodes !== undefined) {
                chunks.value = data.source_nodes;
            }
            queryResponse.value += data["message"];
        });

        ({ done, value } = await reader.read());
        isGeneratingResponse.value = true;
    }

    isGeneratingResponse.value = false;
    isProcessingQuery.value = false;
    chatHistory.value.addMessage("assistant", queryResponse.value);
    queryResponse.value = "";
}

async function sendQuery() {
    try {
        if (!canSendQuery.value) return;
        isProcessingQuery.value = true;

        if (chatHistory.value === null) {
            chatHistory.value = new ChatRequestBuilder(props.patientId)
                .addMessage(
                    "system",
                    "Antworte auf Deutsch! Sei so kurz und knapp wie möglich."
                )
                .addMessage("user", query.value);
        } else {
            chatHistory.value.addMessage("user", query.value);
        }

        query.value = "";

        const chatRequest = chatHistory.value.build();
        const response = await ApiService.stream_chat(chatRequest);
        const reader = response.body.getReader();
        readStream(reader);
    } catch (error) {
        console.error("API call failed:", error);
    }
}

// a computed ref
const chatMessages = computed(() => {
    return chatHistory.value.chatRequest.messages.slice(1);
});

const canSendQuery = computed(() => {
    return !isProcessingQuery.value && query.value != "";
});
</script>

<style scoped>
.user-message {
}

.assistant-message {
}
</style>
