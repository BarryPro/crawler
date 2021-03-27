# -*- coding: utf-8 -*-
# 模拟鼠标悬停实例
import sys

from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver


def get_thunder_url(url):
    chrome_driver_path = "D:\\opt\\chromedriver\\chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver_path)
    # 打开网站
    driver.get(url)
    # 最小化窗口，避免老展示窗口信息
    # driver.minimize_window()
    # 获取006dy网站迅雷连接内容
    result_url = get_006dy_site_thunder_url(driver)
    # 5.关闭浏览器
    # driver.close()
    return result_url


def get_006dy_site_thunder_url(driver):
    # 模拟鼠标事件
    # 1.先找到唯一列表ul
    ul_element = None
    result_url_list = []
    try:
        ul_element = \
            get_element(driver, '//ul[@class="stui-content__playlist clearfix downlist"]')
        if ul_element is None:
            return None
        a_element = ul_element.find_element_by_xpath('.//a')
        # 3.把鼠标移动到对应位置
        ActionChains(driver).move_to_element(a_element).perform()
        # 4.返回迅雷资源链接
        result_url = a_element.get_property('href')
        # 单迅雷url追加到结果集里
        result_url_list.append(result_url)
        return result_url_list
    except NoSuchElementException:
        print("找不到对应的element，尝试处理多element……")
        try:
            a_element_list = \
                get_elements(driver, '//ul[@class="stui-content__playlist clearfix downlist column8"]/li/a')
            if a_element_list is None:
                return None
            for i in a_element_list:
                result_url_list.append(i.get_property('href'))
        except NoSuchElementException:
            print("找不到对应的element，跳过")
    except WebDriverException:
        print("驱动异常跳过，跳过")
        return None
    return result_url_list


def get_element(driver, xpath):
    return driver.find_element_by_xpath(xpath)


def get_elements(driver, xpath):
    return driver.find_elements_by_xpath(xpath)


print get_thunder_url('https://www.006dy.cc/detail/57435.html')



