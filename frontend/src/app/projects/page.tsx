'use client';

import { useState } from 'react';
import { useAuth } from '@/components/providers/auth-provider';
import ProtectedRoute from '@/components/auth/protected-route';
import Link from 'next/link';

export default function ProjectsPage() {
  const { user, signOut } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [selectedProject, setSelectedProject] = useState<any>(null);

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
                className="flex items-center px-4 py-2 text-base font-medium text-gray-600 rounded-md hover:bg-gray-50 hover:text-gray-900"
              >
                <svg className="mr-3 h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Calendar
              </Link>

              <Link
                href="/projects"
                className="flex items-center px-4 py-2 text-base font-medium text-indigo-700 bg-indigo-50 border-l-4 border-indigo-500 rounded-md"
              >
                <svg className="mr-3 h-5 w-5 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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
                <h1 className="text-xl font-semibold text-gray-900">Projects</h1>
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
                <h1 className="text-3xl font-bold text-gray-900 mb-4">Projects</h1>
                <p className="text-gray-600">Organize your tasks into different projects</p>
                <div className="mt-8">
                  <div className="flex">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 flex-1">
                      {/* Personal Project Card */}
                      <div
                        className="bg-white shadow rounded-lg p-6 border border-gray-200 hover:shadow-md transition-shadow cursor-pointer"
                        onClick={() => setSelectedProject({
                          name: 'Personal',
                          description: 'Personal tasks and goals for your daily life and hobbies.',
                          tasks: 5,
                          status: 'Active',
                          icon: 'folder',
                          color: 'indigo'
                        })}
                      >
                        <div className="flex items-center mb-4">
                          <div className="p-2 bg-indigo-100 rounded-md">
                            <svg className="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                            </svg>
                          </div>
                          <h3 className="text-lg font-semibold text-gray-900 ml-3">Personal</h3>
                        </div>
                        <p className="text-gray-600 text-sm mb-4">
                          Personal tasks and goals for your daily life and hobbies.
                        </p>
                        <div className="flex justify-between items-center">
                          <span className="text-xs text-gray-500">5 tasks</span>
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            Active
                          </span>
                        </div>
                      </div>

                      {/* Work Project Card */}
                      <div
                        className="bg-white shadow rounded-lg p-6 border border-gray-200 hover:shadow-md transition-shadow cursor-pointer"
                        onClick={() => setSelectedProject({
                          name: 'Work',
                          description: 'Professional tasks and projects related to your job.',
                          tasks: 12,
                          status: 'In Progress',
                          icon: 'briefcase',
                          color: 'blue'
                        })}
                      >
                        <div className="flex items-center mb-4">
                          <div className="p-2 bg-blue-100 rounded-md">
                            <svg className="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                          </div>
                          <h3 className="text-lg font-semibold text-gray-900 ml-3">Work</h3>
                        </div>
                        <p className="text-gray-600 text-sm mb-4">
                          Professional tasks and projects related to your job.
                        </p>
                        <div className="flex justify-between items-center">
                          <span className="text-xs text-gray-500">12 tasks</span>
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                            In Progress
                          </span>
                        </div>
                      </div>

                      {/* Learning Project Card */}
                      <div
                        className="bg-white shadow rounded-lg p-6 border border-gray-200 hover:shadow-md transition-shadow cursor-pointer"
                        onClick={() => setSelectedProject({
                          name: 'Learning',
                          description: 'Educational tasks and skill development activities.',
                          tasks: 8,
                          status: 'Active',
                          icon: 'book',
                          color: 'purple'
                        })}
                      >
                        <div className="flex items-center mb-4">
                          <div className="p-2 bg-purple-100 rounded-md">
                            <svg className="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                            </svg>
                          </div>
                          <h3 className="text-lg font-semibold text-gray-900 ml-3">Learning</h3>
                        </div>
                        <p className="text-gray-600 text-sm mb-4">
                          Educational tasks and skill development activities.
                        </p>
                        <div className="flex justify-between items-center">
                          <span className="text-xs text-gray-500">8 tasks</span>
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            Active
                          </span>
                        </div>
                      </div>

                      {/* Side Hustle Project Card */}
                      <div
                        className="bg-white shadow rounded-lg p-6 border border-gray-200 hover:shadow-md transition-shadow cursor-pointer"
                        onClick={() => setSelectedProject({
                          name: 'Side Hustle',
                          description: 'Entrepreneurial projects and side business ventures.',
                          tasks: 3,
                          status: 'Planned',
                          icon: 'lightning',
                          color: 'yellow'
                        })}
                      >
                        <div className="flex items-center mb-4">
                          <div className="p-2 bg-yellow-100 rounded-md">
                            <svg className="h-6 w-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                            </svg>
                          </div>
                          <h3 className="text-lg font-semibold text-gray-900 ml-3">Side Hustle</h3>
                        </div>
                        <p className="text-gray-600 text-sm mb-4">
                          Entrepreneurial projects and side business ventures.
                        </p>
                        <div className="flex justify-between items-center">
                          <span className="text-xs text-gray-500">3 tasks</span>
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                            Planned
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Project Detail Panel */}
                    {selectedProject && (
                      <div className="ml-6 w-96 bg-white border border-gray-200 rounded-lg p-6 shadow-lg">
                        <div className="flex justify-between items-start mb-4">
                          <div>
                            <h3 className="text-xl font-bold text-gray-900">{selectedProject.name}</h3>
                            <p className="text-sm text-gray-500 mt-1">{selectedProject.status}</p>
                          </div>
                          <button
                            onClick={() => setSelectedProject(null)}
                            className="text-gray-400 hover:text-gray-600"
                          >
                            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            </svg>
                          </button>
                        </div>

                        <p className="text-gray-600 mb-6">{selectedProject.description}</p>

                        <div className="mb-6">
                          <h4 className="font-medium text-gray-900 mb-3">Overview</h4>
                          <div className="grid grid-cols-2 gap-4">
                            <div className="bg-gray-50 rounded-lg p-3">
                              <p className="text-sm text-gray-500">Tasks</p>
                              <p className="text-lg font-semibold text-gray-900">{selectedProject.tasks}</p>
                            </div>
                            <div className="bg-gray-50 rounded-lg p-3">
                              <p className="text-sm text-gray-500">Progress</p>
                              <p className="text-lg font-semibold text-gray-900">45%</p>
                            </div>
                          </div>
                        </div>

                        <div className="mb-6">
                          <h4 className="font-medium text-gray-900 mb-3">Recent Tasks</h4>
                          <div className="space-y-2">
                            <div className="p-2 bg-gray-50 rounded-md">
                              <p className="text-sm text-gray-600">No tasks scheduled yet</p>
                            </div>
                          </div>
                        </div>

                        <div className="pt-4 border-t border-gray-200">
                          <p className="text-sm text-gray-600 italic">Tasks will be linked soon</p>
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="mt-8 bg-gray-50 rounded-lg p-4 border border-gray-200">
                    <h3 className="font-medium text-gray-800 mb-2">Create New Project</h3>
                    <p className="text-sm text-gray-600 mb-4">Organize your tasks into different categories for better productivity.</p>
                    <button className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50" disabled>
                      New Project
                    </button>
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