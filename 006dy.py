# _*_ coding: utf-8 _*_
import urllib
import re
import threadpool
# 模拟鼠标悬停实例
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver


# 解析006dy网页HTML
def get_html_all_url(url, page_start):
    html = urllib.urlopen(url).read()
    reg_first_page = r'<li><a href="/show/lunli--------(.*?)---.html">首页</a></li>'
    reg_last_page = r'<li><a href="/show/lunli--------(.*?)---.html">尾页</a>'
    first = re.findall(reg_first_page, html)
    if int(page_start) > 0:
        first = [page_start]

    last = re.findall(reg_last_page, html)
    print 'first=' + first[0] + ',last=' + last[0]
    url_list = []
    for page_nun in range(int(first[0]), int(last[0])+1):
        sub_url = 'https://www.006dy.cc/show/lunli--------' + str(page_nun) + '---.html'
        url_list.append(sub_url)
    return url_list


# 获取html子页面
def get_sub_html_url(url, skip_num, skip_url):
    html = urllib.urlopen(url).read()
    reg_page = r'<h4 class="title text-overflow"><a href="(.*?)" title="(.*?)">'
    url_list = []
    index = 0
    for sub_url in re.findall(reg_page, html):
        index = index + 1
        if index <= skip_num and url == skip_url:
            continue
        url_list.append('https://www.006dy.cc'+sub_url[0])
    return url_list


# 使用chrome打开网页并定位到迅雷连接
def get_thunder_url(url):
    chrome_driver_path = "D:\\opt\\chromedriver\\chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver_path)
    # 打开网站
    driver.get(url)
    # 最小化窗口，避免老展示窗口信息
    driver.minimize_window()
    # 获取006dy网站迅雷连接内容
    result_url = get_006dy_site_thunder_url(driver,url)
    # 5.关闭浏览器
    driver.close()
    return result_url


# 定位迅雷联机实现鼠标移动获取链接
def get_006dy_site_thunder_url(driver, url):
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
        print("当前详情页：" + url + "找不到对应的element，尝试处理多element……")
        try:
            a_element_list = \
                get_elements(driver, '//ul[@class="stui-content__playlist clearfix downlist column8"]/li/a')
            if a_element_list is None:
                return None
            for a_element in a_element_list:
                result_url_list.append(a_element.get_property('href'))
        except NoSuchElementException:
            print("找不到对应的element，跳过")
    except WebDriverException:
        print("驱动异常，跳过")
        return None
    return result_url_list


def get_element(driver, xpath):
    return driver.find_element_by_xpath(xpath)


def get_elements(driver, xpath):
    return driver.find_elements_by_xpath(xpath)


def write_file(context):
    f = open("C:\\Users\\Administrator\\Desktop\\006dy_thunder.txt", 'a')  # 若文件不存在，系统自动创建。'a'表示可连续写入到文件，保留原内容，在原
    # 内容之后写入。可修改该模式（'w+','w','wb'等）

    f.write(context)  # 将字符串写入文件中
    f.write("\n")  # 换行


def thread_pool_processor(urls):
    task_pool = threadpool.ThreadPool(10)
    requests = threadpool.makeRequests(thread_executor, urls)
    [task_pool.putRequest(req) for req in requests]
    # 等待一批网页详情执行完
    task_pool.wait()


def thread_executor(url):
    try:
        # 获取迅雷下载地址
        thunder_urls = get_thunder_url(url)
        if isinstance(thunder_urls, list):
            for sub_thunder_url in thunder_urls:
                print sub_thunder_url
                # write_file(sub_thunder_url)
    except Exception:
        print '访问视频详情页出错，跳过继续,当前视频详情页面：' + url


# 获取006dy网站可下载的迅雷地址资源
def thunder_006dy():
    total = 0
    # 要跳过第几页视频资源
    skip_page = '50'
    try:
        for i in get_html_all_url('https://www.006dy.cc/show/lunli-----------.html', skip_page):
            try:
                video_list = \
                    get_sub_html_url(i, 10, 'https://www.006dy.cc/show/lunli--------' + skip_page + '---.html')
                # 线程池执行处理多视频详情url
                thread_pool_processor(video_list)
                # 统计一共有多少条记录
                total = total + len(video_list)
            except Exception:
                print '访问分页网页异常，跳过继续,当前页面：' + i
                continue
        print total
    except Exception:
        print '程序异常结束'


if __name__ == '__main__':
    # 开始处理006dy网站资源
    thunder_006dy()
