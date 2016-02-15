# -*- coding:utf-8 -*-
# author: chaonin 2015/2/15
from appium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException

class phoneBase:
    def __init__(self, host, port, platform, version, deviceName, noReset, unicodeK, resetK, \
        appPackage, appActivity, appPath, xloginID, xpwID, xloginBtn):
        self.pwmode = 'lower'

        self.desired_caps = {}
        self.desired_caps['platformName'] = platform
        self.desired_caps['platformVersion'] = version
        self.desired_caps['deviceName'] = deviceName
        self.desired_caps['noReset'] = noReset
        self.desired_caps['unicodeKeyboard'] = unicodeK
        self.desired_caps['resetKeyboard'] = resetK
        self.desired_caps['appPackage'] = appPackage
        self.desired_caps['appActivity'] = appActivity
        self.desired_caps['app'] = appPath

        self.xpath_login_id = xloginID
        self.xpath_pw_id = xpwID
        self.xpath_login_btn = xloginBtn

        url = "http://" + host + ":" + str(port) + "/wd/hub"
        self.driver = webdriver.Remote(url, self.desired_caps)
        time.sleep(5)

    def login(self, account, pw):
        ele = self.driver.find_element_by_xpath(self.xpath_login_id)
        ele.send_keys(account)
        ele = self.driver.find_element_by_xpath(self.xpath_pw_id)
        ele.click()
        self.inputpw(pw)
        ele = self.driver.find_element_by_xpath(self.xpath_login_btn)
        ele.click()
        time.sleep(5)

    def inputpw(self, pw):
        len1 = len(pw)
        mask = 'keypad_sign_'
        # input the normal password
        for letter in pw:
            if letter >= 'a' and letter <= 'z':
                mask = 'keypad_sign_'
                mask += letter
                if self.pwmode !='lower':
                    self.switchmode('lower')
                ele = self.driver.find_element_by_xpath("//Button[@id=\'" + mask + "\']")
                ele.click()
                print mask
            elif letter >= 'A' and letter <= 'Z':
                mask = 'keypad_sign_'
                mask += chr(ord(letter) + 32)
                if self.pwmode !='upper':
                    self.switchmode('upper')
                ele = self.driver.find_element_by_xpath("//Button[@id=\'" + mask + "\']")
                ele.click()
                print mask
            elif letter >= '0' and letter <= '9':
                mask = 'digitkeypad_'
                mask += letter
                if self.pwmode !='digit':
                    self.switchmode('digit')
                ele = self.driver.find_element_by_xpath("//Button[@id=\'" + mask + "\']")
                ele.click()
                print mask
            else:
                print "unsupport sign now!"
                return 0
            mask = ''
        # input the OK button for after password
        ele = self.driver.find_element_by_xpath("//Button[@id='digitkeypad_oknew']")
        ele.click()
        time.sleep(2)
    def switchmode(self, mode):
        #mode: digit/uppper/lower/sign
        ele = 'null'
        if mode == 'digit':
            ele = self.driver.find_element_by_xpath("//Button[@id='keypad_sign_num']")
            if ele == 'null':
				print "could not found digit-mode switch key, error!"
				return 0
            else:
                ele.click()
                self.pwmode = 'digit'
                return 1
        elif mode == 'upper' or mode == 'lower': 
            ele = self.driver.find_element_by_xpath("//Button[@id='keypad_abc_ABC']")
            if ele == 'null':
                print "could not found digit-mode switch key, error!"
                return 0
            else:
                ele.click()
                if self.pwmode == 'upper':
                    self.pwmode = 'lower'
                else:
                    self.pwmode = 'upper'
                return 1
        else:
			print "parameter error!"
			return 0
    def quit(self):
        self.driver.quit()

class mobileBank(phoneBase):
    def __init__(self, host, port, platform, version, deviceName, noReset, unicodeK, resetK, \
        appPackage, appActivity, appPath, xloginID, xpwID, xloginBtn):
        phoneBase.__init__(self, host, port, platform, version, deviceName, noReset, unicodeK, resetK, \
            appPackage, appActivity, appPath, xloginID, xpwID, xloginBtn) 
        self.xpath_mainpage_tag = "//TextView[@id='tv_showLgtime']"

    def checkIfInMainPage(self):
        # in main page, mobile bank will show log time, check whether in main page via 'tv_showLgtime'
        try:
            self.driver.find_element_by_xpath(self.xpath_mainpage_tag)
        except NoSuchElementException as e:
            print "mobileBank::checkIfInMainPage: ", e
            return 0
        else:
            return 1
    def addInnerAcct(self, name, acct):
        ret = self.checkIfInMainPage()  
        if ret == 0:
            print "mobileBank:addInnerAcct: mobile bank not in main page, switch to it first!"
            return 0
        else:
            ele = self.driver.find_elements_by_xpath("//ImageView[@id='iv_mobilebank']")
            ele[2].click()
            time.sleep(100)
            ele = self.driver.find_element_by_xpath("//Button[@id='title_bar_left_button']")
            ele.click()
            time.sleep(2)
            return 1


if __name__ == '__main__':
    mbank = mobileBank('localhost', 4723, "Android", "4.4.2", "Selendroid", True, True, True, \
        "com.yitong.fjnx.mbank.android", ".Splash", "/Volumes/Mobile/Mobile Test/FJNX_MBANK.apk", \
        "//LinearLayout[@id='ll_account']", "//LinearLayout[@id='ll_pwd']", "//Button[@id='login_btn_login']")
    mbank.login("test","passwd")
    mbank.addInnerAcct("test","622")
    print u"完成"
