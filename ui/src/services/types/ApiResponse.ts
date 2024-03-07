// Response interfaces can also be defined if your API responses are standardized
interface ApiResponse<T> {
    data: T;
    message?: string;
}
