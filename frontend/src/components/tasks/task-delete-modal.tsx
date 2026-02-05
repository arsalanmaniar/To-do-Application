import { taskApi } from '@/lib/api/task-api';

interface TaskDeleteModalProps {
  task: {
    id: number;
    title: string;
  };
  isOpen: boolean;
  onClose: () => void;
  onDelete: (deletedTaskId: number) => void;
}

export default function TaskDeleteModal({ task, isOpen, onClose, onDelete }: TaskDeleteModalProps) {
  if (!isOpen) {
    return null;
  }

  const handleConfirmDelete = async () => {
    try {
      // Call the API to delete the task
      await taskApi.deleteTask(task.id);

      // Notify parent component that the task was deleted
      onDelete(task.id);

      // Close the modal
      onClose();
    } catch (error) {
      console.error('Error deleting task:', error);
      // In a real app, you might want to show an error message to the user
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Delete Task</h3>
        <p className="text-gray-600 mb-6">
          Are you sure you want to delete the task "{task.title}"? This action cannot be undone.
        </p>

        <div className="flex justify-end space-x-3">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={handleConfirmDelete}
            className="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}