from selenium import webdriver
import time 

#无界面
options=webdriver.ChromeOptions()
#添加无界面模式
options.add_argument('--headless')
#创建浏览器对象
driver=webdriver.Chrome(options=options)
#打开页面
driver.get('http://www.mca.gov.cn/article/sj/xzqh/2020/')
#指定节点
driver.find_element_by_xpath('//*[@id="list_content"]/div[2]/div/ul/table/tbody/tr[1]/td[2]/a').click()
#给页面加载预留时间
time.sleep(3)
#获取当前所有窗口
all_handles=driver.window_handles
#切换页面--切换driver对象
driver.switch_to_window(all_handles[1])
#提取数据
t_list=driver.find_elements_by_xpath('//tbody/tr')
for t in t_list:
    t_list=t.text.split()
    print(t_list)