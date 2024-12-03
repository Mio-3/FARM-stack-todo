import { Todo } from "../api/api";
import { useTodoStore } from "../stores/todoStore";

interface TodoItemProps {
  todo: Todo;
}

export const TodoItem = ({ todo }: TodoItemProps) => {
  const { updateTodo, deleteTodo } = useTodoStore();

  const handleToggle = async () => {
    updateTodo(todo.id, { completed: !todo.completed });
  };

  const handleDelete = async () => {
    deleteTodo(todo.id);
  };

  return (
    <div className="flex items-center justify-between p-4 bg-white rounded-lg shadow">
      <div className="flex items-center space-x-4">
        <input type="checkbox" checked={todo.completed} onChange={handleToggle} className="h-4 w-4" />
        <div>
          <h3 className={`text-lg ${todo.completed ? "line-through text-gray-500" : ""}`}>{todo.title}</h3>
          {todo.description && <p className="text-gray-600">{todo.description}</p>}
        </div>
      </div>
      <button onClick={handleDelete} className="text-red-500 hover:text-red-700">
        削除
      </button>
    </div>
  );
};
