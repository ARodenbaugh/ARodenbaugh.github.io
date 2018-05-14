#!/usr/bin/python

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost", "alro7383",, "school" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT * from Student")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("output " % data)

# disconnect from server
db.close()