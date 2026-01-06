from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

todos = ['task', 'learn app dev', 'meditate']


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
  return jsonify({'message': 'Todos created'})


@app.route('/todo/delete/<int:index>')
def delete_todo(index):
  todos.pop(index)
  return jsonify({'message': 'Todo deleted'})


if __name__ == '__main__':
  app.run(debug=True)
