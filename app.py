import sys
import os
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys
import tkinter
from tkinter import messagebox

# exeで配布するために、ユーザ名とパスワードは都度指定する形に
username = sys.argv[1]
password = sys.argv[2]
company = sys.argv[3]
action = sys.argv[4]

USERNAME_XPATH = '//*[@id="txtUserID"]'
PASSWORD_XPATH = '//*[@id="txtPassword"]'
COMPANY_XPATH = '//*[@id="txtCompanyCode"]'

START_XPATH = '//*[@id="ctl00_ContentMain_btnWebStartTime"]'
STARTTIME_XPATH = '//*[@id="ctl00_ContentMain_txtStartTime"]'
END_XPATH = '//*[@id="ctl00_ContentMain_btnWebEndTime"]'

def page_is_loaded(driver):
    return driver.find_element_by_tag_name("body") != None


# ブラウザのドライバを読み込む。
driver = webdriver.Chrome(service_log_path=os.path.devnull,
                          executable_path='chromedriver.exe')
# 対象ページを読み込ませる。まずはログインページ。
driver.get("https://eliteattendance.cvi.co.jp/#bsctrl")
wait = ui.WebDriverWait(driver, 10)
wait.until(page_is_loaded)

# 読み込んだら、find_element_by_xpathで指定して要素を取得し、入力を与える。
# あらかじめ、ブラウザにてwebページのソースを表示して、入力したいフォームなどのIDを探しておく。
username_field = driver.find_element_by_xpath(USERNAME_XPATH)
username_field.send_keys(username)

password_field = driver.find_element_by_xpath(PASSWORD_XPATH)
password_field.send_keys(password)

company_field = driver.find_element_by_xpath(COMPANY_XPATH)
company_field.send_keys(company)

# 全部入力したら、画面遷移
password_field.send_keys(Keys.RETURN)
wait = ui.WebDriverWait(driver, 10)
wait.until(page_is_loaded)

# For Test
# March7 = '//*[@id="ctl00_ContentMain_Calendar1"]/tbody/tr[4]/td[7]/a'
# driver.find_element_by_xpath(March7).click()

# 同様に、入力したい箇所のIDを指定して、入力を与える。
# ここではsubmit要素の状態(enabled/disabled)で場合分けしている。
# またMessageBoxでどちらの分岐になったか、わかるようにしている。
root = tkinter.Tk()
root.withdraw()

if action == 'start':
    if driver.find_element_by_xpath(START_XPATH).is_enabled():
        driver.find_element_by_xpath(START_XPATH).click()
        messagebox.showinfo("Success", """You start this day.
        May your day be well!""")
    else:
        messagebox.showinfo("No action done", """You already started this day.
        May your day be well!""")

elif action == 'end':
    if driver.find_element_by_xpath(START_XPATH).is_enabled():
        driver.find_element_by_xpath(STARTTIME_XPATH).send_keys('10:00')
        driver.find_element_by_xpath(STARTTIME_XPATH).send_keys(Keys.RETURN)
        messagebox.showinfo("Oops", """You seem to forget to start this day.
        Set 10:00.""")

    if driver.find_element_by_xpath(END_XPATH).is_enabled():
        driver.find_element_by_xpath(END_XPATH).click()
        messagebox.showinfo("Success", """You ended this day.
        Hope that it went well!""")
    else:
        messagebox.showinfo("No action done", """You already ended this day.
        How was it?""")

