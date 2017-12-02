from time import gmtime, strftime, localtime


def get_timeNow():
    return localtime()

def set_timer(days): #diff options: tonight, tomorrow, in a week, don't remind me
    if days == 0: #eval best time to view tonight
        make_reminder(eval_restOfDay())
    if days == 1: #eval best time to view during the day
        make_reminder(eval_day())
    if days == 7: #eval best time to view during the week & the day
        make_reminder(eval_week())

#evalfxns
def eval_restOfDay():
    pass

def eval_day():
    pass

def eval_week():
    pass

def make_reminder(date):
    pass

timeAdded = get_timeNow()


