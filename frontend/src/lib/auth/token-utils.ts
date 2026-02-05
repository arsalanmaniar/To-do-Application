// Utility functions for handling JWT tokens in the browser
export const TokenUtils = {
  /**
   * Get the JWT token from browser localStorage
   * @returns The JWT token string or null if not found
   */
  getToken(): string | null {
    if (typeof window === 'undefined') {
      // Server-side, no token available
      return null;
    }

    // Get the token from localStorage
    return localStorage.getItem('auth-token');
  },

  /**
   * Store the JWT token in browser localStorage
   * @param token The JWT token to store
   */
  setToken(token: string): void {
    if (typeof window === 'undefined') {
      // Server-side, nothing to do
      return;
    }

    // Store the token in localStorage
    localStorage.setItem('auth-token', token);
  },

  /**
   * Remove the JWT token from browser localStorage
   */
  removeToken(): void {
    if (typeof window === 'undefined') {
      // Server-side, nothing to do
      return;
    }

    // Remove the token from localStorage
    localStorage.removeItem('auth-token');
  },

  /**
   * Check if the JWT token is expired
   * @param token The JWT token to check
   * @returns True if the token is expired, false otherwise
   */
  isTokenExpired(token: string): boolean {
    try {
      // Decode the token payload (second part of JWT)
      const base64Payload = token.split('.')[1];
      const payload = JSON.parse(atob(base64Payload));

      // Check if the token has an expiration time
      if (payload.exp) {
        const currentTime = Math.floor(Date.now() / 1000);
        return payload.exp < currentTime;
      }

      return false; // If no exp claim, assume not expired
    } catch (error) {
      // If we can't decode the token, assume it's invalid/expired
      console.error('Error decoding token:', error);
      return true;
    }
  },

  /**
   * Get the user data from the JWT token
   * @param token The JWT token to decode
   * @returns The decoded user data or null if unable to decode
   */
  getUserData(token: string): any | null {
    try {
      // Decode the token payload (second part of JWT)
      const base64Payload = token.split('.')[1];
      const payload = JSON.parse(atob(base64Payload));

      return payload;
    } catch (error) {
      console.error('Error decoding token:', error);
      return null;
    }
  },

  /**
   * Check if the user is authenticated
   * @returns True if the user is authenticated, false otherwise
   */
  isAuthenticated(): boolean {
    const token = this.getToken();

    if (!token) {
      return false;
    }

    return !this.isTokenExpired(token);
  }
};