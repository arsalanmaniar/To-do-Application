'use client';

import { useState } from 'react';
import TaskDetail from './task-detail';
import TaskToggle from './task-toggle';
import TaskDeleteModal from './task-delete-modal';

interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: string;
  userId?: string;
}

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated?: (updatedTask: Task) => void;
  onTaskDeleted?: (deletedTaskId: number) => void;
  loading?: boolean;
}

export default function TaskList({ tasks, onTaskUpdated, onTaskDeleted, loading }: TaskListProps) {
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [deletingTask, setDeletingTask] = useState<Task | null>(null);

  const handleUpdateTask = (updatedTask: Task) => {
    setEditingTask(null);
    if (onTaskUpdated) {
      onTaskUpdated(updatedTask);
    }
  };

  const handleDeleteTask = (deletedTaskId: number) => {
    if (onTaskDeleted) {
      onTaskDeleted(deletedTaskId);
    }
  };

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, index) => (
          <div
            key={index}
            className="border rounded-lg p-4 bg-white border-gray-200 animate-pulse"
          >
            <div className="flex items-start">
              <div className="flex-1 min-w-0">
                <div className="h-5 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-1/4"></div>
              </div>
              <div className="ml-4 flex flex-col items-end space-y-2">
                <div className="flex space-x-2">
                  <div className="h-8 w-16 bg-gray-200 rounded"></div>
                  <div className="h-8 w-16 bg-gray-200 rounded"></div>
                </div>
                <div className="h-5 w-10 bg-gray-200 rounded-full"></div>
                <div className="h-5 w-20 bg-gray-200 rounded-full"></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <div
          key={task.id}
          className={`border rounded-lg p-4 transition-all duration-200 ${
            task.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200 hover:shadow-sm'
          }`}
        >
          {editingTask?.id === task.id ? (
            <TaskDetail
              task={task}
              onUpdate={handleUpdateTask}
              onCancel={() => setEditingTask(null)}
            />
          ) : (
            <div className="flex items-start">
              <div className="flex-1 min-w-0">
                <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                  {task.title}
                </h3>
                {task.description && (
                  <p className="mt-1 text-sm text-gray-500">{task.description}</p>
                )}
                <p className="mt-2 text-xs text-gray-400">
                  Created: {new Date(task.createdAt).toLocaleDateString()}
                </p>
              </div>
              <div className="ml-4 flex flex-col items-end space-y-2">
                <div className="flex space-x-2">
                  <button
                    onClick={() => setEditingTask(task)}
                    className="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => setDeletingTask(task)}
                    className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors duration-200"
                  >
                    Delete
                  </button>
                </div>
                <TaskToggle
                  task={task}
                  onToggle={(updatedTask) => {
                    if (onTaskUpdated) {
                      onTaskUpdated(updatedTask);
                    }
                  }}
                />
                <span
                  className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    task.completed
                      ? 'bg-green-100 text-green-800'
                      : 'bg-yellow-100 text-yellow-800'
                  }`}
                >
                  {task.completed ? 'Completed' : 'Pending'}
                </span>
              </div>
            </div>
          )}
        </div>
      ))}

      {tasks.length === 0 && !loading && (
        <div className="text-center py-12">
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
        </div>
      )}

      {deletingTask && (
        <TaskDeleteModal
          task={deletingTask}
          isOpen={!!deletingTask}
          onClose={() => setDeletingTask(null)}
          onDelete={handleDeleteTask}
        />
      )}
    </div>
  );
}