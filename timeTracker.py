



import json
import re
import prettyCLI
import asciiArt as art
from datetime import datetime

dft = prettyCLI.pcli["df"]                # default all

pnk = prettyCLI.pcli["fg"]["pink"]
wht = prettyCLI.pcli["fg"]["white"]
blu = prettyCLI.pcli["fg"]["cyan"]
ylw = prettyCLI.pcli["fg"]["yellow"]
blk = prettyCLI.pcli["fg"]["black"]
grn = prettyCLI.pcli["fg"]["deep-green"]

bgbwht =  prettyCLI.pcli["bg"]["white"]
bggry =  prettyCLI.pcli["bg"]["dark-grey"]

# Global Const

database_filename =

#Global Vars
currentClient = ""
currentProject = ""
currentTask = ""
currentTaskStart = ""

currentUser = "0"
currentUserName = ""


template_dataStore = {
    "last_user" : "0",
    "0" :
        {
            "name"  : "Imogen Heard",
            "start" : "09:00",
            "end"   : "17:00",
            "lunch_start" : "12:30",
            "lunch_end"   : "13:30"
        }
}
class timeTracker:
    def __init__(self):
        self.db_file = "pinkpigeon_datastore.txt"
        self.client = ""
        self.project = ""
        self.task = ""
        self.task_start = ""
        self.user = "0"
        self.username = ""
        self.datastore = template_dataStore

# Default State waits for user input (may later thread the user input to allow timing to continue to happen alongside)
    def state_wait(self):
        user_input = input(f"Enter {pnk}{{client}}.{blu}{{project}}.{ylw}{{task}}{dft} to begin job\n\n").lower()
        values = re.split(r'[;,. ] ?', user_input)
        # for val in values:
        #    print(val.lower())
        if (values[0] == "exit"):
            print("Ending Current Job & Exiting Software")
            # TODO end job script
            # TODO Exit program script
            return 0
        elif (values[0] == "job" and values[1] == "end"):
            print("Ending Current Job")
            # TODO end job script
            return 1
        else:
            self.state_new_job(values[0], values[1], values[2])
            return 1

    def state_init(self):
        print(art.pigeonArt)
        print(f"{pnk}{bggry}  pinkPigeon Productivity Tracker  {dft}\n")
        self.state_load_user()

    def state_load_user(self):
        db_data = self.load_json_file(self.db_file)
        if (db_data == 0):
            print("Database not found, using default user")
            self.user = self.datastore.get("last_user")
            self.username = self.datastore[self.user].get("name", "Unknown User")
            print(json.dumps(self.datastore, indent=4))
        else:
            self.user = db_data.get("last_user")
            self.username = db_data[currentUser].get("name", "Unknown User")
            self.datastore = db_data         # put the loaded data from file into the datastore
            print(json.dumps(db_data, indent=4))
        print(f"Welcome {currentUserName}\n")

    def state_new_job(self, client, project, task):
        # TODO END PREVIOUS JOB
        self.client = client
        self.project = project
        self.task = task
        self.task_start = self.get_datetime()
        db_data = self.load_json_file()
        if (db_data == 0):
            print("no data found, creating log")
            # TODO CREATE FILE?
        else:
            if client in db_data[self.user]:
                print(f"{client} found in {self.username}")
            else:
                print(f"{client} not found in {self.username}, Creating Client")
                self.datastore[self.user].setdefault(client, {})
                self.datastore[self.user][client] = {"first-log": currentTaskStart}
                self.datastore[self.user][client] = {"last-log": currentTaskStart}

            if project in db_data[self.user][client]:
                print(f"{currentProject} found in {client}")
            else:
                print(f"{currentProject} not found for {client}, Creating Project")
                self.datastore[self.user][client][currentProject] = {"first-log": currentTaskStart}
                self.datastore[self.user][client][currentProject] = {"last-log": currentTaskStart}

            if currentTask in db_data[self.user][client][currentProject]:
                print(f"{currentTask} found in {currentProject}")
            else:
                print(f"{currentTask} not found for {currentProject}, Creating Task")
                self.datastore[self.user][currentClient][currentProject][currentTask] = {"first-log": currentTaskStart}
                self.datastore[self.user][currentClient][currentProject][currentTask] = {"last-log": currentTaskStart}

        self.save_dict_to_json(dataStore)
        print(f"""\nStarting New Job:
            {pnk}{client}.{blu}{project}.{ylw}{task}{dft} at {grn}{currentTaskStart}{dft}\n""")

    def state_end_job(self):
        print("Ending Current Job")

    def state_list_cmds(self):
        print("{client}.{project}.{task}      -> Start Job (also ends open job)")
        print("job.end                        -> End Current Job")
        print("job.stats                      -> Get Stats for Current Job")
        print("task.change.{new_task}         -> Change Current Task")
        print("user.change.{user_name}        -> Change user to {user_name}")
        print("user.update.start.{time_in24h} -> Change user work start time")
        print("user.update.end.{time_in24h}   -> Change user work end time")
        print("user.update.lunchstart.{time_in24h} -> Change user lunch time")
        print("user.update.lunchend.{time_in24h} -> Change user lunch time")
        print("user.stats                     -> Get stats for current user")

    # Utility Functions

    def get_datetime(self):
        dt = datetime.now()
        return dt.strftime("%Y-%m-%d %H:%M")

    # Function to save dictionary as a JSON file
    def save_dict_to_json(self, dictionary):
        with open(database_filename, 'w') as file:
            json.dump(dictionary, file, indent=4)

    def load_json_file(self, filename=database_filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)  # Load JSON data into a Python dictionary
            return data
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
            return 0
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the file.")
            return 0
        except:
            print("Error, using default values")
            return 0