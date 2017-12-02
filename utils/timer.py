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
    timeNow = int(time.time())
    timeBuffer = 2*24*60*6
    bestTimeBeg = int(time.mktime(time.strptime(time.strftime('15:00:00 %x'), "%X %x")))
    bestTimeEnd = int(time.mktime(time.strptime(time.strftime('23:59:59 %x'), "%X %x")))
    if timeNow >= bestTimeBeg and timeNow <= bestTimeEnd - timeBuffer:
        return timeNow + timeBuffer #add two hours
    if timeNow < bestTimeBeg:
        return bestTimeBeg
    else:
        return eval_day()

def eval_day():
    #timeNow = int(time.time()) + 24*60*60
    bestTimeBeg = int(time.mktime(time.strptime(time.strftime('15:00:00 %x'), "%X %x"))) + 24*60*60
    #bestTimeEnd = time.mktime(time.strptime(time.strftime('23:59:59 %x'), "%X %x")) + 24*60*60
    return bestTimeBeg

def eval_week():
    bestTimeBeg = int(time.mktime(time.strptime(time.strftime('15:00:00 %x'),"%X %x"))) + 7*24*60*60  
    return bestTimeBeg    

def make_reminder(secs):
    



