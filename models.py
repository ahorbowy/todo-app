import mysql.connector
from config import DB_CONFIG

# Klasa reprezentująca pojedyncze zadanie


class Task():
    def __init__(self, id, name, priority, completed, date):
        self.id = id
        self.name = name
        self.priority = priority
        self.completed = completed
        self.date = date if date else None

# Klasa obsługująca połaczenie z bazą danych


class Database():
    # Inicjalizacja połaczenia z bazą danych
    def __init__(self):
        self.mydb = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.mydb.cursor()
    # Metoda do pobierania zadań z bazy danych

    def get_task(self):
        self.cursor.execute("SELECT * FROM tasks")
        tasks = []
        for row in self.cursor.fetchall():
            task = Task(row[0], row[1], row[2], row[3], row[4])
            tasks.append(task)
        return tasks

    # Metoda do dodawania zadania do bazy danych

    def add_task(self, name, priority, completed, date):
        self.cursor.execute(
            "INSERT INTO tasks (task_name, task_priority, is_completed, task_date) VALUES (%s, %s, %s, %s)", (name, priority, completed, date))
        self.mydb.commit()

    # Metoda do usuwania zadania z bazy danych

    def delete_task(self, id):
        self.cursor.execute(
            "DELETE FROM tasks WHERE id = %s", (id,))
        self.mydb.commit()

    # Metoda do edycji zadania w bazie danych

    def update_task(self, name, priority, completed, date, id):
        self.cursor.execute(
            "UPDATE tasks SET task_name=%s, task_priority=%s, is_completed=%s, task_date=%s WHERE id = %s", (name, priority, completed, date, id))
        self.mydb.commit()

    # Metoda do pobrania konkretnego zadania z bazy danych
    def get_specified_task(self, id):
        self.cursor.execute("SELECT * FROM tasks where id = %s", (id,))
        task_id, task_name, task_priority, task_completed, task_date = self.cursor.fetchone()
        task = Task(task_id, task_name, task_priority,
                    task_completed, task_date)
        return task

    # Metoda zamykająca połączenie z bazą danych
    def close(self):
        self.cursor.close()
        self.mydb.close()
