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

#evalfxns rtrn secs since epoch
def eval_restOfDay():
    timeNow = time.mktime(time.get_timeNow())
    restOfDay = time.mktime(time.strptime(time.strftime('23:59:59 %x'), "%X %x"))
    bestTimeBeg = time.mktime(time.strptime(time.strftime('15:00:00 %x'), "%X %x"))
    bestTimeEnd = time.mktime(time.strptime(time.strftime('23:59:59 %x'), "%X %x"))
    if timeNow >= bestTimeBeg and timeNow <= bestTimeEnd:
        return time.mktime(time.get_timeNow()) #add two hours
    if timeNow < bestTimeBeg:
        return bestTimeBeg
    else:
        return eval_day()

def eval_day():
    day = int(time.strftime("%d", time.localtime())) + 1
    bestTimeBeg = time.mktime(time.strptime(time.strftime('15:00:00 {} %b %Y'.format(day)), "%X %d %b %Y"))
    bestTimeEnd = time.mktime(time.strptime(time.strftime('23:59:59 {} %b %Y'.format(day)), "%X %d %b %Y"))
    return bestTimeBeg

def eval_week():
    #if day < 3:
        
    bestTimeBeg = time.mktime(time.strptime(time.strftime('15:00:00 {} %b %Y'.format(day)), "%X %d %b %Y"))
    bestTimeEnd = time.mktime(time.strptime(time.strftime('23:59:59 {} %b %Y'.format(day)), "%X %d %b %Y"))
    pass

def make_reminder(date):
    pass

timeAdded = get_timeNow()


