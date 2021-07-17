import sqlite3
import sqlite3 as sql
from flask import Flask, render_template

# This is the starter file to make db connection, create table books_1 and
# Then insert some records in the table



# Function to insert records to the table
def add_record(title, topic, cost, quantity):
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO books_1 (title,topic,cost,quantity)"
                        " VALUES(?, ?, ?, ?)",(title, topic, cost, quantity) )

            con.commit()
            msg = "Record successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"

    finally:
        print(msg)
        con.close()


# Function to delete record from the table
def delete(title):

    with sql.connect("database.db") as con:
        query="DELETE FROM books_1 WHERE title = ?"
        cur = con.cursor()
        cur.execute(query,(title,) )
        con.commit()
        msg = "Record successfully deleted"


# Connect with db
conn = sqlite3.connect('database.db')
print("Opened database successfully")

# Check if the table exists and drop table if already exists
tables=conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books_1'")
i=0
for x in tables:
    i+=1
if i>0:
    conn.execute('Drop TABLE books_1')


# Create table books_1
conn.execute('CREATE TABLE books_1 (item_number INTEGER PRIMARY KEY AUTOINCREMENT, '
              'title TEXT NOT NULL, topic TEXT NOT NULL, cost INTEGER, quantity INTEGER)')
print( "Table created successfully")


# Fill the table with some records
add_record('How to get a good grade in 677 in 20 minutes a day', 'Distributed_systems', 50, 100)
add_record('RPCs for Dummies', 'Distributed_systems', 51, 101)
add_record('Xen and the Art of Surviving Graduate School',"Graduate_School",12,100)
add_record('Cooking for the Impatient Graduate Student',"Graduate_School",2,10)
add_record('How to finish Project 3 on time', 'Distributed_systems', 30, 100)

add_record('Why theory classes are so hard.', 'Graduate_School', 10, 100)
add_record('Spring in the Pioneer Valley', 'Graduate_School', 20, 100)

conn.close()

