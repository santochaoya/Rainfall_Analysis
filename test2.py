import datetime as dt


print("Please enter the start time: (format : YYYY-MM-DD HH:00:00)\n")
start_time = input()
print("Please enter the end time: (format : YYYY-MM-DD HH:00:00)\n")
end_time = input()

start_date_time = dt.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
end_date_time = dt.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')




