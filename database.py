import base64

import psycopg2
import base64

stuff = b'SVpUM1Z2aFh3TXh3S0Q4MUh5b09RN01QYlVGQVN3SkU='

# establishing the connection
connection = psycopg2.connect(
    database="pygame_project",
    user='pygame_project_user',
    password=base64.b64decode(stuff).decode('ascii'),
    host='dpg-cgu20a02qv2fdeb7n9qg-a.frankfurt-postgres.render.com',
    port='5432'
)

# andmebaasi loomiseks
cursor = connection.cursor()

create_db = '''CREATE TABLE SCORES(
   NAME VARCHAR(255) NOT NULL,
   SCORE INT   
)'''

# cursor.execute(create_db)
# connection.commit()
# cursor.close()


def add_player(name, score):
    cursor = connection.cursor()
    script = "INSERT INTO SCORES(NAME, SCORE) VALUES (%s, %s)"
    cursor.execute(script, [name, score])
    connection.commit()
    cursor.close()


def query_data():
    cursor = connection.cursor()
    query = """SELECT * FROM SCORES ORDER BY SCORE DESC LIMIT 10;"""
    cursor.execute(query)
    connection.commit()
    resp = cursor.fetchall()
    cursor.close()
    return resp
