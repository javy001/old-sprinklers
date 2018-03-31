import RPi.GPIO as GPIO
import time
import datetime as dt
from sqlalchemy import create_engine
from config import con_string
engine = create_engine(con_string, pool_recycle=3600)

def logger(func, msg):
    con = engine.connect()
    now = dt.datetime.now()
    sql = """insert into sprinklers.logger (run_time, func, meta)
    values('{0}', '{1}', '{2}')""".format(now, func, msg)
    con.execute(sql)
    con.close()


def get_schedule():
    con = engine.connect()
    sql = "select id, start_time, duration from sprinklers.schedule"
    rows = con.execute(sql)
    schedule = {}
    pins = {1: 17, 2: 27, 3: 22, 4: 18}
    for row in rows:
        schedule[row[0]] = {'start_time': row[1], 'duration': row[2], 'pin': pins[row[0]]}
    con.close()
    return schedule


def run_schedule(keys, schedule):
    logger('Run schedule','Starting function')
    GPIO.setmode(GPIO.BCM)
    for sprinkId in keys:
        GPIO.setup(schedule[sprinkId]['pin'], GPIO.OUT)
        #turn on
        logger('Run schedule','Turning on sprinler {0}'.format(sprinkId))
        GPIO.output(schedule[sprinkId]['pin'], GPIO.LOW)
        #sleep duration
        print 'sleep'
        time.sleep(schedule[sprinkId]['duration']*60)
        #turn off
        print 'off'
        GPIO.output(schedule[sprinkId]['pin'], GPIO.HIGH)
        logger('Run schedule','Turning off sprinler {0}'.format(sprinkId))
    GPIO.cleanup()


logger('Program start','Starting program')
schedule = get_schedule()
keys = schedule.keys()
keys.sort()
run_schedule(keys, schedule)
logger('End program','Closing Program')
