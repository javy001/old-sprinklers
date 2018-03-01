from sqlalchemy import create_engine
from config import con_string
import datetime as dt

con = create_engine(con_string)

def view_logs():
    date1 = dt.date.today().strftime('%Y-%m-%d')
    sql = "select * from sprinklers.logger where run_time > '{0}'".format(date1)
    rows = con.execute(sql).fetchall()
    for row in rows:
        print "############### \nRun Time: {0} \nFunction: {1} \nInfo: {2}".format(row[0],
        row[1],row[2])

def change_rain():
    selection = input("\n1. Turn off sprinklers \n2. Turn on sprinlers\n")
    if selection == 1:
        set_value = 1
        msg = "Turning off sprinklers"
    else:
        set_value = 0
        msg = "Turning on sprinklers"
    print msg
    con.execute("update sprinklers.rain set rain={0}".format(set_value))

def change_time():
    selection = raw_input("Insert new start time: ")
    print "New start time is now {0}".format(selection)
    con.execute("update sprinklers.schedule set start_time = '{0}'".format(selection))

sql = "select rain from sprinklers.rain"
if con.execute(sql).fetchone()[0] == 1:
    status = "The sprinklers are set to rain mode"
else:
    status = "The sprinklers are set to run"

start_time = con.execute("select max(start_time) from sprinklers.schedule").fetchone()[0]

print "******************************************* \n{0} \nStart time: {1}".format(status, start_time)
selection = input("""
Make a selection:
1. Change rain mode
2. Change start time
3. View logs
""")

selections = {1: change_rain, 2: change_time, 3: view_logs}

selections[selection]()
