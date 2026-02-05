import apiClient from '@/lib/api/client';
import { TokenUtils } from './token-utils';

// Authentication service functions for handling user authentication
export const authService = {
  /**
   * Register a new user
   * @param userData - User registration data (name, email, password)
   * @returns Promise resolving to registration result
   */
  async register(userData: { name: string; email: string; password: string }) {
    try {
      const response = await apiClient.post('/auth/register', userData);
      return response;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  },

  /**
   * Sign in a user
   * @param credentials - User credentials (email, password)
   * @returns Promise resolving to sign in result
   */
  async signIn(credentials: { email: string; password: string }) {
    try {
      const response = await apiClient.post('/auth/login', credentials);
      return response;
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    }
  },

  /**
   * Sign out the current user
   * @returns Promise resolving when sign out is complete
   */
  async signOut() {
    try {
      // For now, just remove the token from storage
      // Our backend doesn't have a dedicated logout endpoint
      TokenUtils.removeToken();
    } catch (error) {
      console.error('Sign out error:', error);
      // Still remove the token even if there's an error
      TokenUtils.removeToken();
      throw error;
    }
  },

  /**
   * Get the current user's profile
   * @returns Promise resolving to user profile data
   */
  async getProfile() {
    try {
      const response = await apiClient.get('/auth/me');
      return response;
    } catch (error: any) {
      console.error('Get profile error:', error);
      // For now, return a minimal user object if profile fetch fails
      // This allows login to continue even if profile endpoint has issues
      if (error?.response?.status === 404 || error?.response?.status === 401) {
        // Try to get user info from token if direct profile fetch fails
        const token = TokenUtils.getToken();
        if (token) {
          try {
            // Decode the token to get user ID
            const base64Payload = token.split('.')[1];
            const payload = JSON.parse(atob(base64Payload));
            // Return a minimal user object based on token data
            return {
              id: payload.sub, // The user ID is in the 'sub' claim
              email: payload.email || '', // Email might be available if stored in token
              is_active: true,
              created_at: null
            };
          } catch (decodeError) {
            console.error('Error decoding token:', decodeError);
          }
        }
      }
      // If we couldn't create a fallback user object, then throw the error
      throw error;
    }
  }
};

// Export individual functions for named imports
export const {
  register,
  signIn,
  signOut,
  getProfile
} = authService;