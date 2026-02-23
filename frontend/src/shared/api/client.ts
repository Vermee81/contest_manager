import axios, { AxiosError } from "axios";

const apiClient = axios.create({
  baseURL: "/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    const message =
      (error.response?.data as { detail?: string })?.detail ??
      error.message ??
      "Unknown error";
    return Promise.reject(new Error(message));
  }
);

export default apiClient;
