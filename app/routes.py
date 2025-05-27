import os
import uuid
from flask import current_app, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from app.models import Todo

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def register_routes(app):
    @app.route('/')
    def index():
        todos = []
        if app.db:
            try:
                # Query todos without ordering to avoid index requirement
                todos_ref = app.db.collection('todos').where('completed', '==', False)
                for doc in todos_ref.stream():
                    todo_data = doc.to_dict()
                    todo_data['id'] = doc.id
                    todos.append(Todo.from_dict(todo_data))
                
                # Sort in memory by created_at
                todos.sort(key=lambda x: x.created_at, reverse=True)
            except Exception as e:
                flash(f'Error fetching todos: {str(e)}', 'error')
        else:
            # Local development mode - show sample data
            flash('Running in local development mode', 'info')
        
        return render_template('index.html', todos=todos)

    @app.route('/todo/create', methods=['GET', 'POST'])
    def create_todo():
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            image_url = None
            
            # Handle image upload
            if 'image' in request.files:
                image = request.files['image']
                if image and allowed_file(image.filename):
                    filename = secure_filename(f"{uuid.uuid4()}_{image.filename}")
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image.save(image_path)
                    image_url = url_for('static', filename=f'uploads/{filename}')
            
            # Create todo
            todo = Todo(
                title=title,
                description=description,
                image_url=image_url
            )
            
            # Save to Firestore
            app.db.collection('todos').document(todo.id).set(todo.to_dict())
            
            flash('Task added successfully!', 'success')
            return redirect(url_for('index'))
        
        return render_template('create.html')

    @app.route('/todo/<id>')
    def view_todo(id):
        todo_doc = app.db.collection('todos').document(id).get()
        if todo_doc.exists:
            todo_data = todo_doc.to_dict()
            todo_data['id'] = todo_doc.id
            todo = Todo.from_dict(todo_data)
            return render_template('view.html', todo=todo)
        flash('Task not found', 'error')
        return redirect(url_for('index'))

    @app.route('/todo/<id>/edit', methods=['GET', 'POST'])
    def edit_todo(id):
        todo_doc = app.db.collection('todos').document(id).get()
        if not todo_doc.exists:
            flash('Task not found', 'error')
            return redirect(url_for('index'))
        
        todo_data = todo_doc.to_dict()
        todo_data['id'] = todo_doc.id
        todo = Todo.from_dict(todo_data)
        
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            completed = 'completed' in request.form
            image_url = todo.image_url
            
            # Handle image upload
            if 'image' in request.files:
                image = request.files['image']
                if image and allowed_file(image.filename):
                    filename = secure_filename(f"{uuid.uuid4()}_{image.filename}")
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image.save(image_path)
                    image_url = url_for('static', filename=f'uploads/{filename}')
            
            # Update todo
            todo.title = title
            todo.description = description
            todo.completed = completed
            todo.image_url = image_url
            
            # Save to Firestore
            app.db.collection('todos').document(id).update(todo.to_dict())
            
            flash('Task updated successfully!', 'success')
            # Redirect to the appropriate page based on task completion status
            if completed:
                return redirect(url_for('completed_tasks'))
            else:
                return redirect(url_for('index'))
        
        return render_template('edit.html', todo=todo)

    @app.route('/todo/<id>/delete', methods=['POST'])
    def delete_todo(id):
        # Check if the task is completed before deleting
        todo_doc = app.db.collection('todos').document(id).get()
        was_completed = False
        if todo_doc.exists:
            todo_data = todo_doc.to_dict()
            was_completed = todo_data.get('completed', False)
            
        app.db.collection('todos').document(id).delete()
        flash('Task deleted successfully!', 'success')
        
        # Redirect to the appropriate list
        if was_completed:
            return redirect(url_for('completed_tasks'))
        else:
            return redirect(url_for('index'))

    @app.route('/todo/<id>/toggle', methods=['POST'])
    def toggle_todo(id):
        todo_doc = app.db.collection('todos').document(id).get()
        if todo_doc.exists:
            todo_data = todo_doc.to_dict()
            completed = not todo_data.get('completed', False)
            app.db.collection('todos').document(id).update({'completed': completed})
            return jsonify({'completed': completed})
        return jsonify({'error': 'Task not found'}), 404
        
    @app.route('/completed')
    def completed_tasks():
        todos = []
        if app.db:
            try:
                # Query todos without ordering to avoid index requirement
                todos_ref = app.db.collection('todos').where('completed', '==', True)
                for doc in todos_ref.stream():
                    todo_data = doc.to_dict()
                    todo_data['id'] = doc.id
                    todos.append(Todo.from_dict(todo_data))
                
                # Sort in memory by created_at
                todos.sort(key=lambda x: x.created_at, reverse=True)
            except Exception as e:
                flash(f'Error fetching completed tasks: {str(e)}', 'error')
        
        return render_template('completed.html', todos=todos)