const html = String.raw;

async function loadTodos() {
  const response = await fetch('http://127.0.0.1:5000/todo/list');
  const todos = await response.json();

  document.querySelector('#todo-list').innerHTML = '';

  todos.forEach((todo, index) => {
    document
      .querySelector('#todo-list')
      .insertAdjacentHTML(
        'beforeend',
        html`<li>${todo} <button onclick="deleteTodo(${index})">del</button></li>`,
      );
  });
}

document.querySelector('form').addEventListener('submit', createTodo);

async function createTodo(event) {
  event.preventDefault();

  const input = document.querySelector('#todo-input');
  const todo = input.value;

  if (todo == '') return;

  await fetch('/todo/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      todo,
    }),
  });

  input.value = '';
  loadTodos();
}

async function deleteTodo(index) {
  await fetch(`http://127.0.0.1:5000/todo/delete/${index}`);
  loadTodos();
}

loadTodos();
