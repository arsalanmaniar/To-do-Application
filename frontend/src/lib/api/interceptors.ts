import { TokenUtils } from '../auth/token-utils';
import { TokenRefresh } from '../auth/token-refresh';

/**
 * Request interceptor to add authentication token
 * @param config The axios request config
 * @returns Modified request config with authentication token
 */
export const authRequestInterceptor = async (config: any) => {
  // Check if token needs refresh before making the request
  await TokenRefresh.checkAndRefreshToken();

  // Get the current token
  const token = TokenUtils.getToken();

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
};

/**
 * Error handler for request interceptor
 * @param error The error object
 * @returns Promise rejection with the error
 */
export const authRequestInterceptorError = (error: any) => {
  return Promise.reject(error);
};

/**
 * Response interceptor to handle responses and errors
 * @param response The axios response
 * @returns The response data
 */
export const authResponseInterceptor = (response: any) => {
  // Return the response data directly
  return response.data;
};

/**
 * Error handler for response interceptor
 * Handles specific error cases like 401 Unauthorized
 * @param error The error object
 * @returns Promise rejection with the error or retries the request
 */
export const authResponseInterceptorError = async (error: any) => {
  // Handle specific error cases
  if (error.response?.status === 401) {
    // Try to refresh the token if we get a 401
    const refreshed = await TokenRefresh.refreshToken();

    if (refreshed) {
      // Retry the original request with the new token
      error.config.headers.Authorization = `Bearer ${refreshed}`;
      return error.config.adapter(error.config); // Assuming axios adapter pattern
    } else {
      // If refresh failed, redirect to sign-in
      if (typeof window !== 'undefined') {
        window.location.href = '/auth/sign-in';
      }
    }
  }

  // Return the error for handling by the calling function
  return Promise.reject(error);
};