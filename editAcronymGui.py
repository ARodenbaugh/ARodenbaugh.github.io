#!/usr/bin/env python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from database import Database
import sys


# -- Main app
class editAcronymApp(QApplication):

    def __init__(self, database):
        # initialize parent widget
        QApplication.__init__(self, sys.argv)

        # set app name
        self.setApplicationName("Edit Acronym")

        # create main window and pass in database object
        self.mainWindow = MainWindow(database)

        # show main window
        self.mainWindow.setStyleSheet("background-color: rgb(184,186,193)")
        self.mainWindow.show()


# -- Main GUI window
class MainWindow(QMainWindow):

    # initialize main window
    def __init__(self, database):

        # create instance of actions object
        # self.actions = Actions()

        # initialize parent widget
        QMainWindow.__init__(self)

        # initialize this window
        self.setWindowTitle("Edit Database")

        # set main window size (x, y)
        self.setFixedSize(412, 510)

        # create main widget object and pass in database object
        self.mainWidget = MainWidget(database)

        # set main widget object as central widget of main window
        self.setCentralWidget(self.mainWidget)

        # close application
        self.mainWidget.closePushButton.clicked.connect(self.close)


class MainWidget(QWidget):

    def __init__(self, database):
        QWidget.__init__(self)

        # create database to work with
        self.database = database

        # create bold font
        self.boldFont = QFont()
        self.boldFont.setBold(True)
        self.underline = QFont()
        self.underline.setUnderline(True)

        # create frame for search results
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Panel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(1)

        # create frame for search entry
        self.searchframe = QFrame()
        self.searchframe.setFrameShape(QFrame.Box)
        self.searchframe.setFrameShadow(QFrame.Sunken)
        self.searchframe.setLineWidth(1)

        # create layouts whose parent is the frame. Widgets added to this layout will have frame
        self.frameLayout = QVBoxLayout(self.frame)
        self.searchframeLayout = QVBoxLayout(self.searchframe)

        # create frame widget
        self.frameWidget = FrameWidget()
        self.searchFrameWidget = SearchFrameWidget()

        # create tabwidget for multiple results
        self.tabWidget = TabWidget(database)
        self.tabWidget.hide()

        # create line to be above buttons
        self.lineFrame = QFrame()
        self.lineFrame.setFrameStyle(QFrame.HLine)
        self.lineFrame.setFrameShadow(QFrame.Sunken)

        # intro text
        self.titleText = QLabel("Edit Table Entry", alignment=Qt.AlignCenter)
        self.titleText.setFont(self.boldFont)
        self.titleText.setFont(self.underline)
        self.titleText.setStyleSheet("font: 15pt; color: black")

        # -- Layout List
        self.mainLayout = QVBoxLayout(self)
        self.inputLayout = QHBoxLayout()
        self.descriptionInputLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.editLayout = QHBoxLayout()

        # -- Connect to search frame widget
        self.searchFrameWidget.searchButton.clicked.connect(self.searchButtonClicked)
        self.searchFrameWidget.searchInput.returnPressed.connect(self.searchFrameWidget.searchButton.click)

        # -- Buttons Section
        self.editButton = QPushButton("Edit this acronym")
        self.editButton.setFixedSize(130, 30)
        self.editButton.setStyleSheet("background-color: white")
        self.closePushButton = QPushButton("Close")
        self.closePushButton.setFixedSize(100, 30)
        self.closePushButton.setStyleSheet("background-color: lightgrey")
        self.deleteButton = QPushButton("Delete from database")
        self.deleteButton.setFixedSize(140, 30)
        self.deleteButton.setStyleSheet("background-color: white")
        self.buttonLayout.addStretch(0)
        self.editLayout.addStretch(0)
        self.editLayout.addWidget(self.editButton)
        self.editLayout.addSpacing(7)
        self.editLayout.addWidget(self.deleteButton)
        self.buttonLayout.addWidget(self.closePushButton)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.editButton.clicked.connect(self.editButtonClicked)
        self.deleteButton.setEnabled(False)
        self.editButton.setEnabled(False)

        # -- Add results to frame layout
        self.frameLayout.addLayout(self.frameWidget.control)
        self.searchframeLayout.addLayout(self.searchFrameWidget.control)

        # -- MAIN LAYOUT - add all layouts/stretches to main layout
        self.mainLayout.setSpacing(0)
        self.mainLayout.addWidget(self.titleText)
        self.mainLayout.addSpacing(15)
        self.mainLayout.addWidget(self.searchFrameWidget)
        self.mainLayout.addWidget(self.searchframe)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.tabWidget)
        self.mainLayout.addWidget(self.frameWidget)
        self.mainLayout.addWidget(self.frame)
        self.mainLayout.addSpacing(5)
        self.mainLayout.addLayout(self.editLayout)
        self.mainLayout.addSpacing(15)
        self.mainLayout.addWidget(self.lineFrame)
        self.mainLayout.addSpacing(5)
        self.mainLayout.addLayout(self.buttonLayout)

        # -- Buttons clicked section
        self.frameWidget.saveChangesButton.clicked.connect(self.updateEntry)
        self.frameWidget.discardChangesButton.clicked.connect(self.discardButtonClicked)

    def searchButtonClicked(self):

        # get user search input
        self.myacronym = self.searchFrameWidget.searchInput.text().upper().strip()

        # delete any lingering tabs
        self.tabWidget.clear()
        self.tabWidget.close()

        # check if searched acronym is blank
        if self.myacronym == "":
            self.blankSearchError()

        # check if does not exist in database
        elif self.database.checkExists(self.myacronym) == 0:
            self.searchError()

        # else fetch appropriate data and display in GUI
        else:
            self.database.getEntry(self.myacronym)
            # if search is unique, fill out search result form in frame widget
            if len(self.database.data) == 1:
                self.frame.show()
                for row in self.database.data:
                    self.acronymEntry = row[0]
                    self.standforEntry = row[1]
                    self.affiliationEntry = row[2]
                    self.descriptionEntry = row[3]
                self.frameWidget.acronymInput.setText(self.acronymEntry)
                self.frameWidget.standsforInput.setText(self.standforEntry)
                self.frameWidget.affiliationInput.setText(self.affiliationEntry)
                self.frameWidget.descriptionInput.setText(self.descriptionEntry)
                self.editButton.setEnabled(True)
                self.deleteButton.setEnabled(True)

            # else create Tab widgets to display all duplicates
            else:
                self.frame.hide()
                self.frameWidget.hide()
                self.tabWidget.show()
                self.tabWidget.makeTabs()
                self.editButton.setEnabled(True)
                self.deleteButton.setEnabled(True)
                self.dupwarning = QMessageBox()
                self.dupwarning.setIcon(QMessageBox.Information)
                self.dupwarning.setText("There are multiple results for this acronym.\nSelect the tab you would like to edit/delete.")
                self.dupwarning.setWindowTitle("Duplicate Acronym")
                self.dupwarning.setStandardButtons(QMessageBox.Ok)
                self.dupwarning.exec_()


    def discardButtonClicked(self):
        self.resetForm()
        # if search is unique, fill out search result form
        if len(self.database.data) == 1:
            self.searchFrameWidget.searchInput.setText(self.acronymEntry)
            self.frame.show()
            self.frameWidget.show()
            for row in self.database.data:
                self.acronymEntry = row[0]
                self.standforEntry = row[1]
                self.affiliationEntry = row[2]
                self.descriptionEntry = row[3]
            self.frameWidget.acronymInput.setText(self.acronymEntry)
            self.frameWidget.standsforInput.setText(self.standforEntry)
            self.frameWidget.affiliationInput.setText(self.affiliationEntry)
            self.frameWidget.descriptionInput.setText(self.descriptionEntry)
            self.editButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

        # else create tabs to display duplicates
        else:
            self.searchFrameWidget.searchInput.setText(self.tabWidget.acronymInput.toPlainText())
            self.frame.hide()
            self.frameWidget.hide()
            self.tabWidget.show()
            self.tabWidget.makeTabs()
            self.editButton.setEnabled(True)
            self.deleteButton.setEnabled(True)
            # set tab to current
            self.tabWidget.setCurrentIndex(self.index)

    def searchError(self):
        self.resetForm()
        self.errormsg = QMessageBox()
        self.errormsg.setIcon(QMessageBox.Warning)
        self.errormsg.setText("Error: Acronym does not exist in database")
        self.errormsg.setWindowTitle("Error: Not Found")
        self.errormsg.setStandardButtons(QMessageBox.Ok)
        self.errormsg.exec_()

    def blankSearchError(self):
        self.resetForm()
        self.blankerror = QMessageBox()
        self.blankerror.setIcon(QMessageBox.Warning)
        self.blankerror.setText("Please enter a valid acronym to edit.")
        self.blankerror.setWindowTitle("Error: Blank Search")
        self.blankerror.setStandardButtons(QMessageBox.Ok)
        self.blankerror.exec_()

    def deleteButtonClicked(self):

        # show sure message before deleting
        self.suremsg = QMessageBox()
        self.suremsg.setIcon(QMessageBox.Question)
        self.suremsg.setText("Delete this acronym from the database?")
        self.suremsg.setWindowTitle("Delete from database")
        self.suremsg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.reply = self.suremsg.exec_()

        # if acronym is unique, delete and reset form
        if self.reply == QMessageBox.Yes and len(self.database.data) == 1:
            print('*Deleting unique acronym')
            self.database.deleteEntry(self.acronymEntry, self.standforEntry, self.affiliationEntry)
            self.deletedmsg = QMessageBox()
            self.deletedmsg.setIcon(QMessageBox.Information)
            self.deletedmsg.setText("Acronym successfully deleted from database.")
            self.deletedmsg.setWindowTitle("Table Edited")
            self.deletedmsg.setStandardButtons(QMessageBox.Ok)
            self.deletedmsg.exec_()
            self.database.writeToCsv()  # update csv file
            self.resetForm()

        # else if duplicate, delete selected acronym and display remaining (if any)
        elif self.reply == QMessageBox.Yes and len(self.database.data) > 1:
            # obtain the current index data from the tabWidget array
            self.index = self.tabWidget.currentIndex()
            self.acronymEntry = self.tabWidget.uniqueResults[self.index * 4]
            self.standforEntry = self.tabWidget.uniqueResults[self.index * 4 + 1]
            self.affiliationEntry = self.tabWidget.uniqueResults[self.index * 4 + 2]
            self.descriptionEntry = self.tabWidget.uniqueResults[self.index * 4 + 3]
            print("*Deleting duplicate acronym")
            self.database.deleteEntry(self.acronymEntry, self.standforEntry, self.affiliationEntry)
            self.database.writeToCsv()  # update csv file

            # after reset, check if exists then fill out with remaining duplicates or reset form
            self.myacronym = self.acronymEntry
            if self.database.checkExists(self.myacronym) == 0:
                self.resetForm()
            else:
                self.database.getEntry(self.myacronym)
                self.resetForm()
                self.searchFrameWidget.searchInput.setText(self.myacronym)
                # if search is unique, fill out search result form
                if len(self.database.data) == 1:
                    self.frame.show()
                    print("*Show remaining tab")
                    for row in self.database.data:
                        self.acronymEntry = row[0]
                        self.standforEntry = row[1]
                        self.affiliationEntry = row[2]
                        self.descriptionEntry = row[3]
                    self.frameWidget.acronymInput.setText(self.acronymEntry)
                    self.frameWidget.standsforInput.setText(self.standforEntry)
                    self.frameWidget.affiliationInput.setText(self.affiliationEntry)
                    self.frameWidget.descriptionInput.setText(self.descriptionEntry)
                    self.searchFrameWidget.searchInput.setText(self.acronymEntry)
                    self.editButton.setEnabled(True)
                    self.deleteButton.setEnabled(True)
                # else create Tab widgets to display all duplicates
                else:
                    print("*Show remaining tabs")
                    self.frame.hide()
                    self.frameWidget.hide()
                    self.tabWidget.show()
                    self.tabWidget.makeTabs()
                    self.editButton.setEnabled(True)
                    self.deleteButton.setEnabled(True)

            self.deletedmsg = QMessageBox()
            self.deletedmsg.setIcon(QMessageBox.Information)
            self.deletedmsg.setText("Acronym successfully deleted from database.")
            self.deletedmsg.setWindowTitle("Table Edited")
            self.deletedmsg.setStandardButtons(QMessageBox.Ok)
            self.deletedmsg.exec_()

        else:  # doesn't want to delete
            self.suremsg.close()

    def editButtonClicked(self):

        # enable QLineEdit lines to be edited
        self.frameWidget.acronymInput.setReadOnly(False)
        self.frameWidget.standsforInput.setReadOnly(False)
        self.frameWidget.affiliationInput.setReadOnly(False)
        self.frameWidget.descriptionInput.setReadOnly(False)
        self.frameWidget.acronymInput.setStyleSheet("background-color: white")
        self.frameWidget.standsforInput.setStyleSheet("background-color: white")
        self.frameWidget.affiliationInput.setStyleSheet("background-color: white")
        self.frameWidget.descriptionInput.setStyleSheet("background-color: white")

        # show editing message and the save/discard buttons
        self.frameWidget.resultText.hide()
        self.frameWidget.editMessage.show()
        self.frameWidget.saveChangesButton.show()
        self.frameWidget.discardChangesButton.show()
        self.editButton.hide()
        self.deleteButton.hide()
        self.searchFrameWidget.searchButton.setEnabled(False)
        self.searchFrameWidget.searchInput.setReadOnly(True)
        self.searchFrameWidget.searchLabel.setStyleSheet("color: grey")

        # if unique, don't change display
        if len(self.database.data) == 1:
            print('*Editing unique')
            self.searchFrameWidget.searchInput.setText(self.frameWidget.acronymInput.toPlainText())

        # if editing a duplicate, fill out frame widget with the active tab inputs
        elif len(self.database.data) > 1:
            print('*Editing duplicate')
            # obtain the current index data from the tabWidget array
            self.index = self.tabWidget.currentIndex()
            self.acronymEntry = self.tabWidget.uniqueResults[self.index * 4]
            self.standforEntry = self.tabWidget.uniqueResults[self.index * 4 + 1]
            self.affiliationEntry = self.tabWidget.uniqueResults[self.index * 4 + 2]
            self.descriptionEntry = self.tabWidget.uniqueResults[self.index * 4 + 3]
            self.frameWidget.acronymInput.setText(self.acronymEntry)
            self.frameWidget.standsforInput.setText(self.standforEntry)
            self.frameWidget.affiliationInput.setText(self.affiliationEntry)
            self.frameWidget.descriptionInput.setText(self.descriptionEntry)
            self.searchFrameWidget.searchInput.setText(self.acronymEntry)

            # close tabs and display results in frame widget
            self.tabWidget.clear()
            self.tabWidget.close()
            self.frame.show()
            self.frameWidget.show()
            self.tabWidget.hide()
        else:
            print('error')

    def updateEntry(self):
        # show sure message before saving changes
        self.sure = QMessageBox()
        self.sure.setIcon(QMessageBox.Question)
        self.sure.setText("Save these changes?")
        self.sure.setWindowTitle("Edit Entry")
        self.sure.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.myreply = self.sure.exec_()

        # obtain variables to change in the database
        self.newAcronym = self.frameWidget.acronymInput.toPlainText().strip().upper()
        self.newStandfor = self.frameWidget.standsforInput.toPlainText().strip()
        self.newAffiliation = self.frameWidget.affiliationInput.toPlainText().strip()
        self.newDescription = self.frameWidget.descriptionInput.toPlainText().strip()

        # if sure = yes, update the entry
        if self.myreply == QMessageBox.Yes:
            self.database.updateEntry(self.newAcronym, self.newStandfor, self.newAffiliation, self.newDescription,
                                      self.acronymEntry, self.standforEntry, self.affiliationEntry)
            self.database.writeToCsv()  # update csv file
            # show success message after updated
            self.editedmsg = QMessageBox()
            self.editedmsg.setIcon(QMessageBox.Information)
            self.editedmsg.setText("Acronym successfully updated in the database.")
            self.editedmsg.setWindowTitle("Table Edited")
            self.editedmsg.setStandardButtons(QMessageBox.Ok)
            self.editedmsg.exec_()
            self.resetForm()

            # show the updated search results
            self.database.getEntry(self.newAcronym)
            self.searchFrameWidget.searchInput.setText(self.newAcronym)
            # if search is unique, fill out search result form
            if len(self.database.data) == 1:
                self.frame.show()
                for row in self.database.data:
                    self.acronymEntry = row[0]
                    self.standforEntry = row[1]
                    self.affiliationEntry = row[2]
                    self.descriptionEntry = row[3]
                self.frameWidget.acronymInput.setText(self.acronymEntry)
                self.frameWidget.standsforInput.setText(self.standforEntry)
                self.frameWidget.affiliationInput.setText(self.affiliationEntry)
                self.frameWidget.descriptionInput.setText(self.descriptionEntry)
                self.editButton.setEnabled(True)
                self.deleteButton.setEnabled(True)
            # else create Tab widgets to display all duplicates
            else:
                self.frame.hide()
                self.frameWidget.hide()
                self.tabWidget.show()
                self.tabWidget.makeTabs()
                self.editButton.setEnabled(True)
                self.deleteButton.setEnabled(True)
                self.tabWidget.setCurrentIndex(self.index)

    def resetForm(self):
        print("-- reset form")
        # delete any lingering tabs
        self.tabWidget.clear()
        self.tabWidget.close()
        # show default display
        self.frame.show()
        self.frameWidget.show()
        self.tabWidget.hide()
        # reset search result form
        self.frameWidget.acronymInput.setStyleSheet("background-color: lightgrey")
        self.frameWidget.standsforInput.setStyleSheet("background-color: lightgrey")
        self.frameWidget.affiliationInput.setStyleSheet("background-color: lightgrey")
        self.frameWidget.descriptionInput.setStyleSheet("background-color: lightgrey")
        self.searchFrameWidget.searchInput.clear()
        self.searchFrameWidget.searchInput.setReadOnly(False)
        self.searchFrameWidget.searchButton.setEnabled(True)
        self.searchFrameWidget.searchLabel.setStyleSheet("color: black")
        self.frameWidget.acronymInput.clear()
        self.frameWidget.acronymInput.setReadOnly(True)
        self.frameWidget.standsforInput.clear()
        self.frameWidget.standsforInput.setReadOnly(True)
        self.frameWidget.affiliationInput.clear()
        self.frameWidget.affiliationInput.setReadOnly(True)
        self.frameWidget.descriptionInput.clear()
        self.frameWidget.descriptionInput.setReadOnly(True)
        self.frameWidget.saveChangesButton.hide()
        self.frameWidget.discardChangesButton.hide()
        self.frameWidget.editMessage.hide()
        self.frameWidget.resultText.show()
        self.editButton.show()
        self.editButton.setEnabled(False)
        self.deleteButton.show()
        self.deleteButton.setEnabled(False)


class FrameWidget(QFrame):
    def __init__(self):
        QFrame.__init__(self)

        # create layouts
        self.mainLayout = QVBoxLayout(self)
        self.control = QVBoxLayout()
        self.acronymLayout = QHBoxLayout()
        self.standsforLayout = QHBoxLayout()
        self.affiliationLayout = QHBoxLayout()
        self.descriptionLayout = QHBoxLayout()
        self.buttonEditsLayout = QHBoxLayout()

        # -- Acronym autofill Section
        self.acronymLabel = QLabel("Acronym: ")
        self.acronymLabel.setStyleSheet("color: black")
        self.acronymInput = QTextEdit()
        self.acronymInput.setReadOnly(True)
        self.acronymInput.setFixedSize(300, 30)
        self.acronymInput.move(100, 0)
        self.acronymInput.setStyleSheet("background-color: lightgrey")
        self.acronymLayout.addStretch(1)
        self.acronymLayout.addWidget(self.acronymLabel)
        self.acronymLayout.addWidget(self.acronymInput)

        # -- Stands For autofill Section
        self.standsforLabel = QLabel("Stands For: ")
        self.standsforLabel.setStyleSheet("color: black")
        self.standsforInput = QTextEdit()
        self.standsforInput.setReadOnly(True)
        self.standsforInput.setFixedSize(300, 30)
        self.standsforInput.setStyleSheet("background-color: lightgrey")
        self.standsforLayout.addStretch(1)
        self.standsforLayout.addWidget(self.standsforLabel)
        self.standsforLayout.addWidget(self.standsforInput)

        # -- Affiliation autofill Section
        self.affiliationLabel = QLabel("Affiliation:  ")
        self.affiliationLabel.setStyleSheet("color: black")
        self.affiliationInput = QTextEdit()
        self.affiliationInput.setReadOnly(True)
        self.affiliationInput.setFixedSize(300, 30)
        self.affiliationInput.setStyleSheet("background-color: lightgrey")
        self.affiliationLayout.addStretch(1)
        self.affiliationLayout.addWidget(self.affiliationLabel)
        self.affiliationLayout.addWidget(self.affiliationInput)

        # -- Description autofill Section
        self.descriptionLabel = QLabel("Description: \n\n\n\n\n")
        self.descriptionLabel.setStyleSheet("color: black")
        self.descriptionInput = QTextEdit()
        self.descriptionInput.setReadOnly(True)
        self.descriptionInput.setFixedSize(300, 100)
        self.descriptionInput.setStyleSheet("background-color: lightgrey")
        self.descriptionLayout.addWidget(self.descriptionLabel)
        self.descriptionLayout.addWidget(self.descriptionInput)
        self.descriptionLayout.addStretch(1)

        self.resultText = QLabel("Search Results:")

        # -- Format for editing entry
        self.editMessage = QLabel("Make desired changes to the entry.\n")
        self.editMessage.hide()
        self.saveChangesButton = QPushButton("Save Changes")
        self.saveChangesButton.hide()
        self.saveChangesButton.setStyleSheet("background-color: white")
        self.saveChangesButton.setFixedSize(140, 30)
        self.discardChangesButton = QPushButton("Discard Changes")
        self.discardChangesButton.hide()
        self.discardChangesButton.setFixedSize(140, 30)
        self.discardChangesButton.setStyleSheet("background-color: white")
        self.buttonEditsLayout.addStretch(1)
        self.buttonEditsLayout.addWidget(self.saveChangesButton)
        self.buttonEditsLayout.addWidget(self.discardChangesButton)

        self.control.addWidget(self.editMessage)
        self.control.addWidget(self.resultText)
        self.control.addLayout(self.acronymLayout)
        self.control.addLayout(self.standsforLayout)
        self.control.addLayout(self.affiliationLayout)
        self.control.addLayout(self.descriptionLayout)
        self.control.addLayout(self.buttonEditsLayout)


class SearchFrameWidget(QFrame):
    def __init__(self):
        QFrame.__init__(self)

        # create layouts
        self.mainLayout = QVBoxLayout(self)
        self.control = QVBoxLayout()
        self.searchLayout = QHBoxLayout()

        self.searchLabel = QLabel("Search for an acronym to edit: ")
        self.searchLabel.setStyleSheet("color: black")
        self.searchInput = QLineEdit()
        self.searchInput.setFixedSize(90, 30)
        self.searchInput.setStyleSheet("background-color: white")
        self.searchInput.setPlaceholderText("ex: LASP")
        self.searchButton = QPushButton("Search")
        self.searchButton.setStyleSheet("background-color: white")

        # add widgets to search layout
        self.searchLayout.addWidget(self.searchLabel)
        self.searchLayout.addWidget(self.searchInput)
        self.searchLayout.addWidget(self.searchButton)
        self.control.addLayout(self.searchLayout)


class TabWidget(QTabWidget):
    def __init__(self, database):
        QTabWidget.__init__(self)
        # create database object to work with
        self.database = database

    def makeTabs(self):
        # Make a tab for each result
        self.tabs = []
        self.uniqueResults = []
        for result in range(len(self.database.data)):
            self.tabs.append(QWidget())

        counter = 0  # used for labels and iterating through database rows
        for self.tab in self.tabs:
            self.addTab(self.tab, "Result " + str(counter+1))
            self.tabUI(self.tab)

            # Populate the displays in each tab
            self.tab.setLayout(self.control)

            # Fill out tabs with search result data and put in a list to access later
            self.acronymInput.setText(self.database.data[counter][0])
            self.uniqueResults.append(self.acronymInput.toPlainText())
            self.standsforInput.setText(self.database.data[counter][1])
            self.uniqueResults.append(self.standsforInput.toPlainText())
            self.affiliationInput.setText(self.database.data[counter][2])
            self.uniqueResults.append(self.affiliationInput.toPlainText())
            self.descriptionInput.setText(self.database.data[counter][3])
            self.uniqueResults.append(self.descriptionInput.toPlainText())

            counter += 1

    def tabUI(self, mytab):

        # create layouts
        self.control = QVBoxLayout(self)
        self.acronymLayout = QHBoxLayout()
        self.standsforLayout = QHBoxLayout()
        self.affiliationLayout = QHBoxLayout()
        self.descriptionLayout = QHBoxLayout()
        self.buttonEditsLayout = QHBoxLayout()

        # -- Acronym autofill Section
        self.acronymLabel = QLabel("Acronym: ")
        self.acronymLabel.setStyleSheet("color: black")
        self.acronymInput = QTextEdit()
        self.acronymInput.setReadOnly(True)
        self.acronymInput.setFixedSize(300, 30)
        self.acronymInput.move(100, 0)
        self.acronymInput.setStyleSheet("background-color: lightgrey")
        self.acronymLayout.addStretch(1)
        self.acronymLayout.addWidget(self.acronymLabel)
        self.acronymLayout.addWidget(self.acronymInput)

        # -- Stands For autofill Section
        self.standsforLabel = QLabel("Stands For: ")
        self.standsforLabel.setStyleSheet("color: black")
        self.standsforInput = QTextEdit()
        self.standsforInput.setReadOnly(True)
        self.standsforInput.setFixedSize(300, 30)
        self.standsforInput.setStyleSheet("background-color: lightgrey")
        self.standsforLayout.addStretch(1)
        self.standsforLayout.addWidget(self.standsforLabel)
        self.standsforLayout.addWidget(self.standsforInput)

        # -- Affiliation autofill Section
        self.affiliationLabel = QLabel("Affiliation:  ")
        self.affiliationLabel.setStyleSheet("color: black")
        self.affiliationInput = QTextEdit()
        self.affiliationInput.setReadOnly(True)
        self.affiliationInput.setFixedSize(300, 30)
        self.affiliationInput.setStyleSheet("background-color: lightgrey")
        self.affiliationLayout.addStretch(1)
        self.affiliationLayout.addWidget(self.affiliationLabel)
        self.affiliationLayout.addWidget(self.affiliationInput)

        # -- Description autofill Section
        self.descriptionLabel = QLabel("Description: \n\n\n\n\n")
        self.descriptionLabel.setStyleSheet("color: black")
        self.descriptionInput = QTextEdit()
        self.descriptionInput.setReadOnly(True)
        self.descriptionInput.setFixedSize(300, 100)
        self.descriptionInput.setStyleSheet("background-color: lightgrey")
        self.descriptionLayout.addWidget(self.descriptionLabel)
        self.descriptionLayout.addWidget(self.descriptionInput)
        self.descriptionLayout.addStretch(1)

        # add results to tab layout
        self.resultText = QLabel("Search Results:")
        self.control.addWidget(self.resultText)
        self.control.addLayout(self.acronymLayout)
        self.control.addLayout(self.standsforLayout)
        self.control.addLayout(self.affiliationLayout)
        self.control.addLayout(self.descriptionLayout)
        self.control.addLayout(self.buttonEditsLayout)

        mytab.setLayout(self.control)


def main():

    # Create a database object
    database = Database()

    # Connect to the local sqlite3 database
    database.openDatabase()

    # Create the database tables
    database.createDatabase()

    # Create the app
    myapp = editAcronymApp(database)

    # Start event loop
    sys.exit(myapp.exec_())


if __name__ == "__main__":
    main()
