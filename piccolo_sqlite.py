from piccolo.columns import Boolean, Varchar
from piccolo.engine.sqlite import SQLiteEngine
from piccolo.table import Table, create_tables

DB = SQLiteEngine("todo.sqlite")


class Todo(Table, db=DB):
    name = Varchar()
    completed = Boolean(default=False)
