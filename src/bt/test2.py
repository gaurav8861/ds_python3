#!/usr/bin/python
import datetime


from datetime import timedelta

def getdaya(day):
    re = day+3;
    return str(re)

def check

class Name:
    def __init__(self, first_name, second_name, age):
        self.first_name = first_name
        self.second_name = second_name
        self.age = age
    def display_name(self, second_name):
        print("first_name : ", self.first_name)
        print("second_name : ", second_name)
        print("age : ", self.age)
    def current_date(self):
        dt = datetime.datetime.now().timestamp()
        secs, _ = str(dt).split('.')
        return secs
    def future_date(self, num_days, date):
        future_time = datetime.datetime.now() + timedelta(days=num_days)
        dt = future_time.timestamp()
        print(dt)
        secs, _ = str(dt).split('.')
        return secs
class Add:

        def current_date_and_time():
            dt = datetime.datetime.now().timestamp()
            secs, _ = str(dt).split('.')
            return secs

        def future_date_and_time(num_days):
            dt = datetime.datetime.now()
            future_time = dt + timedelta(days=int(num_days))
            dt_timestamp = future_time.timestamp()
            secs, _ = str(dt_timestamp).split('.')
            return secs
if __name__== "__main__":
    name = Name(first_name="gaurav", second_name=None, age=None)
    name.display_name(second_name="verma")
    date = name.current_date()
    print(date)
    print(name.future_date(1, date))

    Add.current_date_and_time()
    day = "1"
    re = getdaya(1)
    print(re)
    Add.future_date_and_time(num_days=getdaya(1))