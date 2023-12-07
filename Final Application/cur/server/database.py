import sqlite3
from datetime import datetime


class CommandDatabase:
    def __init__(self, database_path="audio_commands.db"):
        self.database_path = database_path

    def __enter__(self):
        self.connection = sqlite3.connect(self.database_path)
        self.create_commands_table()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.connection.close()

    def create_commands_table(self):
        try:
            cursor = self.connection.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command_text TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            ''')

        except Exception as e:
            print(f"Error creating commands table: {str(e)}")

    def log_command(self, command):
        try:
            cursor = self.connection.cursor()

            cursor.execute('''
                INSERT INTO commands (command_text, timestamp)
                VALUES (?, ?)
            ''', (command, str(datetime.now())))

        except Exception as e:
            print(f"Error logging command: {str(e)}")

    def list_commands(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM commands")
            commands = cursor.fetchall()
            return commands

        except Exception as e:
            print(f"Error listing commands: {str(e)}")
            return f"Error listing commands: {str(e)}"