<template>
  <div
    class="w-full h-full p-3 border-1 border-200 border-round shadow-none bg-white"
  >
    <div class="h-full w-full flex flex-column align-items-stretch gap-2">
      <div class="flex-grow-1 flex flex-column gap-2">
        <template v-for="(chunk, index) in chunks" :key="index">
          <div class="border-1 border-200 border-round p-2">
            <p class="text-sm text-light">{{ chunk.node.text }}</p>
          </div>
        </template>
      </div>
      <div
        v-if="queryResponse"
        class="border-200 border-1 border-round h-2 p-3 flex-grow-0 flex-column"
      >
        <p class="text-lg font-medium">Mixtral</p>
        <p>{{ queryResponse }}</p>
      </div>
      <div class="flex gap-1">
        <InputText
          v-model="query"
          class="flex-grow-1"
          type="text"
          @keyup.enter="sendQuery"
        ></InputText>
        <Button label="Send" icon="pi pi-send" @click="sendQuery"></Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import ApiService from "@/services/ApiService.ts";
import ChatRequestBuilder from "@/services/types/ChatRequest.ts";

const chunks = ref([]);
const query = ref("");
const queryResponse = ref("");

const props = defineProps(["patientId"]);

async function sendQuery() {
  try {
    const chatRequest = new ChatRequestBuilder(props.patientId)
      .addMessage(
        "system",
        "Antworte auf Deutsch! Sei so kurz und knapp wie möglich."
      )
      .addMessage("user", query.value)
      .build();

    console.log(chatRequest);
    const response = await ApiService.chat(chatRequest);
    queryResponse.value = response.data["response"];
    chunks.value = response.data["source_nodes"];
    // console.log(response.data);
    console.log(response.data["source_nodes"]);
    // Process your data here
  } catch (error) {
    console.error("API call failed:", error);
  }
}
</script>
