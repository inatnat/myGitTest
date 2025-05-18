from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data store for demo purposes
tasks = [
    {"id": 1, "title": "Learn Flask", "completed": False},
    {"id": 2, "title": "Build a REST API", "completed": False}
]

# Get all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

# Get a specific task
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"task": task})

# Create a new task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        return jsonify({"error": "Title is required"}), 400
    
    new_task = {
        "id": tasks[-1]["id"] + 1 if tasks else 1,
        "title": request.json["title"],
        "completed": request.json.get("completed", False)
    }
    tasks.append(new_task)
    return jsonify({"task": new_task}), 201

# Update a task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    
    if not request.json:
        return jsonify({"error": "No data provided"}), 400
    
    task["title"] = request.json.get("title", task["title"])
    task["completed"] = request.json.get("completed", task["completed"])
    
    return jsonify({"task": task})

# Delete a task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    
    tasks.remove(task)
    return jsonify({"result": "Task deleted"})

if __name__ == '__main__':
    app.run(debug=True)
