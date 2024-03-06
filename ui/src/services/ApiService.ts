import axios, { AxiosInstance } from "axios";
import ChatRequest from "./types/ChatRequest";

class ApiService {
  private apiClient: AxiosInstance;

  constructor() {
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

  public async complete(data: CompletionRequest): Promise<ApiResponse<any>> {
    return this.apiClient.post("/complete", data);
  }

  public async getDocuments(
    patientId: string
  ): Promise<ApiResponse<Document[]>> {
    return this.apiClient.get(`/documents?patient_id=${patientId}`);
  }

  public async chat(data: ChatRequest): Promise<ApiResponse<any>> {
    return this.apiClient.post("/chat", data);
  }
}

export default new ApiService();
