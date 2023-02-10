import sqlite3

conn=sqlite3.connect("test.db")


def databasecommand(sql):
    conn.execute(sql)
    



