import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import tkinter
from tkinter import messagebox

# exeで配布するために、ユーザ名とパスワードは都度指定する形に
# username = sys.argv[1]
# password = sys.argv[2]
# company = sys.argv[3]
action = sys.argv[1]

USERNAME_XPATH = '//*[@id="txtUserID"]'
PASSWORD_XPATH = '//*[@id="txtPassword"]'
COMPANY_XPATH = '//*[@id="txtCompanyCode"]'
START_XPATH = '//*[@id="ctl00_ContentMain_btnWebStartTime"]'
STARTTIME_XPATH = '//*[@id="ctl00_ContentMain_txtStartTime"]'
END_XPATH = '//*[@id="ctl00_ContentMain_btnWebEndTime"]'

def page_is_loaded(driver):
    return driver.find_element_by_tag_name("body") != None


# ブラウザのドライバを読み込む。
chrome_options = Options()
chrome_service = Service(executable_path='chromedriver.exe')
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options, service=chrome_service)
# 対象ページを読み込ませる。まずはログインページ。
driver.get("https://pf.us.dell.com/idp/startSSO.ping?PartnerSpId=https%3A%2F%2Fsaml.cvi.co.jp")
wait = ui.WebDriverWait(driver, 10)
# wait.until(page_is_loaded)

# # 読み込んだら、find_element_by_xpathで指定して要素を取得し、入力を与える。
# # あらかじめ、ブラウザにてwebページのソースを表示して、入力したいフォームなどのIDを探しておく。
# username_field = driver.find_element_by_xpath(USERNAME_XPATH)
# username_field.send_keys(username)
#
# password_field = driver.find_element_by_xpath(PASSWORD_XPATH)
# password_field.send_keys(password)
#
# company_field = driver.find_element_by_xpath(COMPANY_XPATH)
# company_field.send_keys(company)
#
# # 全部入力したら、画面遷移
# password_field.send_keys(Keys.RETURN)
# wait = ui.WebDriverWait(driver, 10)
# wait.until(page_is_loaded)

# 同様に、入力したい箇所のIDを指定して、入力を与える。
# ここではsubmit要素の状態(enabled/disabled)で場合分けしている。
# またMessageBoxでどちらの分岐になったか、わかるようにしている。
root = tkinter.Tk()
root.withdraw()

if action == 'start':
    if driver.find_element(By.XPATH,START_XPATH).is_enabled():
    # if driver.find_element_by_xpath(START_XPATH).is_enabled():
        driver.find_element(By.XPATH,START_XPATH).click()
        messagebox.showinfo("Success", """You start this day.
        May your day be well!""")
    else:
        messagebox.showinfo("No action done", """You already started this day.
        May your day be well!""")

elif action == 'end':
    if driver.find_element(By.XPATH,START_XPATH).is_enabled():
        driver.find_element(By.XPATH,STARTTIME_XPATH).send_keys('10:00')
        driver.find_element(By.XPATH,STARTTIME_XPATH).send_keys(Keys.RETURN)
        messagebox.showinfo("Oops", """You seem to forget to start this day.
        Set 10:00.""")

    if driver.find_element(By.XPATH,END_XPATH).is_enabled():
        driver.find_element(By.XPATH,END_XPATH).click()
        messagebox.showinfo("Success", """You ended this day.
        Hope that it went well!""")
    else:
        messagebox.showinfo("No action done", """You already ended this day.
        How was it?""")

driver.close()
try:
    if action == 'start':
        os.system('taskkill /fi "WindowTitle eq attendancepro_start"')
    else:
        os.system('taskkill /fi "WindowTitle eq attendancepro_end"')
    sys.exit()
except:
    messagebox.showwarning("Warning", "You might run from python, or something is wrong with closing window.")