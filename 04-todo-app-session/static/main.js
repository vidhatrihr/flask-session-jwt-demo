const html = String.raw;

document.querySelector('#login-form').addEventListener('submit', handleLogin);
document.querySelector('#todo-form').addEventListener('submit', handleCreateTodo);

api('get', '/auth/whoami').then(data => {
  if (data.success) {
    document.querySelector('#auth-result').textContent = data.message;
  }
});

async function api(method, path, params = {}) {
  const options = {
    method: method,
  };
  let url;
  if (method == 'get') {
    const query = new URLSearchParams({
      ...params,
    }).toString();

    url = `http://127.0.0.1:5000${path}?${query}`;
  }

  if (method == 'post') {
    options.headers = {
      'Content-Type': 'application/json',
    };
    options.body = JSON.stringify(params);

    url = `http://127.0.0.1:5000${path}`;
  }

  const response = await fetch(url, options);
  const data = await response.json();

  if (data.success) {
    console.log(data);
  } else {
    console.error(data);
  }
  return data;
}

async function handleLogin(event) {
  event.preventDefault();

  const data = await api('post', '/auth/login', {
    email: document.querySelector('#email').value,
    password: document.querySelector('#password').value,
  });

  document.querySelector('#auth-result').textContent = data.message;
}

async function renderTodos(todos) {
  document.querySelector('#todos').innerHTML = '';

  for (let todo of todos) {
    document.querySelector('#todos').insertAdjacentHTML(
      'beforeend',
      html`
        <li>
          <span onclick="deleteTodo(${todo.id})">×</span>
          <span class="${todo.isDone ? 'done' : ''}" onclick="markDone(${todo.id})"
            >${todo.text}</span
          >
          <span class="${todo.isStarred ? 'star' : ''}" onclick="markStarred(${todo.id})"
            >${todo.isStarred ? '★' : '☆'}</span
          >
        </li>
      `
    );
  }
}

async function fetchTodos() {
  const data = await api('get', '/todo/list');

  renderTodos(data.payload.todos);
}

async function handleCreateTodo(event) {
  event.preventDefault();

  await api('post', '/todo/create', {
    text: document.querySelector('#todo-text').value,
  });

  fetchTodos();
}

async function markDone(todoId) {
  await api('get', '/todo/update', {
    todoId,
    action: 'markDone',
  });

  fetchTodos();
}

async function markStarred(todoId) {
  await api('get', '/todo/update', {
    todoId,
    action: 'markStarred',
  });

  fetchTodos();
}

async function deleteTodo(todoId) {
  await api('get', '/todo/delete', {
    todoId,
  });

  fetchTodos();
}
