const html = String.raw;

async function loadTodos() {
  const response = await fetch('http://127.0.0.1:5000/todo/list');
  const todos = await response.json();

  document.querySelector('#todo-list').innerHTML = '';

  todos.forEach(todo => {
    document
      .querySelector('#todo-list')
      .insertAdjacentHTML(
        'beforeend',
        html`<li>${todo.text} <button onclick="deleteTodo(${todo.id})">del</button></li>`,
      );
  });
}

document.querySelector('form').addEventListener('submit', createTodo);

async function createTodo(event) {
  event.preventDefault();

  const input = document.querySelector('#todo-input');
  const text = input.value;

  if (text == '') return;

  await fetch('/todo/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text,
    }),
  });

  input.value = '';
  loadTodos();
}

async function deleteTodo(todoId) {
  await fetch(`http://127.0.0.1:5000/todo/delete/${todoId}`);
  loadTodos();
}

loadTodos();
