import time

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import sys


def teacher_update_not_over():
    print(f"[INFO]|{current_time()}|更新页面")
    web.find_element(by=By.XPATH, value='//*[@id="ztTab_chzn"]/a').click()
    web.find_element(by=By.XPATH, value='//*[@id="ztTab_chzn_o_3"]').click()
    web.find_element(by=By.XPATH, value='//*[@id="queryform"]/table[1]/tbody/tr/td[2]/button').click()


def teacher_update_not_comment():
    print(f"[INFO]|{current_time()}|更新页面")
    web.find_element(by=By.XPATH, value='//*[@id="ztTab_chzn"]/a').click()
    web.find_element(by=By.XPATH, value='//*[@id="ztTab_chzn_o_1"]').click()
    web.find_element(by=By.XPATH, value='//*[@id="queryform"]/table[1]/tbody/tr/td[2]/button').click()


def red(text):
    return '\033[31m{}\033[0m'.format(text)


def yellow(text):
    return '\x1b[33m{}\x1b[0m'.format(text)


def blue(text):
    return '\x1b[36m{}\x1b[0m'.format(text)


def current_time():
    return yellow(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))


if __name__ == '__main__':
    ACCOUNT = ''
    PASSWORD = ''
    teacher_num = 0
    print(f"[INFO]|{current_time()}|欢迎来到北理工全自动好评系统")
    ACCOUNT = input(f"[INFO]|{current_time()}|请输入需要评教的学号:>")
    PASSWORD = input(f"[INFO]|{current_time()}|请输入需要评教的密码:>")
    print(f"[INFO]|{current_time()}|正在打开浏览器")

    # 创建浏览器对象
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)
    options.add_argument('--disable-blink-features=AutomationControlled')
    web = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    web.execute_cdp_cmd("Emulation.setUserAgentOverride", {
        "userAgent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"
    })
    web.get('https://pj.bit.edu.cn/pjxt2.0/welcome')
    print(f"[INFO]|{current_time()}|当前登录信息如下")
    print(f"[INFO]|{current_time()}|用户:{blue(ACCOUNT)}")
    print(f"[INFO]|{current_time()}|密码:{blue(PASSWORD)}")
    start_time = time.time()
    web.find_element(by=By.XPATH, value='//*[@id="username"]').send_keys(ACCOUNT)
    web.find_element(by=By.XPATH, value='//*[@id="password"]').send_keys(PASSWORD, Keys.ENTER)
    try:
        warning = web.find_element(by=By.XPATH, value='//*[@id="showErrorTip"]').text
        print(f"[{red('ERROR')}]|{current_time()}|{red('登录失败')},{red(warning)}")
        sys.exit()
    except Exception as e:
        print(f"[INFO]|{current_time()}|登陆成功")
    time.sleep(0.5)
    print(f"[INFO]|{current_time()}|进入评教界面")
    web.get('https://pj.bit.edu.cn/pjxt2.0/stpj/queryListStpj')
    teacher_update_not_comment()
    print(f"[INFO]|{current_time()}|正在获取需要评教的教师数量")
    try:
        teacher_num = web.find_element(by=By.XPATH,
                                       value='//*[@id="queryform"]/div/table/tbody/tr/td/div/ul/li[1]/a/font').text
        teacher_num = eval(teacher_num)
    except:
        pass
    print(f"[INFO]|{current_time()}|共有{teacher_num}位教师需要评教")
    for i in range(teacher_num):
        teacher_update_not_comment()
        teacher_name = web.find_element(by=By.XPATH, value='//*[@id="table_report"]/tbody/tr[1]/td[5]').text
        print(f"[INFO]|{current_time()}|正在评教{blue(teacher_name)}")
        web.find_element(by=By.XPATH, value='//*[@id="table_report"]/tbody/tr[1]/td[7]/div/a').click()
        time.sleep(0.5)
        check_form_list = web.find_elements(by=By.XPATH, value='//*[@id="cjForm"]/div/div[2]/div[2]/div')
        for i in range(9):
            check_form = check_form_list[i]
            info = check_form.find_element(by=By.XPATH, value='label').text
            comment = blue("非常符合")
            print(f"[INFO]|{current_time()}|{info}:{comment}")
            check_form.find_element(by=By.XPATH, value='div[1]/input').click()
        web.find_element(by=By.XPATH, value='//*[@id="cjForm"]/div/div[2]/div[2]/div[11]/a[1]').click()
        print(f"[INFO]|{current_time()}|{blue(teacher_name)}评教结束")
        time.sleep(0.5)
        web.find_element(by=By.XPATH, value='/html/body/div[2]/div[2]/a').click()
        time.sleep(1)
    print(f"[INFO]|{current_time()}|所有评教结束")
    print(f"[INFO]|{current_time()}|本次评教了{blue(teacher_num)}位教师")
    end_time = time.time()
    print(f"[INFO]|{current_time()}|用时{blue(end_time - start_time)}s")
