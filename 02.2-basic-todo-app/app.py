from flask import Flask, render_template, jsonify, request

# ⚠️ There is no authentication in this app
app = Flask(__name__)


class Todo:
  # ⚠️ There is no database in this app
  table = {}  # id -> todo objects
  next_id = 0  # id that should be assigned to next todo object

  def __init__(self, text):
    self.id = Todo.next_id
    self.text = text
    self.is_done = False
    self.id_starred = False

    Todo.next_id += 1  # id autoincrement
    Todo.table[self.id] = self  # Add to table, self refers to current object

  def dictify(self):
    return {
        "id": self.id,
        "text": self.text,
        "isDone": self.is_done,
        "idStarred": self.id_starred,
    }


# Create three objects, they will automatically be added to table
Todo('Task')
Todo('Learn app dev')
Todo('Meditate')


@app.route('/')
def root():
  return render_template('index.html')


@app.route('/todo/list')
def get_todos():
  return jsonify([
      todo.dictify() for todo in Todo.table.values()
  ])


@app.route('/todo/create', methods=['POST'])
def create_todo():
  text = request.json.get('text')

  Todo(text)  # Automatically added to table
  return jsonify({'message': 'Todo created'})


@app.route('/todo/update/<int:todo_id>')
def update_todo(todo_id):
  action = request.args.get('action')

  todo = Todo.table[todo_id]
  if action == 'markDone':
    todo.is_done = not todo.is_done
  elif action == 'markStarred':
    todo.id_starred = not todo.id_starred

  return jsonify({'message': 'Todo updated'})


@app.route('/todo/delete/<int:todo_id>')
def delete_todo(todo_id):
  del Todo.table[todo_id]
  return jsonify({'message': 'Todo deleted'})


if __name__ == '__main__':
  app.run(debug=True)
