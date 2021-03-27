# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

if __name__ == '__main__':
    chrome_driver_path = "D:\\opt\\chromedriver\\chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver_path)
    driver.get('https://www.baidu.com/')
    driver.maximize_window()
    js = """
        var evObj = document.createEvent('MouseEvents'); 
        evObj.initMouseEvent(\"mouseover\",true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
        arguments[0].dispatchEvent(evObj);
    """
    menu_xpath = "//a[text()='更多']"
    more_menu = WebDriverWait(driver=driver, timeout=15).until(EC.visibility_of_element_located((By.XPATH, menu_xpath)))
    driver.execute_script(js, more_menu)
    time.sleep(3)
    driver.quit()
