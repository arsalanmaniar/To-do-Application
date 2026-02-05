import { NextRequest, NextResponse } from 'next/server';

// Define protected routes that require authentication
const protectedRoutes = ['/dashboard', '/profile', '/settings'];

export function middleware(request: NextRequest) {
  // For our custom auth system, we'll check for the presence of the token in the Authorization header
  // The API client should include the JWT token in the Authorization header
  const authHeader = request.headers.get('authorization');
  const hasToken = authHeader && authHeader.startsWith('Bearer ');

  // Check if the current route is protected
  const isProtectedRoute = protectedRoutes.some(route =>
    request.nextUrl.pathname.startsWith(route)
  );

  // If trying to access a protected route without a token, redirect to sign-in
  if (isProtectedRoute && !hasToken) {
    // Redirect to sign-in page with a return URL
    const signInUrl = new URL('/auth/sign-in', request.nextUrl.origin);
    signInUrl.searchParams.set('callbackUrl', request.nextUrl.pathname);
    return NextResponse.redirect(signInUrl);
  }

  // Allow the request to continue
  return NextResponse.next();
}

// Specify which paths the middleware should run for
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};