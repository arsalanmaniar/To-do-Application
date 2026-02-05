'use client';

import { useState } from 'react';
import { taskApi } from '@/lib/api/task-api';

interface TaskDetailProps {
  task: {
    id: number;
    title: string;
    description?: string;
    completed: boolean;
    createdAt: string;
  };
  onUpdate: (updatedTask: any) => void;
  onCancel: () => void;
}

export default function TaskDetail({ task, onUpdate, onCancel }: TaskDetailProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [completed, setCompleted] = useState(task.completed);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSave = async () => {
    setLoading(true);
    setError(null);

    try {
      const updatedTask = await taskApi.updateTask(task.id, {
        title,
        description,
        completed
      });

      onUpdate(updatedTask);
      setIsEditing(false);
    } catch (err: any) {
      console.error('Error updating task:', err);
      setError(err.message || 'Failed to update task');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    // Revert to original values
    setTitle(task.title);
    setDescription(task.description || '');
    setCompleted(task.completed);
    setIsEditing(false);
    onCancel();
  };

  const toggleEditMode = () => {
    if (isEditing) {
      // Cancel editing and revert to original values
      setTitle(task.title);
      setDescription(task.description || '');
      setCompleted(task.completed);
    }
    setIsEditing(!isEditing);
  };

  return (
    <div className="border rounded-lg p-4 bg-white">
      {error && (
        <div className="rounded-md bg-red-50 p-4 mb-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">{error}</h3>
            </div>
          </div>
        </div>
      )}

      {isEditing ? (
        <div className="space-y-4">
          <div>
            <label htmlFor="task-title" className="block text-sm font-medium text-gray-700">
              Title
            </label>
            <input
              type="text"
              id="task-title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              disabled={loading}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>

          <div>
            <label htmlFor="task-description" className="block text-sm font-medium text-gray-700">
              Description
            </label>
            <textarea
              id="task-description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              disabled={loading}
              rows={3}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>

          <div className="flex items-center">
            <input
              id="task-completed"
              type="checkbox"
              checked={completed}
              onChange={(e) => setCompleted(e.target.checked)}
              disabled={loading}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label htmlFor="task-completed" className="ml-2 block text-sm text-gray-900">
              Completed
            </label>
          </div>

          <div className="flex space-x-3">
            <button
              onClick={handleSave}
              disabled={loading}
              className="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {loading ? 'Saving...' : 'Save'}
            </button>
            <button
              onClick={handleCancel}
              disabled={loading}
              className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div className="flex justify-between items-start">
            <div className="flex-1">
              <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className="mt-1 text-sm text-gray-500 whitespace-pre-wrap">{task.description}</p>
              )}
              <p className="mt-2 text-xs text-gray-400">
                Created: {new Date(task.createdAt).toLocaleDateString()}
              </p>
            </div>
            <div className="ml-4">
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

          <div className="mt-4 flex space-x-3">
            <button
              onClick={toggleEditMode}
              className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Edit
            </button>
            <button
              onClick={() => setCompleted(!completed)}
              className={`inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 ${
                completed
                  ? 'bg-yellow-600 hover:bg-yellow-700'
                  : 'bg-green-600 hover:bg-green-700'
              }`}
            >
              {completed ? 'Mark as Pending' : 'Mark as Complete'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}