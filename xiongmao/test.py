import unittest
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
# 无头浏览器的配置项
from selenium.webdriver.chrome.options import Options
# 实现规避检测配置项
from selenium.webdriver import ChromeOptions

# 无头浏览器相关配置
# 规避selenium被浏览器检测的风险
options = ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

brower = webdriver.Chrome(options=options)
brower.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'
})

brower.get("https://www.taobao.com")
# 获取源码信息
page = brower.page_source
print(page)
# 标签定位
search_input = brower.find_element_by_id("q")
# 标签交互
search_input.send_keys("iphone")
search_btn = brower.find_element_by_css_selector(".btn-search")
search_btn.click()
# 执行js代码
brower.execute_script("window.scrollTo(0,document.body.scrollHeight)")
# 浏览器返回
brower.back()
# brower.forward()
# 如果定位元素存在于iframe标签之中，则必须通过如下操作进行标签定位
# brower.switch_to.frame("iframeResult")  # switch_to：切换作用域,传递iframe的id
# div = brower.find_element_by_id("draggable")
# 动作链(由于原本的浏览器对象中没有长按事件，因此需先通过ActionChains将浏览器对象包裹成动作链对象）
# action = ActionChains(brower)
# 点击长按
# action.click_and_hold(div)
# perform：立即执行
# action.move_by_offset(17,0).perform()
# 释放动作链
sleep(2)
# action.release()
# brower.quit()
