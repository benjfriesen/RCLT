from pathlib import Path
import sqlite3

# working directories
working_dir = Path(__file__).parent.absolute()
db = working_dir.parent / 'db' / 'main.sqlite'

# connect to database
connection = sqlite3.connect(db)

# create a cursor
cursor = connection.cursor()


# execute query
try:
    cursor.execute("SELECT * FROM boards")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

# close the connection
finally:
    connection.close()