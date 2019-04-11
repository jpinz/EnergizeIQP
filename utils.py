import datetime

epoch = datetime.datetime.utcfromtimestamp(0)


def get_month():
    month_check = 1

    while month_check == 1:
        month = input("Enter the month of the data in number format, EX: 11 = November, 01 = January: ")
        if int(month) in range(1, 12):
            month_check = 0
        else:
            print("The month entered is not a month number or not entered correctly")
            month_check = 1

    return month


def get_day(year, month):
    day_check = 1

    while day_check == 1:
        day = input("Enter the day of the data in number format: ")
        day_int = int(day)
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 \
                or month == 12:
            if day_int in range(1, 31):
                day_check = 0
            else:
                print("Enter a day in the month chosen")
                day_check = 1

        if month == 4 or month == 6 or month == 9 or month == 11:
            if day_int in range(1, 30):
                day_check = 0
            else:
                print("Enter a day in the month chosen")
                day_check = 1

        # if month is feb, check for leap year

        if month == 2:
            if year % 4 == 0:
                if day_int in range(1, 29):
                    day_check = 0
                else:
                    print("Enter a day in the month chosen")
                    day_check = 1
            else:
                if day_int in range(1, 28):
                    day_check = 0
                else:
                    print("Enter a day in the month chosen")
                    day_check = 1
    return day_int


def map_hmo_to_id(HMO_id):
    HMO_name = ""
    HMO_num = 0
    if HMO_id == '720200236':
        HMO_name = "25 McIntyre"
        HMO_num = 4

    elif HMO_id == '720200260':
        HMO_name = "2 Himbleton"
        HMO_num = 2

    elif HMO_id == '720200288':
        HMO_name = "37 Woodstock"
        HMO_num = 1

    elif HMO_id == '720200295':
        HMO_name = "50 Bleinheim"
        HMO_num = 5

    elif HMO_id == '720200262':
        HMO_name = "8 Bozward"
        HMO_num = 3

    return HMO_name, HMO_num


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0
