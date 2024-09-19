
import datetime



month_dict = { 'January'  : 1,
               'February' : 2,
               'March'    : 3,
               'April'    : 4,
               'May'      : 5,
               'June'     : 6,
               'July'     : 7,
               'August'   : 8,
               'September': 9,
               'October'  : 10,
               'November' : 11,
               'December' : 12  }


def convert_to_datetime(column):
    return column.apply(lambda x: datetime.date( *map(int,str(x).split('-')) ))


def last_day_of_month(any_day):
    # The day 28 exists in every month. 4 days later, it's always next month
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtracting the number of the current day brings us back one month
    return next_month - datetime.timedelta(days=next_month.day)