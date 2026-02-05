import apiClient from './client';
import { AxiosError } from 'axios';

// Task API service for handling task-related API calls
export const taskApi = {
  /**
   * Get all tasks for the current user
   * @returns Promise resolving to array of tasks
   */
  async getTasks(params?: { completed?: boolean; limit?: number; offset?: number }) {
    try {
      // Build query string from parameters, handling types appropriately
      const queryParams = new URLSearchParams();

      if (params?.completed !== undefined) {
        queryParams.append('completed', params.completed.toString());
      }

      if (params?.limit !== undefined) {
        queryParams.append('limit', params.limit.toString());
      }

      if (params?.offset !== undefined) {
        queryParams.append('offset', params.offset.toString());
      }

      const queryString = queryParams.toString();
      const url = `/api/v1/tasks${queryString ? '?' + queryString : ''}`;

      const response = await apiClient.get(url);
      // The backend returns a TaskListResponse object with tasks array inside
      // Extract the tasks array to match what the frontend components expect
      return response.data.tasks || response.data;
    } catch (error) {
      console.error('Get tasks API error:', error);
      // Log more details about the error
      const axiosError = error as AxiosError;
      if (axiosError.response) {
        console.error('Response data:', axiosError.response.data);
        console.error('Response status:', axiosError.response.status);
        console.error('Response headers:', axiosError.response.headers);
      } else if (axiosError.request) {
        console.error('Request data:', axiosError.request);
      } else {
        console.error('Error message:', axiosError.message);
      }
      throw error;
    }
  },

  /**
   * Get a specific task by ID
   * @param taskId - The ID of the task to retrieve
   * @returns Promise resolving to the task object
   */
  async getTask(taskId: number | string) {
    try {
      const response = await apiClient.get(`/api/v1/tasks/${taskId}`);
      return response.data;
    } catch (error) {
      console.error('Get task API error:', error);
      throw error;
    }
  },

  /**
   * Create a new task
   * @param taskData - Task data (title, description, etc.)
   * @returns Promise resolving to the created task
   */
  async createTask(taskData: { title: string; description?: string; completed?: boolean }) {
    try {
      // Prepare the payload ensuring it matches the backend schema
      const payload: any = {
        title: taskData.title
      };

      if (taskData.description != null && taskData.description.trim() !== '') {
        payload.description = taskData.description;
      }

      if (taskData.completed != null) {
        payload.completed = taskData.completed;
      }

      const response = await apiClient.post('/api/v1/tasks', payload);
      return response.data;
    } catch (error) {
      console.error('Create task API error:', error);
      throw error;
    }
  },

  /**
   * Update an existing task
   * @param taskId - The ID of the task to update
   * @param taskData - Updated task data
   * @returns Promise resolving to the updated task
   */
  async updateTask(taskId: number | string, taskData: Partial<{ title: string; description?: string; completed?: boolean }>) {
    try {
      // Prepare the payload ensuring it only includes provided fields
      const payload: any = {};

      if (taskData.title !== undefined) {
        payload.title = taskData.title;
      }

      if (taskData.description !== undefined) {
        payload.description = taskData.description;
      }

      if (taskData.completed !== undefined) {
        payload.completed = taskData.completed;
      }

      const response = await apiClient.put(`/api/v1/tasks/${taskId}`, payload);
      return response.data;
    } catch (error) {
      console.error('Update task API error:', error);
      throw error;
    }
  },

  /**
   * Delete a task
   * @param taskId - The ID of the task to delete
   * @returns Promise resolving when the task is deleted
   */
  async deleteTask(taskId: number | string) {
    try {
      const response = await apiClient.delete(`/api/v1/tasks/${taskId}`);
      return response.data;
    } catch (error) {
      console.error('Delete task API error:', error);
      throw error;
    }
  },

  /**
   * Toggle task completion status
   * @param taskId - The ID of the task to toggle
   * @param completed - The new completion status
   * @returns Promise resolving to the updated task
   */
  async toggleTaskCompletion(taskId: number | string, completed: boolean) {
    try {
      const response = await apiClient.patch(`/api/v1/tasks/${taskId}/complete`, {
        completed: Boolean(completed)
      });
      return response.data;
    } catch (error) {
      console.error('Toggle task completion API error:', error);
      throw error;
    }
  }
};

// Export individual functions for named imports
export const {
  getTasks,
  getTask,
  createTask,
  updateTask,
  deleteTask,
  toggleTaskCompletion
} = taskApi;
