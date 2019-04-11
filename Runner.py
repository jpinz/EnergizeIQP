import chooseafile as ch
import getdata
import plotall
import datetime
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--id", help="the id of the HMO")
    parser.add_argument("-y", "--year", help="the year to analyze", type=int)
    args = parser.parse_args()
    if args.id:
        HMO_id = args.id
        if args.year:
            HMO_path = "./csv/{}_{}.csv".format(args.id, args.year)
        else:
            current_year = datetime.datetime.now().year
            last_year = current_year - 1
            HMO_path = "./csv/{}_{}_{}.xlsx".format(args.id, str(current_year), str(last_year)[-2:])
    else:
        """This is the main function for the program, input the selected method you want to run"""
        print("Pick an HMO: ")
        HMO_id, HMO_path = ch.chooseafile()

    if isinstance(HMO_id, list) and isinstance(HMO_path, list):
        for i in range(0, len(HMO_path)):
            xlsx = getdata.load_xlsx(HMO_path[i])
            df = getdata.get_season(xlsx)
            breaks = getdata.get_special_dates(xlsx)
            plotall.plot_all(HMO_id[i], df, breaks)
        return 0
    else:
        print(HMO_path)
        xlsx = getdata.load_xlsx(HMO_path)
        df = getdata.get_season(xlsx)
        breaks = getdata.get_special_dates(xlsx)

        plotall.plot_all(HMO_id, df, breaks)

        return 0

    return


if __name__ == '__main__':
    main()
