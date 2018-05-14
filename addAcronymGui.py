#!/usr/bin/env python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from database import Database
import sys


# -- Main app
class addAcronymApp(QApplication):

    def __init__(self, database):
        # initialize parent widget
        QApplication.__init__(self, sys.argv)

        # set app name
        self.setApplicationName("Add Acronym")

        # create main window and pass in database object
        self.mainWindow = MainWindow(database)

        # show main window
        self.mainWindow.setStyleSheet("background-color: rgb(184,185,191)")
        self.mainWindow.show()


# -- Main GUI window
class MainWindow(QMainWindow):

    # initialize main window
    def __init__(self, database):

        # initialize parent widget
        QMainWindow.__init__(self)

        # initialize this window
        self.setWindowTitle("")

        # set main window size (x, y)
        self.setFixedSize(835, 267)

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

        # import default acronyms from csv
        #self.database.importFromCsv()

        # create bold font
        self.boldFont = QFont()
        self.boldFont.setBold(True)

        # create line to be above buttons
        self.lineFrame = QFrame()
        self.lineFrame.setFrameStyle(QFrame.HLine)
        self.lineFrame.setFrameShadow(QFrame.Sunken)

        # intro text
        self.titleText = QLabel("Add Acronym to the Database", alignment=Qt.AlignCenter)
        self.titleText.setFont(self.boldFont)
        self.titleText.setStyleSheet("font: 20pt; color: black")

        # -- Layout List
        self.mainLayout = QVBoxLayout(self)
        self.caseLayout = QVBoxLayout()
        self.inputLayout = QHBoxLayout()
        self.affilLayout = QHBoxLayout()
        self.groupLayout = QVBoxLayout()
        self.custLayout = QHBoxLayout()
        self.outerLayout = QHBoxLayout()
        self.textLayout = QVBoxLayout()
        self.blankLayout = QVBoxLayout()
        self.descriptionInputLayout = QHBoxLayout()
        self.descriptionInputLayout.setAlignment(Qt.AlignTop)
        self.buttonLayout = QHBoxLayout()

        # -- Acronym Input Section
        self.acronymLabel = QLabel("Acronym: ")
        self.acronymLabel.setStyleSheet("color: black")
        self.acronymInput = QLineEdit()
        self.acronymInput.setFixedSize(100, 30)
        self.acronymInput.setPlaceholderText("ex: LASP")
        self.acronymInput.setStyleSheet("background-color: white")
        self.acronymInput.setToolTip("Enter an Acronym to add to the database.")

        # -- Stands For Input Section
        self.standsforLabel = QLabel("Stands For: ")
        self.standsforLabel.setStyleSheet("color: black")
        self.standsforInput = QLineEdit()
        self.standsforInput.setFixedSize(255, 30)
        self.standsforInput.setPlaceholderText("ex: Lab for Atmospheric and Space Physics")
        self.standsforInput.setStyleSheet("background-color: white")
        self.standsforInput.setToolTip("Enter what the acronym stands for.")

        # -- Affiliation Input Section
        self.affiliationLabel = QLabel("Affiliation: ")
        self.affiliationLabel.setStyleSheet("color: black")
        self.affiliationInput = QComboBox()
        self.affiliationInput.setFixedSize(180, 30)
        self.affiliationInput.addItems(AffiliationOptions.options)
        self.affiliationInput.setStyleSheet("background-color: white")
        self.affiliationInput.setToolTip("Choose an affiliation for the acronym.")
        self.otherAffilText = QLabel("Custom Affiliation: \n\n\n\n")
        self.otherAffilText.setEnabled(False)
        self.otherAffiliationInput = QLineEdit()
        self.otherAffiliationInput.setFixedSize(180, 30)
        self.otherAffiliationInput.setStyleSheet("background-color: rgb(184,185,191)")
        self.otherAffiliationInput.setEnabled(False)

        # -- Description Input Section
        self.descriptionLabel = QLabel("Description: \n (Optional)")
        self.descriptionLabel.setStyleSheet("color: black")
        self.descriptionInput = QTextEdit()
        self.descriptionInput.setFixedSize(300, 100)
        self.descriptionInput.setPlaceholderText("ex: Research Institute at CU Boulder")
        self.descriptionInput.setStyleSheet("background-color: white")
        self.descriptionInput.setToolTip("Optionally enter a description of the acronyms usage.")
        self.descriptionInputLayout.addWidget(self.descriptionLabel, 0, Qt.AlignTop)
        self.descriptionInputLayout.addWidget(self.descriptionInput)
        self.descriptionInputLayout.addStretch(.5)

        # -- Add acronym and standfor inputs to H input layout
        self.inputLayout.addSpacing(10)
        self.inputLayout.addWidget(self.acronymLabel)
        self.inputLayout.addWidget(self.acronymInput)
        self.inputLayout.addSpacing(15)
        self.inputLayout.addWidget(self.standsforLabel)
        self.inputLayout.addWidget(self.standsforInput)
        # -- Add affiliation input and custom to V layout
        self.affilLayout.addStretch(2)
        self.affilLayout.addWidget(self.affiliationLabel)
        self.affilLayout.addWidget(self.affiliationInput)

        # add custom affils to their V layouts then add to custom H layout
        self.textLayout.addSpacing(6)
        self.textLayout.addWidget(self.otherAffilText)
        self.blankLayout.addWidget(self.otherAffiliationInput, 0, Qt.AlignTop)
        self.custLayout.addLayout(self.textLayout)
        self.custLayout.addLayout(self.blankLayout)

        # add affil and custom to V group layout
        self.groupLayout.addStretch(0)
        self.groupLayout.addLayout(self.affilLayout)
        self.groupLayout.addSpacing(3)
        self.groupLayout.addLayout(self.custLayout)
        self.groupLayout.addStretch(1)

        # add inputs and description to V case layout
        self.caseLayout.addLayout(self.inputLayout)
        self.caseLayout.addSpacing(10)
        self.caseLayout.addLayout(self.descriptionInputLayout)
        # add Case H and Group H layouts to outer V layout
        self.outerLayout.addLayout(self.caseLayout)
        self.outerLayout.addLayout(self.groupLayout)

        # -- Buttons Section
        self.addAcronymButton = QPushButton("Add Acronym")
        self.addAcronymButton.setEnabled(False)
        self.addAcronymButton.setFixedSize(200, 30)
        self.addAcronymButton.setStyleSheet("background-color: white")
        self.addAcronymButton.setToolTip("Enter an Acronym, what it stands for, and its affiliation.")
        self.closePushButton = QPushButton("Close")
        self.closePushButton.setFixedSize(200, 30)
        self.closePushButton.setStyleSheet("background-color: white")
        self.buttonLayout.addStretch(0)
        self.buttonLayout.addWidget(self.addAcronymButton)
        self.buttonLayout.addWidget(self.closePushButton)

        # -- MAIN LAYOUT - add all layouts/stretches to main layout
        self.mainLayout.addWidget(self.titleText)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.outerLayout)
        self.mainLayout.addSpacing(5)
        self.mainLayout.addWidget(self.lineFrame)
        self.mainLayout.addLayout(self.buttonLayout)

        # check inputs when any text is changed
        self.otherAffiliationInput.textChanged.connect(self.checkInputs)
        self.acronymInput.textChanged.connect(self.checkInputs)
        self.standsforInput.textChanged.connect(self.checkInputs)
        self.affiliationInput.currentIndexChanged.connect(self.checkInputs)
        self.descriptionInput.textChanged.connect(self.checkInputs)
        self.addAcronymButton.clicked.connect(self.addAcronymButtonClicked)

    # Handle all tooltips after any input text is changed
    def checkInputs(self):
        # First delete any leading/trailing spaces in the text-inputted strings
        self.editedAcronym = self.acronymInput.text().strip()
        self.editedStandfor = self.standsforInput.text().strip()
        self.editedDescription = self.descriptionInput.toPlainText().strip()
        self.otherAffiliationInput.setToolTip("Select the ~Custom~ option above to insert a custom affiliation.")
        # Check for empty inputs
        if self.editedAcronym == "":
            self.addAcronymButton.setToolTip("Enter an acronym to add to the database.")
            self.addAcronymButton.setEnabled(False)
        elif self.editedStandfor == "":
            self.addAcronymButton.setToolTip("Enter what the acronym stands for.")
            self.addAcronymButton.setEnabled(False)
        elif self.affiliationInput.currentIndex() == self.affiliationInput.findText("-- choose --"):
            self.addAcronymButton.setToolTip("Choose an affiliation for the acronym.")
            self.addAcronymButton.setEnabled(False)
            self.otherAffilText.setEnabled(False)
            self.otherAffiliationInput.setEnabled(False)
        if self.affiliationInput.currentIndex() == self.affiliationInput.findText("~Custom~"):
            self.otherAffiliation()
            # enable line edit for custom
            self.otherAffilText.setEnabled(True)
            self.otherAffiliationInput.setEnabled(True)
            self.otherAffiliationInput.setToolTip("Enter a custom affiliation for the acronym.")
            self.affiliationInput.setToolTip("Select an affiliation or enter a custom affiliation below.")
        if self.affiliationInput.currentText() != "~Custom~":
            self.otherAffiliationInput.setEnabled(False)
            self.otherAffiliationInput.setText("")
            self.otherAffilText.setEnabled(False)
            self.otherAffiliationInput.setStyleSheet("background-color: rgb(184,185,191)")
        # Handle "Custom" affiliation entry
        if self.affiliationInput.currentText() == "~Custom~" and self.otherAffiliationInput.text().strip() == "":  # if custom and blank, throw error
            self.addAcronymButton.setToolTip("Select an affiliation or fill out the Custom Affiliation box.")
            self.addAcronymButton.setEnabled(False)
        elif self.affiliationInput.currentText() == "~Custom~" and self.otherAffiliationInput.text().strip() != "":  # if custom and not blank, set affiliation to custom
            self.myaffiliation = self.otherAffiliationInput.text().strip()
        else:
            self.myaffiliation = self.affiliationInput.currentText()  # if not custom set affiliation to current input
        # If requirements met, enable "Add Acronym" Button
        if self.editedAcronym != "" and self.editedStandfor != "" and self.affiliationInput.currentText() != "-- choose --":
            if self.affiliationInput.currentText() == "~Custom~" and self.otherAffiliationInput.text().strip() == "":
                self.addAcronymButton.setEnabled(False)
                self.addAcronymButton.setToolTip("Select an affiliation or fill out the Custom Affiliation box.")
            elif self.affiliationInput.currentText() == "~Custom~" and self.otherAffiliationInput.text().strip() != "":
                self.addAcronymButton.setEnabled(True)
                self.addAcronymButton.setToolTip("Click to add this acronym to the database.")
            elif self.affiliationInput.currentText() != "~Custom~":
                self.addAcronymButton.setToolTip("Click to add this acronym to the database.")
                self.otherAffiliationInput.setEnabled(False)
                self.otherAffilText.setEnabled(False)
                self.addAcronymButton.setEnabled(True)

    # Handle the affiliation input display if the user selects "Custom Affiliation"
    def otherAffiliation(self):
        if self.affiliationInput.currentIndex() == self.affiliationInput.findText("~Custom~"):
            # enable line edit for custom
            self.otherAffilText.setEnabled(True)
            self.otherAffiliationInput.setEnabled(True)
            self.otherAffiliationInput.setToolTip("Enter a custom affiliation for the acronym.")
            self.affiliationInput.setToolTip("Select an affiliation or enter a custom affiliation below.")

        # Handle display when custom is enabled
        if self.otherAffiliationInput.isEnabled():
            self.otherAffiliationInput.setStyleSheet("background-color: white")
        else:
            self.otherAffiliationInput.setStyleSheet("background-color: rgb(184,185,191)")

    # Function checks inputs and adds inputted acronym & its info to the database
    def addAcronymButtonClicked(self):
        # Replace any colons with dashes (to protect CSV file)
        self.editedAcronym = self.editedAcronym.replace(":", "-")
        self.editedStandfor = self.editedStandfor.replace(":", "-")
        self.myaffiliation = self.myaffiliation.replace(":", "-")
        self.editedDescription = self.editedDescription.replace(":", "-")

        # Check if filled out properly and if acronym exists already
        if self.editedAcronym != "" and self.editedStandfor != "" and self.affiliationInput.currentText() != "-- choose --":
            if self.database.checkExists(self.editedAcronym.upper()) == 1:  # acronym exists: throw error
                if self.database.checkAllExists(self.editedAcronym.upper(), self.editedStandfor, self.myaffiliation, self.editedDescription) == 1:
                    self.exactDuplicate()  # acronym is exact duplicate - display message and do not add
                elif self.duplicateError() == 0:  # User wants to add it anyway
                    self.database.addEntry(self.editedAcronym.upper(), self.editedStandfor, self.myaffiliation, self.editedDescription)
                    self.successMessage()
                    self.database.writeToCsv()
                else:
                    print("-- does not want to add")
            # else acronym does not exists - bypass error and add it to database
            else:
                self.sure = QMessageBox()
                self.sure.setIcon(QMessageBox.Question)
                self.sure.setText("Add this acronym to the database?")
                self.sure.setWindowTitle("Add Acronym")
                self.sure.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                self.myreply = self.sure.exec_()
                if self.myreply == QMessageBox.Yes:
                    self.database.addEntry(self.editedAcronym.upper(), self.editedStandfor, self.myaffiliation, self.editedDescription)
                    self.successMessage()
                    self.database.writeToCsv()

    # Display error if acronym already exists and offer override option
    def duplicateError(self):
        self.duplicatemsg = QMessageBox()
        self.duplicatemsg.setIcon(QMessageBox.Warning)
        self.duplicatemsg.setText("This acronym already exists in the database.")
        self.duplicatemsg.setWindowTitle("Warning: Duplicate Entry")
        self.duplicatemsg.addButton(QPushButton("Add Anyway"), QMessageBox.YesRole)
        self.duplicatemsg.setStandardButtons(QMessageBox.Cancel)
        self.reply = self.duplicatemsg.exec_()
        if self.reply == QMessageBox.Cancel:
            return 1
        # else return 0 to add the duplicate
        else:
            return 0

    # If entry is exact duplicate, display message and in turn, do not add
    def exactDuplicate(self):
        self.dupmsg = QMessageBox()
        self.dupmsg.setIcon(QMessageBox.Warning)
        self.dupmsg.setText("This exact entry already exists in the database.\nCannot add exact duplicates.")
        self.dupmsg.setWindowTitle("Error: Exact Duplicate")
        self.dupmsg.setStandardButtons(QMessageBox.Ok)
        self.dupmsg.exec_()

    # Display message if successfully added to database and option to add another or close GUI
    def successMessage(self):
        self.successmsg = QMessageBox()
        self.successmsg.setIcon(QMessageBox.Information)
        self.successmsg.setText("This acronym was successfully added to database.")
        self.successmsg.setWindowTitle("Acronym Added!")
        self.successmsg.setStandardButtons(QMessageBox.Ok)
        self.successmsg.exec_()
        self.resetForm()

    def resetForm(self):
        self.acronymInput.clear()
        self.standsforInput.clear()
        self.affiliationInput.setCurrentIndex(0)
        self.descriptionInput.clear()


class AffiliationOptions:

    # dict of options for affiliation drop-down menu

    options = ['-- choose --', 'N/A', 'LASP-general', 'NASA-general', 'Mission Name', 'Mission-Specific', 'Multi-Mission', 'National Organization', 'Operational Software', 'OASIS', 'Web Design', '~Custom~']


def main():

    # Create a database object
    database = Database()

    # Connect to the local sqlite3 database
    database.openDatabase()

    # Create the database tables
    database.createDatabase()

    # Create the app
    myapp = addAcronymApp(database)

    # Start event loop
    sys.exit(myapp.exec_())

if __name__ == "__main__":
    main()
