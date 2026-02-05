import { TokenUtils } from './token-utils';
import apiClient from '../api/client';

/**
 * JWT token refresh mechanism for maintaining user sessions
 */
export class TokenRefresh {
  private static refreshPromise: Promise<string> | null = null;

  /**
   * Refresh the JWT token if it's expired or about to expire
   * @returns Promise resolving to the new token or null if refresh failed
   */
  static async refreshToken(): Promise<string | null> {
    // Prevent multiple simultaneous refresh requests
    if (this.refreshPromise) {
      return this.refreshPromise;
    }

    const token = TokenUtils.getToken();
    if (!token) {
      console.warn('No token found for refresh');
      return null;
    }

    // Check if token is not expired, no need to refresh
    if (!TokenUtils.isTokenExpired(token)) {
      return token;
    }

    try {
      this.refreshPromise = this.performRefresh();
      const newToken = await this.refreshPromise;

      if (newToken) {
        // Store the new token
        TokenUtils.setToken(newToken);
        return newToken;
      } else {
        // If refresh failed, remove the old token
        TokenUtils.removeToken();
        return null;
      }
    } catch (error) {
      console.error('Token refresh failed:', error);
      // If refresh failed, remove the old token
      TokenUtils.removeToken();
      return null;
    } finally {
      this.refreshPromise = null;
    }
  }

  /**
   * Perform the actual token refresh request
   * @returns Promise resolving to the new token
   */
  private static async performRefresh(): Promise<string | null> {
    try {
      // For now, return the existing token if it exists
      // Our backend doesn't have a dedicated refresh endpoint
      // In a real implementation, we'd call the backend refresh endpoint
      const existingToken = TokenUtils.getToken();
      return existingToken;
    } catch (error) {
      console.error('Perform token refresh error:', error);
      return null;
    }
  }

  /**
   * Check if token is valid (not expired)
   * Since backend doesn't support refresh tokens, this just validates the current token
   * @returns Promise resolving to true if token is valid, false otherwise
   */
  static async checkAndRefreshToken(): Promise<boolean> {
    const token = TokenUtils.getToken();

    if (!token) {
      return false;
    }

    // Check if token is expired
    const isExpired = TokenUtils.isTokenExpired(token);

    if (isExpired) {
      // If token is expired, remove it and return false
      TokenUtils.removeToken();
      return false;
    }

    return true;
  }

  /**
   * Decode the payload of a JWT token
   * @param token The JWT token to decode
   * @returns The decoded payload or null if decoding fails
   */
  private static decodeTokenPayload(token: string) {
    try {
      const parts = token.split('.');
      if (parts.length !== 3) {
        throw new Error('Invalid token format');
      }

      // Add padding if needed
      const payload = parts[1].replace(/-/g, '+').replace(/_/g, '/');
      const decodedPayload = atob(payload);
      return JSON.parse(decodedPayload);
    } catch (error) {
      console.error('Error decoding token payload:', error);
      return null;
    }
  }
}

// Export convenience functions
export const { refreshToken, checkAndRefreshToken } = TokenRefresh;