# backend_app.py
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

# --- Database Setup ---
DATABASE = 'todolist.db'

def get_db():
    """
    Connects to the specific database.
    Creates the 'tasks' table if it doesn't exist.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # Return rows as dictionary-like objects
    # Create table if it doesn't exist
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            done BOOLEAN NOT NULL CHECK (done IN (0, 1)) DEFAULT 0
        )
    ''')
    conn.commit()
    return conn

def close_connection(exception=None):
    """Closes the database connection."""
    # This function is typically used with app.teardown_appcontext
    # For simplicity here, we'll manage connections within each route
    pass

# --- Flask App Setup ---
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes, allowing frontend requests

# --- API Routes ---

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Retrieve all tasks from the database."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, description, done FROM tasks ORDER BY id")
        tasks_list = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(tasks_list)
    except Exception as e:
        print(f"Error getting tasks: {e}")
        return jsonify({"error": "Failed to retrieve tasks"}), 500

@app.route('/tasks', methods=['POST'])
def add_task():
    """Add a new task to the database."""
    if not request.json or not 'description' in request.json:
        return jsonify({"error": "Missing 'description' in request body"}), 400

    description = request.json['description']
    if not description: # Basic validation
         return jsonify({"error": "'description' cannot be empty"}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (description, done) VALUES (?, ?)", (description, 0))
        conn.commit()
        new_task_id = cursor.lastrowid
        conn.close()
        # Return the newly created task
        return jsonify({"id": new_task_id, "description": description, "done": False}), 201
    except Exception as e:
        print(f"Error adding task: {e}")
        return jsonify({"error": "Failed to add task"}), 500

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task by its ID."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        # Check if task exists before deleting
        cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        if task is None:
            conn.close()
            return jsonify({"error": "Task not found"}), 404

        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Task deleted successfully"}), 200 # Or 204 No Content
    except Exception as e:
        print(f"Error deleting task {task_id}: {e}")
        return jsonify({"error": "Failed to delete task"}), 500

# Optional: Route to update task status (mark as done/undone)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task's status (e.g., mark as done)."""
    if not request.json or 'done' not in request.json:
        return jsonify({"error": "Missing 'done' field in request body"}), 400

    try:
        done_status = bool(request.json['done']) # Convert to boolean
        conn = get_db()
        cursor = conn.cursor()

        # Check if task exists
        cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        if task is None:
            conn.close()
            return jsonify({"error": "Task not found"}), 404

        cursor.execute("UPDATE tasks SET done = ? WHERE id = ?", (done_status, task_id))
        conn.commit()

        # Fetch the updated task to return it
        cursor.execute("SELECT id, description, done FROM tasks WHERE id = ?", (task_id,))
        updated_task = dict(cursor.fetchone())
        conn.close()

        return jsonify(updated_task), 200
    except Exception as e:
        print(f"Error updating task {task_id}: {e}")
        return jsonify({"error": "Failed to update task"}), 500


# --- Run the App ---
if __name__ == '__main__':
    # Ensure the database and table exist before starting
    with app.app_context():
        get_db()
    # Run on localhost, port 5000
    # Use host='0.0.0.0' to make it accessible on your network
    app.run(debug=True, host='0.0.0.0', port=5500)
