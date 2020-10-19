from selenium import webdriver

#无界面模式
options=webdriver.ChromeOptions()
#添加无界面参数
options.add_argument('--headless')
#创建浏览器对象
driver=webdriver.Chrome(options=options)
#打开页面
driver.get('https://maoyan.com/')
#点击榜单--榜单节点
driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/ul/li[5]/a').click()
#点击top100
driver.find_element_by_xpath('/html/body/div[3]/ul/li[5]/a').click()

def func():
    #找10个dd节点--返回值列表
    dd_list=driver.find_elements_by_xpath('//*[@id="app"]/div/div/div/dl/dd')
    #遍历
    for dd in dd_list:
        #text:获取当前节点/子节点/后代节点的文本内容
        film_info_list=dd.text.split('\n')
        print(film_info_list)
        print("*"*5)

while True:
    #第一页
    func()
    try:
        #下一页
        driver.find_element_by_link_text('下一页').click()
    except Exception as e:
        driver.quit()
        break

