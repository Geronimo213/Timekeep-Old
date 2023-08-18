import pickle
import timeKeepingHelper as tkh
from datetime import datetime
import time
import bcrypt_helper as bh
import sys
from flask import flask
from flask.ext.mysqldb import MySQL
import json
app.config()

try:
    usr_file = open(".timekeep_users.dat", "r+")
except IOError:
    usr_file = open(".timekeep_users.dat", "w")
    usr_file.close()
    usr_file = open(".timekeep_users.dat", "r+")

user = bh.promptUser(usr_file)
PIK_usr = ".timekeep_%s.dat" % user.upper()

PIK = str(PIK_usr)
projects = []
try:
    with open(PIK, "rb") as file:
        projects = pickle.load(file)
except FileNotFoundError:
    with open(PIK, "wb") as file:
        print("No projects file found. Performing first time setup.")
        pickle.dump(projects, file, pickle.HIGHEST_PROTOCOL)

while True:

    for i, project in enumerate(projects):
        print("%d. %s" % (i + 1, str(project.name)))

    usr_select = input("Choose a project or '+' to create a new project. '*' for settings. Bye' to exit.")

    if usr_select.isdigit():
        selection_index = int(usr_select) - 1
        selection = projects[selection_index]
        while True:
            print("\nName: %s\nStart date: %s\nTotal hours: %.2f\nClient: %s\n" % (
                selection.name, str(selection.start_date.date()), selection.total_hours, selection.client))
            print("\n1. Edit\n2. Delete\n3. Begin work\n4. Cancel")
            proj_selection = input("Choose an option. ")

            if proj_selection == "1":
                edit_select = input("Edit which field?").upper()
                if edit_select == "NAME":
                    selection.name = input("New value: ")
                elif edit_select == "START DATE":
                    selection.start_date = datetime.strptime(input("Starting date of project (Month Day Year: "),
                                                             '%B %d %Y')
                elif edit_select == "TOTAL HOURS":
                    selection.total_hours = float(input("Total hours worked: "))
                elif edit_select == "CLIENT":
                    selection.client = input("Client name: ")
            elif proj_selection == "2":
                if input("Are you sure you want to remove the project? This is not reversible!").upper() == "YES":
                    del projects[selection_index]
                    break
            elif proj_selection == "4":
                break
            elif proj_selection == "3":
                start_time = datetime.now()
                input("Tracking time. Press enter when finished . . . ")
                end_time = datetime.now()
                time_delta = abs(end_time - start_time).total_seconds() / 3600.0
                selection.total_hours = float(selection.total_hours + float(time_delta))

    elif usr_select == '+':
        name = input("Name of the project: ")
        start_date = datetime.strptime(input("Starting date of project (MM/DD/YY: "), '%B %d %Y')
        client = input("Name of client: ")
        tkh.createProject(projects, name, start_date, client)
        with open(PIK, "wb") as file:
            pickle.dump(projects, file, pickle.HIGHEST_PROTOCOL)
    elif usr_select == '*':
        print("Choose an option:\n1.Load a user file.")

    elif usr_select.upper() == "BYE":
        print("Shutting down. Have a nice day.")
        with open(PIK, "wb") as file:
            pickle.dump(projects, file, pickle.HIGHEST_PROTOCOL)
        sys.exit(0)
