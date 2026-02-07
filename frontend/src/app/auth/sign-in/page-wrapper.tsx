'use client';

import { Suspense } from 'react';
import SignInPageContent from './page-content';

export default function SignInPageWrapper() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <SignInPageContent />
    </Suspense>
  );
}