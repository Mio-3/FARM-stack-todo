import axios from 'axios';

const baseURL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: baseURL,
  headers: {
    'Context-Type': "application/json",
  },
});

export interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
}

export interface CreateTodo {
  title: string;
  description?: string;
  completed: boolean;
}

export const TodoAPI = {
  getAllTodos: async () => {
    const response = await api.get<Todo[]>('/todos/');
    return response.data;
  },

  createTodo: async (input: CreateTodo) => {
    const response = await api.post<Todo>('/todos', input);
    return response.data;
  },

  getTodo: async (id: string) => {
    const response = await api.get<Todo>(`/todos/${id}`);
    return response.data;
  },

  updateTodo: async (id: string, input: Partial<CreateTodo>) => {
    const response = await api.put<Todo>(`/todos/${id}`, input);
    return response.data;
  },

  deleteTodo: async (id: string) => {
    await api.delete(`/todos/${id}`);
  }
}