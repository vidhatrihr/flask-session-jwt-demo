# Flask Session and JWT Authentication Demo

This is a demo that I created for understanding and implementing various authentication and session management techniques in Flask. It features a series of progressively complex demo applications, starting from a basic, unauthenticated setup and culminating in a secure to-do application using JSON Web Tokens (JWT).

## Learning Objectives

These are my learning objectives while I was doing these demonstrations:

- The fundamentals of web authentication and session management.
- The differences between session-based and token-based authentication.
- How to implement session-based authentication in Flask using server-side storage.
- The security risks associated with different session management strategies.
- How to use HTTP-only cookies to securely store session information.
- The principles of JSON Web Tokens (JWT) and how to implement them from scratch.
- How to build a stateless authentication system using JWT.
- Understanding the bytes data structure.
- Understanding ASCII character set.
- Understanding Base64.

## Notebooks

This is just me exploring concepts.

- **`base64-implementation.ipynb`**: A from-scratch implementation of Base64 encoding and decoding, a fundamental component of JWT.
- **`jwt-implementation.ipynb`**: A detailed, from-scratch implementation of JWT, including token creation, signing, and verification.
- **`bytes-data-type.ipynb`**: An exploration of Python's `bytes` data type, which is essential for cryptographic operations in JWT.

---

## Demo Applications

### 1. Launch Missile (Basic Session-Based Authentication)

- **Folder:** `01-launch-missile-session`
- **Description:** This simple application demonstrates the necessity of authentication for protecting sensitive actions. It features a basic login system and a "launch missile" button that is only accessible to authenticated users.
- **Authentication:** This application uses a basic form of session-based authentication. Upon successful login, a unique session token is generated and stored in the database along with the user's ID. This token is then sent to the client, which must include it in the query parameters of subsequent requests to authenticate.
- **Security Note:** This implementation is **not secure** for production environments. Exposing the session token in the URL makes it vulnerable to being intercepted or logged, which could lead to unauthorized access.
- **Key Files:**
  - `app.py`: Contains the main Flask application logic, including the login and "launch missile" routes.
  - `templates/index.html`: The simple HTML page with the login form and the "launch missile" button.

### 2. Basic To-Do App (No Authentication)

This application serves as a baseline for the more advanced to-do applications. It is provided in two versions to illustrate different approaches to in-memory data management.

#### Version 2.1

- **Folder:** `02.1-basic-todo-app`
- **Description:** A minimal to-do application with no authentication or database. To-do items are stored in a simple Python list in memory.
- **Functionality:** List, create, and delete to-do items.

#### Version 2.2

- **Folder:** `02.2-basic-todo-app`
- **Description:** An improved version of the basic to-do app that uses a `Todo` class to represent to-do items and a dictionary to store them. This version demonstrates a more structured approach to data management, with the `Todo` class handling the auto-incrementing of IDs.
- **Functionality:** Same as version 2.1.

### 3. To-Do App with Session (Local Storage)

- **Folder:** `03-todo-app-session-ls`
- **Description:** This application introduces session-based authentication to the to-do app. After a successful login, the session details (session ID and token) are sent to the client and stored in the browser's local storage.
- **Authentication:** For each subsequent request, the client sends the session details in the query parameters (for GET requests) or the JSON request body (for POST requests). The server then validates these details against the database to authenticate the user.
- **Security Note:** This approach has security vulnerabilities. Storing session information in local storage makes it accessible to any script running on the page (XSS vulnerability), and passing session details in query parameters exposes them in the URL.
- **Key Files:**
  - `routes.py`: Defines the application's routes, including login, logout, and to-do CRUD operations.
  - `decorators.py`: Contains the `login_required` decorator, which protects routes that require authentication.
  - `utils.py`: Includes utility functions, such as `validate_session`, which is responsible for authenticating the user.

### 4. To-Do App with Session (Cookies)

- **Folder:** `04-todo-app-session-cookies`
- **Description:** This application enhances the previous to-do app by using HTTP-only cookies to store session information, which is a more secure approach than using local storage.
- **Authentication:** Upon successful login, the server sets the `sessionId` and `token` as HTTP-only cookies in the user's browser. These cookies are automatically and securely sent with every subsequent request, and the server validates them to authenticate the user.
- **Features:**
  - **Secure Session Management:** HTTP-only cookies are not accessible to client-side scripts, which helps to mitigate XSS attacks.
  - **Logout:** The application includes a logout feature that deletes the user's session from the database.
  - **Logout Everywhere:** This feature invalidates all active sessions for a user, which is useful for security purposes.
- **Key Files:**
  - `routes.py`: Includes the login, logout, and "logout everywhere" routes.
  - `utils.py`: The `validate_session` function is updated to read the session information from the request cookies.

### 5. To-Do App with JWT

- **Folder:** `05-todo-app-jwt`
- **Description:** This is the most advanced version of the to-do app, implementing a stateless authentication system using JSON Web Tokens (JWT). This approach eliminates the need for server-side session storage.
- **Authentication:** After a successful login, the server generates a JWT that contains the user's ID and an "issued at" timestamp. This JWT is then sent to the client as an HTTP-only cookie. For every subsequent request, the server decodes and verifies the JWT to authenticate the user.
- **Features:**
  - **Stateless Authentication:** The server does not need to store session information, making the application more scalable.
  - **Custom JWT Implementation:** The JWT functionality is implemented from scratch in `jwt.py`, providing a clear understanding of how JWTs work.
  - **Token Expiration:** The application includes a mechanism to expire tokens after a certain period, which is a crucial security feature for JWT-based authentication.
- **Key Files:**
  - `jwt.py`: Contains the from-scratch implementation of JWT encoding, decoding, and verification.
  - `decorators.py`: The `login_required` decorator is updated to use the `verify_jwt` function to authenticate users.
  - `routes.py`: The login route is modified to generate and set the JWT cookie.

---

## Technologies Used

- **Backend:** Flask, Flask-SQLAlchemy
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **Authentication:**
  - Session-based authentication (server-side storage)
  - Token-based authentication (JWT)

## How to Run the Applications

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/vidhatrihr/flask-session-jwt-demo.git
    ```
2.  **Install the required dependencies:**
    ```bash
    pip install Flask Flask-SQLAlchemy
    ```
3.  **Navigate to the desired application's directory:**
    ```bash
    cd flask-session-jwt-demo/01-launch-missile-session
    ```
4.  **Run the application:**
    ```bash
    python app.py
    ```

Each application is self-contained and can be run independently. Please refer to the source code for more detailed implementation information.
