import './globals.css';
import type { Metadata } from 'next';
import { AuthProvider } from '@/components/providers/auth-provider';
import React from 'react';

export const metadata: Metadata = {
  title: 'Todo Full-Stack Web Application',
  description: 'A secure todo application with authentication and task management',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="font-sans">
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
