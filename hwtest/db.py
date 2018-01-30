#!/usr/bin/python
import sqlite3
import sys
import pandas as pd

def to_csv(name, path):
    db = sqlite3.connect(name)
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table_name in tables:
        table_name = table_name[0]
        table = pd.read_sql_query("SELECT * from %s" % table_name, db)
        table.to_csv(path + "/" + table_name + '.csv', index_label='index')

print "db.py",sys.argv[1],sys.argv[2]
to_csv(sys.argv[1],sys.argv[2])
