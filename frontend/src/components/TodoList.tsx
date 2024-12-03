import { useEffect } from "react";
import { useTodoStore } from "../stores/todoStore";
import { TodoItem } from "./TodoItem";


export const TodoList = () => {
  const { todos, isLoading, error, fetchTodos } = useTodoStore();

  useEffect(() => {
    fetchTodos();
  }, []);

  if (isLoading) return <div>Loading ..</div>
  if (error) return <div>Error: {error}</div>
  if (!todos) return <div>No todos found</div>;

  return (
    <div className=" space-x-4">
      {Array.isArray(todos) && todos.map((todo) => (
        <TodoItem key={todo.id} todo={todo} />
      ))}
    </div>
  )
  
  
}