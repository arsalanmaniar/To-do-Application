import apiClient from './client';

// Authentication API service for handling authentication-related API calls
export const authApi = {
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
      console.error('Registration API error:', error);
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
      console.error('Sign in API error:', error);
      throw error;
    }
  },

  /**
   * Sign out the current user
   * @returns Promise resolving when sign out is complete
   */
  async signOut() {
    try {
      const response = await apiClient.post('/auth/logout');
      return response;
    } catch (error) {
      console.error('Sign out API error:', error);
      throw error;
    }
  },

  /**
   * Get the current user's profile
   * @returns Promise resolving to user profile data
   */
  async getProfile() {
    try {
      const response = await apiClient.get('/auth/profile');
      return response;
    } catch (error) {
      console.error('Get profile API error:', error);
      throw error;
    }
  },

  /**
   * Update user profile
   * @param profileData - Updated profile data
   * @returns Promise resolving to update result
   */
  async updateProfile(profileData: Partial<{ name: string; email: string }>) {
    try {
      const response = await apiClient.put('/auth/profile', profileData);
      return response;
    } catch (error) {
      console.error('Update profile API error:', error);
      throw error;
    }
  },

  /**
   * Refresh the authentication token
   * @returns Promise resolving to refreshed token
   */
  async refreshToken() {
    try {
      const response = await apiClient.post('/auth/refresh');
      return response;
    } catch (error) {
      console.error('Token refresh API error:', error);
      throw error;
    }
  },

  /**
   * Request password reset
   * @param email - User's email address
   * @returns Promise resolving to password reset request result
   */
  async requestPasswordReset(email: string) {
    try {
      const response = await apiClient.post('/auth/forgot-password', { email });
      return response;
    } catch (error) {
      console.error('Password reset request API error:', error);
      throw error;
    }
  },

  /**
   * Reset password with token
   * @param token - Password reset token
   * @param newPassword - New password
   * @returns Promise resolving to password reset result
   */
  async resetPassword(token: string, newPassword: string) {
    try {
      const response = await apiClient.post('/auth/reset-password', {
        token,
        newPassword
      });
      return response;
    } catch (error) {
      console.error('Password reset API error:', error);
      throw error;
    }
  }
};

// Export individual functions for named imports
export const {
  register,
  signIn,
  signOut,
  getProfile,
  updateProfile,
  refreshToken,
  requestPasswordReset,
  resetPassword
} = authApi;