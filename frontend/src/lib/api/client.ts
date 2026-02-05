import axios, { AxiosRequestConfig, AxiosResponse, AxiosError, InternalAxiosRequestConfig } from 'axios';
import { TokenUtils } from '../auth/token-utils';
import { TokenRefresh } from '../auth/token-refresh';

// Extend the InternalAxiosRequestConfig type to include retry properties
declare module 'axios' {
  interface InternalAxiosRequestConfig {
    retryCount?: number;
    maxRetries?: number;
  }
}

// Create an Axios instance with default configuration
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 10000, // 10 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Function to implement retry logic with exponential backoff
const retryRequest = async (
  config: AxiosRequestConfig,
  retries: number = 3,
  delay: number = 1000
): Promise<AxiosResponse> => {
  try {
    return await apiClient(config);
  } catch (error) {
    if (retries > 0) {
      // Exponential backoff: wait longer between each retry
      await new Promise(resolve => setTimeout(resolve, delay));
      return retryRequest(config, retries - 1, delay * 2);
    }
    throw error;
  }
};

// Request interceptor to add authentication token
apiClient.interceptors.request.use(
  (config) => {
    // Get the current token
    const token = TokenUtils.getToken();

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle responses and errors
apiClient.interceptors.response.use(
  (response) => {
    // Return the response data directly
    return response.data;
  },
  async (error: AxiosError) => {
    // Handle specific error cases
    if (error.response?.status === 401) {
      // For 401 errors, immediately clear the token and redirect to sign-in
      // Do NOT attempt to refresh the token as backend doesn't support refresh tokens
      TokenUtils.removeToken();

      // Redirect to sign-in page
      if (typeof window !== 'undefined') {
        window.location.href = '/auth/sign-in';
      }

      // Don't retry the request - just return the error
      return Promise.reject(error);
    }

    // For network errors or server errors, implement retry logic
    const config = error.config;
    if (config && !config.retryCount) {
      const status = error.response?.status;

      // Retry on network errors (0) or server errors (5xx)
      if (!status || (status >= 500 && status < 600)) {
        config.retryCount = config.retryCount || 0;
        const maxRetries = config.maxRetries || 3;

        if (config.retryCount < maxRetries) {
          config.retryCount++;

          // Exponential backoff: wait longer between each retry
          const delay = Math.pow(2, config.retryCount) * 1000; // 2^retryCount * 1000ms
          await new Promise(resolve => setTimeout(resolve, delay));

          return apiClient(config);
        }
      }
    }

    // Return the error for handling by the calling function
    return Promise.reject(error);
  }
);

export default apiClient;