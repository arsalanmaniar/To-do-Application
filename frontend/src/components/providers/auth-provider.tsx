'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { TokenUtils } from '@/lib/auth/token-utils';
import { authService } from '@/lib/auth/auth-service';

// Define the shape of our authentication context
interface AuthContextType {
  user: any | null;
  isAuthenticated: boolean;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<any>;
  signOut: () => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<any>;
  getSession: () => Promise<any>;
}

// Create the authentication context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Props for the AuthProvider component
interface AuthProviderProps {
  children: ReactNode;
}

// AuthProvider component to wrap the application
export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Check authentication status on component mount
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        if (TokenUtils.isAuthenticated()) {
          const profile = await authService.getProfile();
          if (profile) {
            setUser(profile);
          } else {
            setUser(null);
          }
        } else {
          setUser(null);
        }
      } catch (error) {
        console.error('Error checking auth status:', error);
        // If profile fetch fails, still set user to null but continue loading
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  // Sign in function
  const signIn = async (email: string, password: string) => {
    setLoading(true);
    try {
      const response = await authService.signIn({ email, password });
      if (response?.access_token) {
        // Store the token in local storage
        TokenUtils.setToken(response.access_token);

        // Get the user profile after successful sign in
        try {
          const profile = await authService.getProfile();
          if (profile) {
            setUser(profile);
          }
        } catch (profileError) {
          console.error('Failed to fetch user profile after login:', profileError);
          // Continue with login flow even if profile fetch fails
          // The user is still authenticated based on the token
        }
      }
      return response;
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  // Sign out function
  const signOut = async () => {
    setLoading(true);
    try {
      await authService.signOut();
      setUser(null);
    } catch (error) {
      console.error('Sign out error:', error);
      // Even if sign out fails, clear local state
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  // Register function
  const register = async (email: string, password: string, name: string) => {
    setLoading(true);
    try {
      const response = await authService.register({ name, email, password });
      if (response?.id) {
        // After successful registration, sign in the user
        const signInResponse = await authService.signIn({ email, password });
        if (signInResponse?.access_token) {
          // Store the token in local storage
          TokenUtils.setToken(signInResponse.access_token);

          // Get the user profile after successful sign in
          try {
            const profile = await authService.getProfile();
            if (profile) {
              setUser(profile);
            }
          } catch (profileError) {
            console.error('Failed to fetch user profile after registration:', profileError);
            // Continue with registration flow even if profile fetch fails
            // The user is still authenticated based on the token
          }
        }
      }
      return response;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  // Get session function
  const getSession = async () => {
    try {
      if (TokenUtils.isAuthenticated()) {
        const profile = await authService.getProfile();
        if (profile?.data) {
          setUser(profile.data);
          return { user: profile.data, token: TokenUtils.getToken() };
        } else {
          setUser(null);
          return null;
        }
      } else {
        setUser(null);
        return null;
      }
    } catch (error) {
      console.error('Get session error:', error);
      setUser(null);
      return null;
    }
  };

  // Check if user is authenticated - only depends on token validity, not user object availability
  // The user object can be loaded asynchronously after authentication is established
  const isAuthenticated = TokenUtils.isAuthenticated();

  // Provide the authentication context to child components
  const value: AuthContextType = {
    user,
    isAuthenticated,
    loading,
    signIn,
    signOut,
    register,
    getSession,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use the authentication context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};