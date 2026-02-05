import React from 'react';

interface ApiErrorHandlerProps {
  error: {
    message: string;
    status?: number;
    details?: string;
  } | null;
  onRetry?: () => void;
  onDismiss?: () => void;
}

export default function ApiErrorHandler({ error, onRetry, onDismiss }: ApiErrorHandlerProps) {
  if (!error) {
    return null;
  }

  // Determine error type based on status code
  const getErrorType = () => {
    if (error.status) {
      if (error.status >= 500) return 'server';
      if (error.status >= 400) return 'client';
    }
    return 'network';
  };

  const errorType = getErrorType();

  // Get error title based on type
  const getTitle = () => {
    switch (errorType) {
      case 'server':
        return 'Server Error';
      case 'client':
        return 'Request Failed';
      case 'network':
        return 'Network Error';
      default:
        return 'Error';
    }
  };

  // Get error icon based on type
  const getIcon = () => {
    switch (errorType) {
      case 'server':
        return (
          <svg className="h-6 w-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        );
      case 'client':
        return (
          <svg className="h-6 w-6 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        );
      case 'network':
        return (
          <svg className="h-6 w-6 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        );
      default:
        return (
          <svg className="h-6 w-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        );
    }
  };

  return (
    <div className="rounded-md bg-red-50 p-4 mb-4">
      <div className="flex">
        <div className="flex-shrink-0">
          {getIcon()}
        </div>
        <div className="ml-3">
          <h3 className="text-sm font-medium text-red-800">
            {getTitle()}
          </h3>
          <div className="mt-2 text-sm text-red-700">
            <p>{error.message}</p>
            {error.details && (
              <p className="mt-1 text-xs text-red-600">{error.details}</p>
            )}
          </div>
          <div className="mt-4">
            <div className="-mx-2 -my-1.5 flex">
              {onRetry && (
                <button
                  type="button"
                  onClick={onRetry}
                  className="mx-2 rounded-md bg-red-50 px-2 py-1.5 text-sm font-medium text-red-800 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-red-600 focus:ring-offset-2 focus:ring-offset-red-50"
                >
                  Retry
                </button>
              )}
              {onDismiss && (
                <button
                  type="button"
                  onClick={onDismiss}
                  className="mx-2 rounded-md bg-red-50 px-2 py-1.5 text-sm font-medium text-red-800 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-red-600 focus:ring-offset-2 focus:ring-offset-red-50"
                >
                  Dismiss
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}