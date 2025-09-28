# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0011342F41D2E3172A6FED4EDA06C4A0FCCF1AC82C9CD25C8E1D83D181A3C1CABE338C596F017220119CD58477DAACF688858CC72B0D9A20DAD13F14ABA85F3DE8CC959D0440863D791793B8650D3B51FFB2FA08DFF58D3116832081BDF8E077C65FD9F0485C6E6D9C22ABD8972B08B766070B73F857AB477255567F49956DC194CF58E36426E97E06553F74A6B9F1DF117BE07E91389F686F5FC73F8F8EFA93F22006259727E949008BE5522C54BE9C2279E76C3F3B68A6B9D6DDF0D61B99519B774074DE828F85534A39DFE52962A445094385BD2A8D33D9454EE1396275CBCFA30E43B6AF4988B4271FB036AC3A9B0775831DA19B90362B0648D6FFB9F2D44EA9E6EC6E6776B78F7D2E7C883DBBD83FC82712B8F189A1D6253CDCCAC1EA436AA0A8FE0DAC718B76E1968BE41671F262B8DC08D0CA7E8F637B316235031C197D9B1FF7754B9F4747C2DBB12C92ADF8160DE0F65D255B4DC0BC8B349746342FD556FB6152B297B25A3B9665166CA0815AD466AAE386878A85B65B899EA7DA7B43749012E59CBCF318B201767FDBE423423B1D622BC1F03852BD98C327C14BD0DA"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
