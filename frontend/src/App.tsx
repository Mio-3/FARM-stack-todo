import { AddTodoForm } from "./components/AddTodoForm";
import { TodoList } from "./components/TodoList";


function App() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <h1 className="text-3xl font-bold mb-8">Todo App</h1>
      <AddTodoForm />
      <TodoList />
    </div>
  );
}

export default App;