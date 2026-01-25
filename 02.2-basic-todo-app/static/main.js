const html = String.raw;

async function loadTodos() {
  const response = await fetch('http://127.0.0.1:5000/todo/list');
  const todos = await response.json();

  document.querySelector('#todo-list').innerHTML = '';

  todos.forEach(todo => {
    document.querySelector('#todo-list').insertAdjacentHTML(
      'beforeend',
      html`<li>
        ${todo.idStarred ? '⭐ ' : ''}
        <span class="${todo.isDone ? 'done' : ''}">${todo.text}</span>
        <button onclick="markDone(${todo.id})">done</button>
        <button onclick="markStarred(${todo.id})">star</button>
        <button onclick="deleteTodo(${todo.id})">delete</button>
      </li>`,
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

async function deleteTodo(todoId) {
  await fetch(`http://127.0.0.1:5000/todo/delete/${todoId}`);
  loadTodos();
}

async function markDone(todoId) {
  await fetch(`/todo/update/${todoId}?action=markDone`);
  loadTodos();
}

async function markStarred(todoId) {
  await fetch(`/todo/update/${todoId}?action=markStarred`);
  loadTodos();
}

loadTodos();
