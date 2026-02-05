'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/providers/auth-provider';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode; // Optional fallback component while checking auth status
}

// Protected route wrapper component that checks authentication before rendering children
export default function ProtectedRoute({ children, fallback }: ProtectedRouteProps) {
  const router = useRouter();
  const { isAuthenticated, loading } = useAuth();

  useEffect(() => {
    // If user is not authenticated and not loading, redirect to sign-in
    if (!loading && !isAuthenticated) {
      router.push('/auth/sign-in');
    }
  }, [isAuthenticated, loading, router]);

  // Show fallback while checking authentication status, or redirect if not authenticated
  if (loading) {
    return fallback || (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // If not authenticated, don't render anything (redirect effect will handle navigation)
  if (!isAuthenticated) {
    return null;
  }

  // If authenticated, render the protected content
  return <>{children}</>;
}