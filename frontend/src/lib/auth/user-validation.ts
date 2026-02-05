import { TokenUtils } from './token-utils';

/**
 * User data validation utilities to ensure proper data isolation
 */
export class UserValidation {
  /**
   * Validates that the provided data belongs to the current user
   * @param data The data object to validate (e.g., a task, profile, etc.)
   * @param userIdField The field name that contains the user ID (default: 'userId')
   * @returns boolean indicating if the data belongs to the current user
   */
  static validateUserDataOwnership(data: any, userIdField: string = 'userId'): boolean {
    if (!data || typeof data !== 'object') {
      return false;
    }

    const currentUserId = this.getCurrentUserId();
    if (!currentUserId) {
      return false;
    }

    const dataUserId = data[userIdField];
    return dataUserId === currentUserId;
  }

  /**
   * Validates an array of data objects to ensure they all belong to the current user
   * @param dataArray The array of data objects to validate
   * @param userIdField The field name that contains the user ID (default: 'userId')
   * @returns boolean indicating if all data belongs to the current user
   */
  static validateUserDataOwnershipBatch(dataArray: any[], userIdField: string = 'userId'): boolean {
    if (!Array.isArray(dataArray)) {
      return false;
    }

    return dataArray.every(data => this.validateUserDataOwnership(data, userIdField));
  }

  /**
   * Gets the current user ID from the JWT token
   * @returns The current user ID or null if not authenticated or token doesn't contain user ID
   */
  static getCurrentUserId(): string | null {
    const token = TokenUtils.getToken();
    if (!token) {
      return null;
    }

    try {
      // Decode the token payload (second part of JWT)
      const base64Payload = token.split('.')[1];
      const payload = JSON.parse(atob(base64Payload));

      // Look for common user ID fields in the payload
      return payload.userId || payload.sub || payload.id || null;
    } catch (error) {
      console.error('Error decoding token for user ID:', error);
      return null;
    }
  }

  /**
   * Validates that a user ID is valid (not null, not empty, properly formatted)
   * @param userId The user ID to validate
   * @returns boolean indicating if the user ID is valid
   */
  static validateUserId(userId: string | null | undefined): boolean {
    if (!userId) {
      return false;
    }

    // Basic validation: check if it's a non-empty string
    return typeof userId === 'string' && userId.trim().length > 0;
  }

  /**
   * Sanitizes user data by removing fields that shouldn't be exposed to the client
   * @param data The data object to sanitize
   * @param allowedFields Optional array of fields that are allowed to be returned
   * @returns A sanitized version of the data object
   */
  static sanitizeUserData(data: any, allowedFields?: string[]): any {
    if (!data || typeof data !== 'object') {
      return data;
    }

    if (!allowedFields) {
      // Default sensitive fields to exclude
      const defaultExcluded = ['password', 'salt', 'hash', 'token', 'session', 'secret'];
      return Object.keys(data).reduce((sanitized: any, key) => {
        if (!defaultExcluded.includes(key.toLowerCase())) {
          sanitized[key] = data[key];
        }
        return sanitized;
      }, {});
    }

    // Only include allowed fields
    return allowedFields.reduce((sanitized: any, field) => {
      if (data.hasOwnProperty(field)) {
        sanitized[field] = data[field];
      }
      return sanitized;
    }, {});
  }

  /**
   * Validates user permissions for a specific action
   * @param action The action to validate (e.g., 'read', 'write', 'delete')
   * @param resource The resource to access (e.g., 'tasks', 'profile')
   * @param resourceId Optional resource ID for more granular permission checks
   * @returns boolean indicating if the user has permission
   */
  static validateUserPermissions(
    action: 'read' | 'write' | 'delete' | 'update',
    resource: string,
    resourceId?: string
  ): boolean {
    // In a real implementation, this would check user roles and permissions
    // For now, we'll implement basic validation based on authentication and ownership

    const currentUserId = this.getCurrentUserId();
    if (!currentUserId) {
      return false;
    }

    // If it's a user's own data, allow basic CRUD operations
    if (resource === 'profile' && action === 'read' && !resourceId) {
      return true; // Users can read their own profile
    }

    if (resource === 'profile' && action === 'update' && !resourceId) {
      return true; // Users can update their own profile
    }

    // For other resources, if a resourceId is provided, we'd need to check ownership
    // This would typically involve making an API call to verify ownership
    // For now, we'll return true for demonstration purposes
    return true;
  }
}

// Export convenience functions
export const {
  validateUserDataOwnership,
  validateUserDataOwnershipBatch,
  getCurrentUserId,
  validateUserId,
  sanitizeUserData,
  validateUserPermissions
} = UserValidation;