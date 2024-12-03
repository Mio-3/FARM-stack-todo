import { create } from 'zustand';
import { Todo, CreateTodo, TodoAPI } from '../api/api';

interface TodoStore {
  todos: Todo[];
  isLoading: boolean;
  error: string | null;
  fetchTodos: () => Promise<void>;
  addTodo: (input: CreateTodo) => Promise<void>;
  updateTodo: (id: string, input: Partial<CreateTodo>) => Promise<void>;
  deleteTodo: (id: string) => Promise<void>;
}

export const useTodoStore = create<TodoStore>((set, get) => ({
  todos: [],
  isLoading: false,
  error: null,
  
  fetchTodos: async () => {
    set({ isLoading: true, error: null });
    try {
      const todos = await TodoAPI.getAllTodos();
      set({ todos });
    } catch (error) {
      set({ error: 'Todoの取得に失敗しました' });
    } finally {
      set({ isLoading: false });
    }
  },

  addTodo: async (input: CreateTodo) => {
    try {
      const newTodo = await TodoAPI.createTodo(input);
      set(state => ({ todos: [...state.todos, newTodo] }));
    } catch (error) {
      set({ error: 'Todoの作成に失敗しました' });
    }
  },

  updateTodo: async (id: string, input: Partial<CreateTodo>) => {
    try {
      const updatedTodo = await TodoAPI.updateTodo(id, input);
      set(state => ({
        todos: state.todos.map(todo => 
          todo.id === id ? updatedTodo : todo
        )
      }));
    } catch (error) {
      set({ error: 'Todoの更新に失敗しました' });
    }
  },

  deleteTodo: async (id: string) => {
    try {
      await TodoAPI.deleteTodo(id);
      set(state => ({
        todos: state.todos.filter(todo => todo.id !== id)
      }));
    } catch (error) {
      set({ error: 'Todoの削除に失敗しました' });
    }
  }
}));