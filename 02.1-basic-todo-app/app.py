from flask import Flask, render_template, jsonify, request

# ⚠️ There is no authentication in this app
app = Flask(__name__)

# ⚠️ There is no database in this app
todos = ['task', 'learn app dev', 'meditate']  # Collection of todo texts


@app.route('/')
def root():
  return render_template('index.html')


@app.route('/todo/list')
def get_todos():
  return jsonify(todos)


@app.route('/todo/create', methods=['POST'])
def create_todo():
  todo = request.json.get('todo')

  todos.append(todo)
  return jsonify({'message': 'Todo created'})


@app.route('/todo/delete/<int:index>')
def delete_todo(index):
  todos.pop(index)
  return jsonify({'message': 'Todo deleted'})


if __name__ == '__main__':
  app.run(debug=True)
