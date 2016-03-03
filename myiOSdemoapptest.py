# -*- coding:utf-8 -*-
from appium import webdriver
import time, logging

desired_caps = {}
desired_caps['platformName'] = "iOS"
desired_caps['platformVersion'] = "9.2.1"
desired_caps['deviceName'] = "Dream(9.2.1)"
desired_caps['udid'] = "f5951894f37eac2e91898a8a2f8cf1e6e059b9cc"
desired_caps['app'] = "/Volumes/Mobile/Mobile Test/myDemoApp/myDemoApp.app"
desired_caps['bundleId'] = "com.chaonin.myDemoApp"
#desired_caps[''] = 
driver = webdriver.Remote("http://localhost:4723/wd/hub",desired_caps)
ele = driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAButton[1]")
for i in range(1,11):
    ele.click()
    time.sleep(1)
    print "you have click the item ", ++i, " times"
driver.quit()
