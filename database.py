#!/usr/bin/env python3
import sqlite3
import csv


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

    # function to add new entry to existing database
    def addEntry(self, acronym, standfor, affiliation, description):
        # handle empty description
        if description == "":
            newdescription = "N/A"
        else:
            newdescription = description

        # add acronym to database
        params = (acronym, standfor, affiliation, newdescription)
        self.cursor.execute("INSERT INTO acronyms_tbl VALUES(?, ?, ?, ?)", params)
        self.cxn.commit()
        print("-- entry added")

    # function to fetch data from database
    def getEntry(self, acronym):
        # if acronym exists in database, fetch data
        self.cursor.execute("SELECT * FROM acronyms_tbl WHERE acronym = ?", (acronym, ))
        self.data = self.cursor.fetchall()
        for row in self.data:
            self.acronymEntry = row[0]
            self.standforEntry = row[1]
            self.affiliationEntry = row[2]
            self.descriptionEntry = row[3]

    # function to edit an existing entry
    def updateEntry(self, acronym, standfor, affiliation, description, oldacronym, oldstandfor, oldaffiliation):
        # handle empy description
        if description == "":
            newdescription = "N/A"
        else:
            newdescription = description
        self.cursor.execute("UPDATE acronyms_tbl \
                            SET acronym = ?, standfor = ?, affiliation = ?, description = ?\
                            WHERE acronym = ? and standfor = ? and affiliation = ?", (acronym, standfor, affiliation, newdescription, oldacronym, oldstandfor, oldaffiliation, ))
        self.cxn.commit()
        print("-- entry updated")

    # function to check if acronym exists in database
    def checkExists(self, acronym):
        # check if already exists
        self.cursor.execute("SELECT 1 FROM acronyms_tbl WHERE acronym = ?", (acronym, ))
        # return True if exists already
        self.acronymExists = self.cursor.fetchone()
        if self.acronymExists is not None:
            print("-- acronym exists")
            return 1
        else:
            print("-- acronym does not exist")
            return 0

    # function to check for exact duplicate entry
    def checkAllExists(self, acronym, standfor, affiliation, description):
        if description == "":
            newdescription = "N/A"
        else:
            newdescription = description
        # check if already exists
        self.cursor.execute("SELECT count(*) from acronyms_tbl WHERE acronym = ? and standfor = ? and affiliation = ? and description = ?", (acronym, standfor, affiliation, newdescription, ))
        # return True if exists already
        self.count = self.cursor.fetchone()
        if self.count is not None:
            if self.count[0] > 0:  # exact entry already exists
                print("-- exact replica")
                return 1
            else:  # entire entry is unique
                print("-- not exact replica")
                return 0

    # function to delete existing acronym from database
    def deleteEntry(self, acronym, standfor, affiliation):
        self.cursor.execute("DELETE FROM acronyms_tbl WHERE acronym = ? and standfor = ? and affiliation = ?", (acronym, standfor, affiliation, ))
        self.cxn.commit()
        print("-- entry deleted")

    # function to close database connection
    def closeDatabase(self):
        #  If the cursor is valid, close it
        if self.cursor is not None:
            self.cursor.close()
            print("-- cursor closed")
        # If the DB connection is valid, close it
        if self.cxn is not None:
            self.cxn.close()
            print("-- cxn closed")

    # write table to csv after edits
    def writeToCsv(self):
        with open("data.csv", 'w') as csv_file:
            self.cursor.execute("SELECT * from acronyms_tbl order by acronym")
            csvWriter = csv.writer(csv_file, delimiter=":")
            rows = self.cursor.fetchall()
            csvWriter.writerows(rows)
        print("-- written to csv")

    # only use to import default values to table
    def importFromCsv(self):

        with open('default.csv', 'r') as file:
            reader = csv.reader(file, delimiter=":")
            for row in reader:
                self.cursor.execute("Insert Into acronyms_tbl VALUES(?, ?, ?, ?)", row)
            print("-- default imported")
            self.cxn.commit()
