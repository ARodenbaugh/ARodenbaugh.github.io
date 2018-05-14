#!/usr/bin/env python3
import sqlite3

class Database(object):
    def __init__(self):

        self.cxn = None
        self.cursor = None

    def openDatabase(self):
        try:
            # a connection to the database
            self.cxn = sqlite3.connect("myfile.db")

            # a cursor from the database connection
            self.cursor = self.cxn.cursor()

        except sqlite3.Error as e:
            print("Error connecting to database!")

    def createDatabase(self):
        # Create a table
        sql = ("CREATE TABLE IF NOT EXISTS acronyms_tbl (ACRONYM VARCHAR(10) NOT NULL,\
                                                         STANDFOR VARCHAR(50),\
                                                         AFFILIATION VARCHAR(80),\
                                                         DESCRIPTION VARCHAR(200))")
        # execute sql (create table)
        self.executeNonQuery(sql)
        print("-- table made")

    def executeNonQuery(self, sql):
        if self.cxn is not None and self.cursor is not None:
            #  Try executing SQL
            try:
                self.cursor.execute(sql)
                self.cxn.commit()
                print("-- executed query")
            # If any errors occur, return the no info dictionary
            except sqlite3.Error as error:
                print("Failed to execute SQL statement.  ")

    # function to write data to database
    def addEntry(self, acronym, standfor, affiliation, description):
        params = (acronym, standfor, affiliation, description)
        self.cursor.execute("INSERT INTO acronyms_tbl VALUES(?, ?, ?, ?)", params)
        print("-- entry added")

    # function to fetch data from database
    def getEntry(self, acronym):
        self.cursor.execute("SELECT * FROM acronyms_tbl WHERE acronym = ?", (acronym, ))
        #print(self.cursor.fetchone())

        # fetch data
        for row in self.cursor:
            print("Acronym: ", row[0])
            print("Stands for: ", row[1])
            print("Affiliation: ", row[2])
            print("Description: ", row[3])

    # Function to close database connection
    def closeDatabase(self):
        #  If the cursor is valid, close it
        if (self.cursor is not None):
            self.cursor.close()
            print("-- cursor closed")
        # If the DB connection is valid, close it
        if (self.cxn is not None):
            self.cxn.close()
            print("-- cxn closed")


'''
def main():

    # Create a database object
    database = Database()

    # Connect to the local sqlite3 database
    database.openDatabase()

    # Create the database tables
    database.createDatabase()

    # Add info to database
    database.addEntry()  #'LASP', "Lab for At and Space Physics", "Lasp-general", "my workplace")

    # Get entry from database
    database.getEntry('LASP')

    # Close the connection to the database
    database.closeDatabase()

    # create the app
    myapp = addAcronymApp(database)

    # start event loop
    sys.exit(myapp.exec_())


if (__name__ == "__main__"):
    main()
'''



