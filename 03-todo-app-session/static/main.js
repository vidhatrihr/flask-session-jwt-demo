const html = String.raw;

let sessionId = localStorage.getItem('sessionId');
let token = localStorage.getItem('token');

if (sessionId && token) {
  document.querySelector('#auth-result').textContent = 'already logged in';
}

document.querySelector('form').addEventListener('submit', handleLogin);

async function handleLogin(event) {
  event.preventDefault();

  const response = await fetch('http://127.0.0.1:5000/auth/login', {
    method: 'post',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: document.querySelector('#email').value,
      password: document.querySelector('#password').value,
    }),
  });

  const data = await response.json();

  if (data.success) {
    console.log(data);
    sessionId = data.payload.sessionId;
    token = data.payload.token;
    localStorage.setItem('sessionId', sessionId);
    localStorage.setItem('token', token);
  } else {
    console.error(data);
  }
  document.querySelector('#auth-result').textContent = data.message;
}

async function markDone(id) {
  const res = await fetch(
    `http://127.0.0.1:5000/todo/update?todo_id=${id}&action=mark_done&session_id=${sessionId}&token=${token}`
  );
  const data = await res.json();

  if (data.success) {
    console.log(data);
  } else {
    console.error(data);
  }

  fetchTodos();
}

async function fetchTodos() {
  const response = await fetch(
    `http://127.0.0.1:5000/todo/list?session_id=${sessionId}&token=${token}`
  );
  const data = await response.json();

  if (data.success) {
    console.log(data);
  }

  renderTodos(data.payload.todos);
}

function renderTodos(todos) {
  document.querySelector('#todos').innerHTML = '';
  for (let todo of todos) {
    document.querySelector('#todos').insertAdjacentHTML(
      'beforeend',
      html`
        <li>
          <span class="${todo.isDone ? 'done' : 'empty'}" onclick="markDone(${todo.id})"
            >${todo.text}</span
          >
        </li>
      `
    );
  }
}
