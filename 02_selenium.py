from selenium import webdriver
import time

#打开浏览器---创建浏览器对象
driver = webdriver.Chrome()
#打开百度
driver.get('http://www.baidu.com/')
#在搜索框输入---找搜索框节点
driver.find_element_by_xpath('//*[@id="kw"]').send_keys('百度图片')
#点击百度一下---找百度一下节点
driver.find_element_by_xpath('//*[@id="su"]').click()

# 5秒钟后关闭浏览器
# time.sleep(5)
# driver.quit()