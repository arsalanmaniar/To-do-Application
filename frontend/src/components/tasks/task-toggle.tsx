'use client';

import { useState } from 'react';
import { taskApi } from '@/lib/api/task-api';

interface TaskToggleProps {
  task: {
    id: number;
    title: string;
    completed: boolean;
  };
  onToggle: (updatedTask: any) => void;
}

export default function TaskToggle({ task, onToggle }: TaskToggleProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [localCompleted, setLocalCompleted] = useState(task.completed);

  const toggleCompletion = async () => {
    setIsLoading(true);

    try {
      // Optimistically update the UI
      const newCompletedState = !localCompleted;
      setLocalCompleted(newCompletedState);

      // Call the API to update the task
      const updatedTask = await taskApi.toggleTaskCompletion(task.id, newCompletedState);

      // Notify parent component of the update
      onToggle(updatedTask);
    } catch (error) {
      console.error('Error toggling task completion:', error);
      // Revert the optimistic update on error
      setLocalCompleted(task.completed);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      onClick={toggleCompletion}
      disabled={isLoading}
      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
        localCompleted ? 'bg-green-600' : 'bg-gray-200'
      } disabled:opacity-50`}
      aria-label={localCompleted ? 'Mark task as pending' : 'Mark task as complete'}
    >
      <span
        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
          localCompleted ? 'translate-x-6' : 'translate-x-1'
        }`}
      />
      <span className="sr-only">{localCompleted ? 'Completed' : 'Pending'}</span>
    </button>
  );
}