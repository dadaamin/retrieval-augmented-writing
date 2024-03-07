interface ChatMessage {
    role: "system" | "user";
    content: string;
}

interface ChatRequest {
    messages: ChatMessage[];
    patient_id: string;
}

export default class ChatRequestBuilder {
    private chatRequest: ChatRequest;

    constructor(patientId: string) {
        this.chatRequest = {
            messages: [],
            patient_id: patientId,
        };
    }

    addMessage(role: ChatMessage["role"], content: string): ChatRequestBuilder {
        const message: ChatMessage = { role, content };
        this.chatRequest.messages.push(message);
        return this;
    }

    build(): ChatRequest {
        return this.chatRequest;
    }
}
