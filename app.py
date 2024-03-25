from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date
from models import Database
import os

app = Flask(__name__)               # Inicjalizacja aplikacji Flask

db = Database()                     # Inicjalizacja obiektu bazy danych
app.secret_key = os.urandom(24)     # Wygenerowanie secret key (klucza sesji)


# Utworzenie endpointów

# Endpoint do wyświetlenia strony głównej
@app.route('/', methods=["GET"])
def home():
    return render_template("index.html")

# Endpoint do wyświetlenia zadań z bazy danych


@app.route('/tasks', methods=["GET"])
def tasks():
    if request.method == "GET":
        tasks = db.get_task()
        return render_template("tasks.html", tasks=tasks, today=date.today())

# Endpoint do dodawania zadania do bazy danych


@app.route('/add_tasks', methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        name = request.form["task_name"]
        priority = request.form["task_priority"]
        if "is_completed" in request.form:
            completed = True
        else:
            completed = False
        task_date = request.form["task_date"]

        # Walidacja
        if not name or not task_date:
            flash("Task name and date are required.", "error")
            return redirect(url_for('add_task'))

        db.add_task(name, priority, completed, task_date)
        return redirect(url_for('tasks'))
    elif request.method == "GET":
        return render_template("add_tasks.html")

# Endpoint do usuwania wybranego zadania z bazy danych


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    db.delete_task(task_id)
    return redirect(url_for('tasks'))

# Endpoint do edycji wybranego zadania z bazy danych


@app.route('/update/<int:task_id>', methods=["GET", "POST"])
def update_task(task_id):
    if request.method == "POST":
        name = request.form["task_name"]
        priority = request.form["task_priority"]
        if "is_completed" in request.form:
            completed = True
        else:
            completed = False
        task_date = request.form["task_date"]

        # Walidacja
        if not name or not task_date:
            flash("Task name and date are required.", "error")
            return redirect(url_for('update_task', task_id=task_id))

        db.update_task(name, priority, completed, task_date, task_id)
        return redirect(url_for('tasks'))

    elif request.method == "GET":
        task = db.get_specified_task(task_id)
        return render_template("edit_task.html", task=task)


if __name__ == '__main__':
    app.run(debug=True)
