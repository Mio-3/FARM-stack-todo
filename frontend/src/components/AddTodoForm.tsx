import { useState } from "react";
import { useTodoStore } from "../stores/todoStore";


export const AddTodoForm = () => {
  const [ title, setTitle ] = useState('');
  const [ description, setDescription ] = useState('');
  const { addTodo } = useTodoStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    await addTodo({
      title,
      description: description.trim(),
      completed: false,
    });

    setTitle('');
    setDescription('');
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 mb-8">
      <div>
        <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="タスクを入力"
            className="w-full p-2 border rounded"
            required
          />
      </div>
      <div>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="詳細を入力（任意）"
          className="w-full p-2 border rounded"
          rows={3}
        />
      </div>
      <button
        type="submit"
        className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
      >
        追加
      </button>
    </form>
  );
};