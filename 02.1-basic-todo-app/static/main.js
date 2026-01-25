const html = String.raw;

async function loadTodos() {
  const response = await fetch('http://127.0.0.1:5000/todo/list');
  const todos = await response.json();

  document.querySelector('#todo-list').innerHTML = '';

  todos.forEach((text, index) => {
    document
      .querySelector('#todo-list')
      .insertAdjacentHTML(
        'beforeend',
        html`<li>${text} <button onclick="deleteTodo(${index})">delete</button></li>`,
      );
  });
}

document.querySelector('form').addEventListener('submit', createTodo);

async function createTodo(event) {
  event.preventDefault();

  await fetch('/todo/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text: document.querySelector('#todo-input').value,
    }),
  });

  loadTodos();
}

async function deleteTodo(index) {
  await fetch(`http://127.0.0.1:5000/todo/delete/${index}`);
  loadTodos();
}

loadTodos();
