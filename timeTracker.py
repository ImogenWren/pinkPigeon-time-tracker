



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
mgn = prettyCLI.pcli["fg"]["magenta"]

bgbwht =  prettyCLI.pcli["bg"]["white"]
bggry =  prettyCLI.pcli["bg"]["dark-grey"]

# Global Const



#Global Vars


template_dataStore = {
    "last_user" : "0",
    "0" :
        dict(name="Imogen Heard", start="09:00", end="17:00", lunch_start="12:30", lunch_end="13:30", job_open=False,
             last_job="")
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
        self.current_state = 1

    def state_machine(self):
        self.state_init()
        print("loop 0")
        self.current_state = self.state_load_user()
        print("loop 2")
        while self.current_state >= 1:
            if self.current_state == 1:
                self.current_state = self.state_wait()
            elif self.current_state == 2:
                self.current_state = self.state_job_active()
            else:
                print("state machine exception, resetting (for now)")
                self.current_state = 1





    def state_wait(self): # Default State waits for user input (may later thread the user input to allow timing to continue to happen alongside)
        user_input = input(f"Enter {pnk}{{client}}.{blu}{{project}}.{ylw}{{task}}{dft} to begin job\n\n").lower()
        values = re.split(r'[;,. ] ?', user_input)
        # for val in values:
        #    print(val.lower())
        if (values[0] == "exit"):
            print("Ending Current Job & Exiting Software")
            # TODO end job script
            # TODO Exit program script
            return 0
        elif ((values[0] == "job" and values[1] == "end") or (values[0] == "end" and values[1] == "job" )):
            print("Ending Current Job")
            # TODO end job script
            return 3
        else:
            try:
                self.state_new_job(values[0], values[1], values[2])
                return 2
            except:
                print("Exception in state_new_job, ignoring previous input")
        return 1



    def state_job_active(self):
        if self.datastore[self.user]["job_open"] == True:
            try:
                user_input = input(f"Job Active, to end job type {pnk}""end"f" {dft} \n\n")
                if user_input.lower() == "end":
                    #TODO close job
                    print("closing job")
                    self.state_end_job()
                    #self.datastore[self.user]["job_open"] = False
                    return 1
                elif user_input.lower() == "exit":
                    user_input = input(f"End current job before exit? y/n \n\n")
                    if user_input.lower() == "y":
                        print("closing job")
                        self.state_end_job()
                        return 0
                    else:
                        return 0
            except KeyboardInterrupt:
                user_input = input(f"End current job before exit? y/n \n\n")
                if user_input.lower() == "y":
                    print("closing job")
                    self.state_end_job()
                    return 0
                else:
                    return 0




    def state_init(self):
        print(art.pigeonArt)
        print(f"{pnk}{bggry}  pinkPigeon Productivity Tracker  {dft}\n")


    def state_load_user(self):
        db_data = self.load_json_file()
        if (db_data == 0):
            print("Database not found, using default user")
            self.user = self.datastore.get("last_user")
            self.username = self.datastore[self.user].get("name", "Unknown User")
            #print(json.dumps(self.datastore, indent=4))
            return 1
        else:
            self.user = db_data.get("last_user")
            self.username = db_data[self.user].get("name", "Unknown User")
            self.datastore = db_data         # put the loaded data from file into the datastore
            #print(json.dumps(db_data, indent=4))
        print(f"Welcome {self.username}\n")
        if self.datastore[self.user]["job_open"] == True:
            current_job = self.datastore[self.user]["last_job"]
            print(f"Open job {current_job} found")
            user_input = input("Continue job? y/n\n\n")
            if user_input.lower() == "y":
                print("Loop 1")
                return 2
            else:
                self.state_end_job()
                return 1
        else:
            return 1




    def state_new_job(self, client, project, task):
        # TODO END PREVIOUS JOB
        # TODO SAVE DATA TO JSON FILE
        self.client = client
        self.project = project
        self.task = task
        self.task_start = self.get_datetime()
        db_data = self.load_json_file()
        if (db_data == 0):                                 # No valid file found -> create file
            print("no data found, exiting")               # There should at the very least be a valid JSON file, create the file on opening program
            return 0
            # TODO CREATE FILE?
        else:                                                       # File found -> look for existing jobs
            # Update LOCAL datastore with new JSON data
            self.datastore = db_data
            ## Check for existing client in database
            if client in self.datastore[self.user]:
                print(f"{client} found in {self.username}")
            else:
                print(f"{client} not found in {self.username}, Create Client?")
                if (self.user_yes_no()):
                    self.datastore[self.user].setdefault(client, {"hours_total":0})
                    #self.datastore[self.user][client][.setdefault("hours_total", 0)
                    self.datastore[self.user][client]["first_log"] =  self.task_start
                else:
                    return 0
            self.datastore[self.user][client]["last_log"] =  self.task_start          # the last log should be entered always as this is where the calculation is done

            if project in self.datastore[self.user][client]:
                print(f"{project} found in {client}")
            else:
                print(f"{project} not found for {client}, Create Project?")
                if (self.user_yes_no()):
                    self.datastore[self.user][client].setdefault(project, {"hours_total":0})
                    #self.datastore[self.user][client][project].setdefault("hours_total", 0)
                    self.datastore[self.user][client][project]["first_log"] = self.task_start
                else:
                    return 0
            self.datastore[self.user][client][project]["last_log"] = self.task_start

            if task in self.datastore[self.user][client][project]:
                print(f"{task} found in {project}")
            else:
                print(f"{task} not found for {project}, Creating Task")
                if (self.user_yes_no()):
                    self.datastore[self.user][client][project].setdefault(task, {"hours_total":0})
                    #self.datastore[self.user][client][project][task].setdefault("hours_total", 0)
                    print("CREATING TASK first log")
                    self.datastore[self.user][client][project][task]["first_log"] = self.task_start
                else:
                    return 0
            self.datastore[self.user][client][project][task]["last_log"] =  self.task_start
            self.datastore[self.user]["last_job"] = (f"{client}.{project}.{task}")
        # Change job open variable
        self.datastore[self.user]["job_open"] = True
        self.save_dict_to_json(self.datastore)
        print(f"""\nStarting Job:
            {pnk}{client}.{blu}{project}.{ylw}{task}{dft} at {grn}{self.task_start}{dft}\n""")
        return 1   #return 1 on success

    def state_end_job(self):
        db_data = self.load_json_file()
        self.job_end = self.get_datetime()
        if (db_data == 0):  # No valid file found -> create file
            print("no data found, exiting")  # There should at the very least be a valid JSON file, create the file on opening program
            return 0
            # TODO CREATE FILE?
        else:  # File found -> look for existing jobs
            print(f"Ending Current Job{db_data[self.user]["last_job"]}")
            self.datastore = db_data
            values = re.split(r'[;,. ] ?', self.datastore[self.user]["last_job"])
            self.client = values[0]
            self.project = values[1]
            self.task = values[2]

            client_job_start = self.datastore[self.user][self.client]["last_log"]
            client_new_hours = self.time_difference(client_job_start, self.job_end)
            client_current_hours = self.datastore[self.user][self.client]["hours_total"]
            self.datastore[self.user][self.client]["last_log"] = self.job_end
            self.datastore[self.user][self.client]["hours_total"] = client_current_hours + client_new_hours

            project_job_start = self.datastore[self.user][self.client][self.project]["last_log"]
            project_new_hours = self.time_difference(project_job_start, self.job_end)
            project_current_hours = self.datastore[self.user][self.client][self.project]["hours_total"]
            self.datastore[self.user][self.client][self.project]["last_log"] = self.job_end
            self.datastore[self.user][self.client][self.project]["hours_total"] = project_current_hours + project_new_hours

            task_job_start = self.datastore[self.user][self.client][self.project][self.task]["last_log"]
            task_new_hours = self.time_difference(task_job_start, self.job_end)
            task_current_hours = self.datastore[self.user][self.client][self.project][self.task]["hours_total"]
            task_hours = task_current_hours + task_new_hours
            self.datastore[self.user][self.client][self.project][self.task]["last_log"] = self.job_end
            self.datastore[self.user][self.client][self.project][self.task]["hours_total"] = task_hours

            self.datastore[self.user]["job_open"] = False
            self.save_dict_to_json(self.datastore)
            print(f"""\nClosed Job: {pnk}{self.client}.{blu}{self.project}.{ylw}{self.task}{dft} at {grn}{self.job_end}{dft}\n""")
            print(f"You Worked: {mgn}{task_hours}{dft} hours on your current job")
            return 1
        return 1


    def state_list_cmds(self):     # note not all commands implemented yet
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

    def time_difference(self, time_start, time_end):
        date_format = "%Y-%m-%d %H:%M"
        date_start = datetime.strptime(time_start, date_format)
        date_end = datetime.strptime(time_end, date_format)
        seconds_elapsed = date_end - date_start
        hours_difference = seconds_elapsed.total_seconds()/3600
        return hours_difference


    def get_datetime(self):
        dt = datetime.now()
        return dt.strftime("%Y-%m-%d %H:%M")

    # Function to save dictionary as a JSON file
    def save_dict_to_json(self, dictionary):
        with open(self.db_file, 'w') as file:
            json.dump(dictionary, file, indent=4)

    def load_json_file(self):
        try:
            with open(self.db_file, 'r') as file:
                data = json.load(file)  # Load JSON data into a Python dictionary
            return data
        except FileNotFoundError:
            print(f"Error: The file '{self.db_file}' was not found.")
            return 0
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the file.")
            return 0
        except:
            print("Error, using default values")
            return 0

    def user_yes_no(self):
        user_input = input("y/n  (No will cancel create job)\n\n")
        if user_input.lower() == "y":
            return 1
        else:
            print("Creating Job Cancelled")
            return 0
