
def do_all():
    hmo_ids = ["720200236", "720200260", "720200288", "720200262"]
    # 720200295 is 50 Bleinheim, the data logger is broken though
    file_names = []

    for hmo in hmo_ids:
        file_names.append('./csv/{}_2018_19.xlsx'.format(hmo))

    return hmo_ids, file_names


# The following code takes one day of data of user choice and analyzes it.
def chooseafile():
    # If more HMOS are recorded from, add their name below.
    HMO_list = ["25_McIntyre", "2_Himbleton", "37_Woodstock", "8_Bozward", "all"]  # 50_Bleinheim has no data for this season
    # If more data is recorded in the future, add the year, month number below.
    year_list = ["2017_18", "2018_19", "2019_20"]
    month_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

    HMO_check = 1

    while HMO_check == 1:
        print("HMO Names: 25_McIntyre, 2_Himbleton, 37_Woodstock, 8_Bozward. Or just type 'all' (no "
              "quotes)")  # 50_Bleinheim has no data for this season
        print("")
        HMO = input("Type name of the HMO you wish to analyze: ")
        if HMO in HMO_list:
            print("{} is a correct HMO name".format(HMO))
            HMO_check = 0
        else:
            print("The entered HMO name does not exist")
            HMO_check = 1

    year_check = 1

    while year_check == 1:
        year = input("Type the heating season you wish to analyze in Ex: 2018 format (will start in that year, and end in the spring the year after): ")
        i_year = int(year)
        year = "{}_{}".format(year, (str(i_year+1)[-2:]))
        if year in year_list:
            year_check = 0
        else:
            print("The entered year name is formatted wrong or not a valid year")
            year_check = 1
    if HMO == "all":
        return do_all()
    elif HMO == "25_McIntyre":
        string_start = "720200236_"
    elif HMO == "2_Himbleton":
        string_start = "720200260_"
    elif HMO == "37_Woodstock":
        string_start = "720200288_"
    elif HMO == "50_Bleinheim":
        string_start = "720200295_"
    elif HMO == "8_Bozward":
        string_start = "720200262_"
    else:
        print("error in code where likely the start of the string part does not have a check for the new HMO added")

    # final_string = "./csv/{}/{}{}.csv".format(HMO, string_start, year)
    final_string = "./csv/{}{}.xlsx".format(string_start, year)
    # print(final_string)

    return string_start[:-1], final_string

