import os
import re
from selenium import webdriver
import urllib3
from pathlib import Path


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
        string_start = "hmo_4"
    elif HMO == "2_Himbleton":
        string_start = "hmo_2"
    elif HMO == "37_Woodstock":
        string_start = "hmo_1"
    elif HMO == "50_Bleinheim":
        string_start = "hmo_5"
    elif HMO == "8_Bozward":
        string_start = "hmo_3"
    else:
        print("error in code where likely the start of the string part does not have a check for the new HMO added")

    file_names = []
    for file in os.listdir("./{}/".format(string_start)):
        if file.endswith(".html"):
            file_names.append('./{}/{}'.format(string_start, file))

    return string_start, file_names


def do_all():
    hmo_nums = ["hmo_1", "hmo_2", "hmo_3", "hmo_4"]
    # hmo_5 is 50 Bleinheim, the data logger is broken though

    for hmo in hmo_nums:
        file_names = []
        for file in os.listdir("./{}/".format(hmo)):
            if file.endswith(".html"):
                file_names.append('./{}/{}'.format(hmo, file))
        screenshot(hmo, file_names)


def screenshot(hmo_num, file_names):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.set_window_size(2500, 1600)
    screenshot_folder = './{}/screenshots/'.format(hmo_num)
    if not os.path.exists(screenshot_folder):
        os.mkdir(screenshot_folder)

    for file in file_names:
        name = re.search("([^\/]+$)", file).group(0)[0:-5]
        driver.get("https://jpinzer.me/EnergizeIQP" + file[1:])
        print(driver.current_url)
        driver.save_screenshot('./{}/screenshots/{}.png'.format(hmo_num, name))
    driver.quit()


def main():
    """This is the main function for the program, input the selected method you want to run"""
    print("Pick an HMO: ")
    hmo_id, file_names = chooseafile()

    if hmo_id is None or file_names is None:
        return

    print(file_names)

    screenshot(hmo_id, file_names)

    return


if __name__ == '__main__':
    main()
