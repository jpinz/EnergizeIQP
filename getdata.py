import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def load_xlsx(file_path):
    print("Loading {}...".format(file_path))
    return pd.ExcelFile(file_path)


def get_season(xlsx):
    print("Getting Season")
    return pd.read_excel(xlsx, 'Season')


def get_progress_week_1(xlsx):
    print("Getting Progress Week Semester 1")
    return pd.read_excel(xlsx, 'Progress Week Semester 1')


def get_christmas_break(xlsx):
    print("Getting Christmas Break")
    return pd.read_excel(xlsx, 'Christmas Break')


def get_assessment_week_1(xlsx):
    print("Getting Assessment Week Semester 1")
    return pd.read_excel(xlsx, 'Assessment Week Semester 1')


def get_cold_week(xlsx):
    print("Getting Cold Week")
    return pd.read_excel(xlsx, 'Cold Week')


def get_hot_week(xlsx):
    print("Getting Hot Week")
    return pd.read_excel(xlsx, 'Hot Week')


def get_progress_week_2(xlsx):
    print("Getting Progress Week Semester 2")
    return pd.read_excel(xlsx, 'Progress Week Semester 2')


def get_special_dates(xlsx):
    return {
        'Progress Week Semester 1': get_progress_week_1(xlsx),
        'Christmas Break': get_christmas_break(xlsx),
        'Assessment Week Semester 1': get_assessment_week_1(xlsx),
        'Cold Week': get_cold_week(xlsx),
        'Hot Week': get_hot_week(xlsx),
        'Progress Week Semester 2': get_progress_week_2(xlsx)
    }
