'use client';

import { useState } from 'react';
import { useAuth } from '@/components/providers/auth-provider';
import ProtectedRoute from '@/components/auth/protected-route';
import Link from 'next/link';

export default function CalendarPage() {
  const { user, signOut } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);

  const handleSignOut = async () => {
    try {
      await signOut();
    } catch (err) {
      console.error('Sign out error:', err);
    }
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        {/* Mobile sidebar toggle */}
        <div className="md:hidden">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="fixed top-4 left-4 z-50 p-2 rounded-md bg-indigo-600 text-white shadow-lg"
          >
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>

        {/* Sidebar */}
        <aside
          className={`fixed inset-y-0 left-0 z-40 w-64 bg-white shadow-lg transform ${
            sidebarOpen ? 'translate-x-0' : '-translate-x-full'
          } md:translate-x-0 transition-transform duration-300 ease-in-out`}
        >
          <div className="flex items-center justify-between p-4 border-b">
            <h2 className="text-xl font-bold text-indigo-600">TodoApp</h2>
            <button
              onClick={() => setSidebarOpen(false)}
              className="md:hidden text-gray-500 hover:text-gray-700"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <nav className="mt-5 px-2">
            <div className="space-y-1">
              <Link
                href="/dashboard"
                className="flex items-center px-4 py-2 text-base font-medium text-gray-600 rounded-md hover:bg-gray-50 hover:text-gray-900"
              >
                <svg className="mr-3 h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
                Dashboard
              </Link>

              <Link
                href="/calendar"
                className="flex items-center px-4 py-2 text-base font-medium text-indigo-700 bg-indigo-50 border-l-4 border-indigo-500 rounded-md"
              >
                <svg className="mr-3 h-5 w-5 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Calendar
              </Link>

              <Link
                href="/projects"
                className="mt-1 flex items-center px-4 py-2 text-base font-medium text-gray-600 rounded-md hover:bg-gray-50 hover:text-gray-900"
              >
                <svg className="mr-3 h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                Projects
              </Link>

              <Link
                href="/team"
                className="mt-1 flex items-center px-4 py-2 text-base font-medium text-gray-600 rounded-md hover:bg-gray-50 hover:text-gray-900"
              >
                <svg className="mr-3 h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                Team
              </Link>

              <button
                onClick={handleSignOut}
                className="mt-1 w-full flex items-center px-4 py-2 text-base font-medium text-gray-600 rounded-md hover:bg-gray-50 hover:text-gray-900 text-left"
              >
                <svg className="mr-3 h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                Sign out
              </button>
            </div>
          </nav>
        </aside>

        {/* Main content */}
        <div className="md:pl-64 flex flex-col">
          {/* Top navigation */}
          <header className="bg-white shadow-sm">
            <div className="flex items-center justify-between h-16 px-4 sm:px-6 lg:px-8">
              <div className="flex items-center">
                <h1 className="text-xl font-semibold text-gray-900">Calendar</h1>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-700 hidden sm:block">
                  Welcome, {user?.name || user?.email}
                </span>
                <button
                  onClick={handleSignOut}
                  className="hidden sm:inline-flex items-center px-3 py-1 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Sign out
                </button>
              </div>
            </div>
          </header>

          {/* Page content */}
          <main className="flex-1 py-8">
            <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="text-center">
                <h1 className="text-3xl font-bold text-gray-900 mb-4">Calendar</h1>
                <p className="text-gray-600">Track your tasks and events over time</p>
                <div className="mt-8 bg-white shadow rounded-lg p-6">
                  <div className="max-w-4xl mx-auto">
                    <div className="flex items-center justify-between mb-6">
                      <h2 className="text-2xl font-bold text-gray-800">January 2026</h2>
                      <div className="flex space-x-2">
                        <button className="p-2 rounded-md bg-gray-100 hover:bg-gray-200">
                          <svg className="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                          </svg>
                        </button>
                        <button className="p-2 rounded-md bg-gray-100 hover:bg-gray-200">
                          <svg className="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                          </svg>
                        </button>
                      </div>
                    </div>

                    {/* Calendar grid */}
                    <div className="grid grid-cols-7 gap-1 mb-2">
                      {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
                        <div key={day} className="p-3 text-center text-sm font-medium text-gray-500 bg-gray-50 rounded-md">
                          {day}
                        </div>
                      ))}
                    </div>

                    <div className="flex">
                      <div className="grid grid-cols-7 gap-1 flex-1">
                        {/* Empty days for the start of the month */}
                        {Array.from({ length: 3 }).map((_, i) => (
                          <div key={`empty-start-${i}`} className="min-h-24 p-2 border border-gray-200 rounded-md"></div>
                        ))}

                        {/* Days of the month */}
                        {Array.from({ length: 31 }).map((_, i) => {
                          const day = i + 1;
                          const isToday = day === new Date().getDate();
                          const isSelected = selectedDate && selectedDate.getDate() === day;
                          return (
                            <div
                              key={day}
                              onClick={() => setSelectedDate(new Date(2026, 0, day))}
                              className={`min-h-24 p-2 border rounded-md cursor-pointer transition-all ${
                                isToday
                                  ? 'border-indigo-500 bg-indigo-50 ring-2 ring-indigo-500'
                                  : isSelected
                                    ? 'border-indigo-300 bg-indigo-100 ring-1 ring-indigo-300'
                                    : 'border-gray-200 hover:bg-gray-50'
                              }`}
                            >
                              <div className={`text-sm font-medium ${
                                isToday ? 'text-indigo-700' : 'text-gray-900'
                              }`}>
                                {day}
                              </div>
                              {day === 15 && (
                                <div className="mt-1 text-xs px-2 py-1 bg-indigo-100 text-indigo-800 rounded-full truncate">
                                  Meeting
                                </div>
                              )}
                              {day === 20 && (
                                <div className="mt-1 text-xs px-2 py-1 bg-green-100 text-green-800 rounded-full truncate">
                                  Deadline
                                </div>
                              )}
                            </div>
                          );
                        })}
                      </div>

                      {/* Side Panel for selected date */}
                      {selectedDate && (
                        <div className="ml-4 w-80 bg-white border border-gray-200 rounded-lg p-4 shadow-lg">
                          <div className="flex justify-between items-center mb-4">
                            <h3 className="text-lg font-semibold text-gray-900">
                              {selectedDate.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
                            </h3>
                            <button
                              onClick={() => setSelectedDate(null)}
                              className="text-gray-400 hover:text-gray-600"
                            >
                              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                              </svg>
                            </button>
                          </div>

                          <div className="space-y-3">
                            <div className="p-3 bg-gray-50 rounded-md">
                              <p className="text-sm text-gray-600">No tasks scheduled yet</p>
                            </div>
                          </div>

                          <div className="mt-4 pt-4 border-t border-gray-200">
                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                              Upcoming feature: Task scheduling
                            </span>
                          </div>
                        </div>
                      )}
                    </div>

                    <div className="mt-8 p-4 bg-blue-50 rounded-lg border border-blue-100">
                      <h3 className="font-medium text-blue-800 mb-2">Tasks by Date</h3>
                      <p className="text-sm text-blue-600">Tasks will appear here by date</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </main>
        </div>

        {/* Overlay for mobile sidebar */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 z-30 bg-black bg-opacity-50 md:hidden"
            onClick={() => setSidebarOpen(false)}
          ></div>
        )}
      </div>
    </ProtectedRoute>
  );
}