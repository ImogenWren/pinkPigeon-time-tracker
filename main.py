'''
time-tracker

// Funner Names?
productivityPigeon
timeOwl


Simple CLI interface for tracking time spent over different projects & hirarchies

Setup:
-> Enter in typical work hours
-> Enter in typical lunch break hours

Use:
- When starting a job:
    - Enter:
        - `{client}.{project}.{task}`
        eg:
        `remotelabs.stc.develop-fw`

-> Software will check for existing client & project,
    -> if found, software will log start time
    -> if client not found, prompt user to add new client
    -> if project not found, prompt user to add new project
    -> if task not found, prompt user to add new task
        -> Software will report:
            - "Job

- When finishing a job:
    - Enter:
        - `task.finished`
        or
        - `job.finished`
        or
        - `close.task`
        or
        - `close.job`

-> Software will close project and log end time & hours spent on job

-> Starting a new task will automatically close the last one with prompt
    -> "{software-name} cannot have two jobs open, closing previous task: {client}.{project}.{task}

-> Entering lunch hour will close current job & log hours, then prompt user:
    - "Current Job: {client}.{project}.{task} closed for lunch hour: resume? yes/no"
        - On user select no, program will enter wait state
-> If ending work day, software will close current task, then prompt user:
    - "End of Work Day, Current Job: {client}.{project}.{task} closed"
        -> Software will automatically close

Reading back logs
_All data will be saved in JSON/CSV etc format OR database for easy recall, with various in program commands to get back specific data_

Recall Commands:
`{client}.gethours` -> returns total hours for client
`{client}.gethourssince` -> returns hours for client since last hours since was made
'{


# Data Store
{
"client":
    {
    "first-log":"{date of first log}",
    "last-log":"{date of last log}",
    "last-report":"{date of last report}",
    "total-hours":{total hours for client},
    "hours-since":{hours since last report for client}
        {
         "project":
            "first-log":"{date of first log}",
            "last-log":"{date of last log}",
            "last-report":"{date of last report}",
            "total-hours":{total hours for project},
            "hours-since":{hours since last report for project}
            {
            "task":
                "first-log":"{date of first log}",
                "last-log":"{date of last log}",
                "last-report":"{date of last report}",
                "total-hours":{total hours for task},
                "hours-since":{hours since last report for task}
            }  #end of task
        } # end of project
    } # end of client
} # end of data-store

'''
import timeTracker

pp = timeTracker.timeTracker()

def main():
    pp.state_init()
    pp.state_machine()
    print("Software Exiting, Goodbye")





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()




