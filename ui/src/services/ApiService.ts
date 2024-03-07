import axios, { AxiosInstance } from "axios";
import ChatRequest from "./types/ChatRequest";

class ApiService {
  private apiClient: AxiosInstance;
  private baseUrl: string;

  constructor() {
    this.baseUrl = "http://127.0.0.1:8000";
    this.apiClient = axios.create({
      baseURL: "http://127.0.0.1:8000", // Replace with your API URL
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    });
  }

  public async getRoot(): Promise<ApiResponse<any>> {
    return this.apiClient.get("/");
  }

  public async getDocuments(patientId: string): Promise<Response> {
    const url = `${this.baseUrl}/documents?patient_id=${patientId}`;
    return fetch(url);
  }

  public async chat(data: ChatRequest): Promise<ApiResponse<any>> {
    return this.apiClient.post("/chat", data);
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
