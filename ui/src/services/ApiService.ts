import ChatRequest from "./types/ChatRequest";

class ApiService {
    private baseUrl: string;

    constructor() {
        this.baseUrl = "http://127.0.0.1:8000";
    }

    public async getRoot(): Promise<Response> {
        return fetch(this.baseUrl + "/");
    }

    public async getDocuments(patientId: string): Promise<Response> {
        const url = `${this.baseUrl}/documents?patient_id=${patientId}`;
        return fetch(url);
    }

    public async chat(data: ChatRequest): Promise<Response> {
        const response = fetch(this.baseUrl + "/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });
        return response;
    }

    public async stream_chat(data: ChatRequest): Promise<Response> {
        const response = fetch(this.baseUrl + "/stream_chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });
        return response;
    }
}

export default new ApiService();
