import datetime
import os
import pandas as pd


def chooseafile():
    # If more HMOS are recorded from, add their name below.
    HMO_list = ["25_McIntyre", "2_Himbleton", "37_Woodstock", "50_Bleinheim", "8_Bozward", "all"]

    HMO_check = 1

    while HMO_check == 1:
        print("HMO Names: 25_McIntyre, 2_Himbleton, 37_Woodstock, 50_Bleinheim, 8_Bozward. Or just type 'all' (no "
              "quotes)")
        print("")
        HMO = input("Type name of the HMO you wish to analyze: ")
        if HMO in HMO_list:
            print("{} is a correct HMO name".format(HMO))
            HMO_check = 0
        else:
            print("The entered HMO name does not exist")
            HMO_check = 1

    if HMO == "all":
        return do_all()
    elif HMO == "25_McIntyre":
        string_start = "720200236"
    elif HMO == "2_Himbleton":
        string_start = "720200260"
    elif HMO == "37_Woodstock":
        string_start = "720200288"
    elif HMO == "50_Bleinheim":
        string_start = "720200295"
    elif HMO == "8_Bozward":
        string_start = "720200262"
    else:
        print("error in code where likely the start of the string part does not have a check for the new HMO added")

    file_names = []
    for file in os.listdir("./csv/RawBD/{}/".format(string_start)):
        if file.endswith(".csv") and string_start in file:
            file_names.append('./csv/RawBD/{}/{}'.format(string_start, file))

    return string_start, file_names


def do_all():
    hmo_ids = ["720200236", "720200260", "720200288", "720200262"]
    # 720200295 is 50 Bleinheim, the data logger is broken though

    for hmo in hmo_ids:
        file_names = []
        for file in os.listdir("./csv/RawBD/{}/".format(hmo)):
            if file.endswith(".csv") and hmo in file:
                file_names.append('./csv/RawBD/{}/{}'.format(hmo, file))
        combine(hmo, file_names)


def special_times(df):
    special_dates = {
        'Progress Week Semester 1': {
            'start': datetime.datetime.strptime('03112018', '%d%m%Y'),
            'end': datetime.datetime.strptime('11112018', '%d%m%Y'),
            'df': None
        },
        'Christmas Break': {
            'start': datetime.datetime.strptime('24122018', '%d%m%Y'),
            'end': datetime.datetime.strptime('06012019', '%d%m%Y'),
            'df': None
        },
        'Assessment Week Semester 1': {
            'start': datetime.datetime.strptime('14012019', '%d%m%Y'),
            'end': datetime.datetime.strptime('18012019', '%d%m%Y'),
            'df': None
        },
        'Cold Week': {
            'start': datetime.datetime.strptime('27012019', '%d%m%Y'),
            'end': datetime.datetime.strptime('02022019', '%d%m%Y'),
            'df': None
        },
        'Hot Week': {
            'start': datetime.datetime.strptime('24022019', '%d%m%Y'),
            'end': datetime.datetime.strptime('02032019', '%d%m%Y'),
            'df': None
        },
        'Progress Week Semester 2': {
            'start': datetime.datetime.strptime('02032019', '%d%m%Y'),
            'end': datetime.datetime.strptime('10032019', '%d%m%Y'),
            'df': None
        },
        # 'Easter Break': {
        #     'start': datetime.datetime.strptime('13042019', '%d%m%Y'),
        #     'end': datetime.datetime.strptime('28042019', '%d%m%Y'),
        #     'df': None
        # }
    }

    for key, value in special_dates.items():
        print(key)
        timeframe_df = df.copy()
        start_date = value['start']
        end_date = value['end'] + datetime.timedelta(days=1)
        mask = (timeframe_df.index > start_date) & (timeframe_df.index <= end_date)
        value['df'] = timeframe_df.loc[mask]

    return special_dates


def combine(hmo_id, file_names):
    data = []
    # weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for file_path in file_names:
        print(file_path)
        df_file = pd.read_csv(file_path)
        df_file['datetime'] = pd.to_datetime(df_file['Time'])
        df_file.index = df_file['datetime']
        df_file.drop(['Time', 'HwTSet', 'ActPow', 'PowSet', 'PrimTSet'], axis=1, inplace=True)

        data.append(df_file)

    df = pd.concat(data, ignore_index=False)

    df.index = df['datetime']
    df.drop(df.columns[len(df.columns) - 1], axis=1, inplace=True)
    df.fillna(method='ffill', inplace=True)
    df = df.replace(pd.np.nan, 0)

    df.clip(upper=pd.Series({'PrimT': 55}), axis=1)

    special_dates = special_times(df)

    # weekdays = []

    # for i in range(0, 7):
    #     weekdays.append(df[df.index.weekday == i])

    # print(list(weekdays))

    print(df.head(19))

    start = df.iloc[0].name.year
    end = df.iloc[-1].name.year

    years = "{}_{}".format(str(start), str(end)[-2:])

    with pd.ExcelWriter('./csv/{}_{}.xlsx'.format(hmo_id, years)) as writer:
        print("Starting to write Season")
        df.to_excel(writer, sheet_name='Season')
        print("Season written")
        for key, value in special_dates.items():
            print('Starting to write {}'.format(key))
            value['df'].to_excel(writer, sheet_name=key)
            print('{} Written'.format(key))
        # for index, day in enumerate(weekday_names):
        #     print(index, day)
        #     # print(weekdays[index])
        #     weekdays[index].to_excel(writer, sheet_name=day)



def main():
    """This is the main function for the program, input the selected method you want to run"""
    print("Pick an HMO: ")
    hmo_id, file_names = chooseafile()

    if hmo_id is None or file_names is None:
        return

    print(file_names)

    combine(hmo_id, file_names)

    return


if __name__ == '__main__':
    main()
