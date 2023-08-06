import calendar
from dateutil.relativedelta import relativedelta

def month_inc(df,feature):# Eg df.date or df.date_col (panda series) as input arg to the function
    df = df.copy()
    l = []
    for i in df[feature]: 
        y = i.year
        m = i.month
        d = i.day
        if calendar.monthrange(y,m)[1] == d:# if the date is the last date of the month
            x = i + relativedelta(months=1)
            x = x + relativedelta(day=31)# last date of the next month
            l.append(x)
        else:
            x = i+relativedelta(months=1)# Give the similar date in the next month
            l.append(x)
    return (df.assign(cal_next_month=l))