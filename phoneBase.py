# -*- coding:utf-8 -*-
# author: chaonin
# date:   2015/2/15
from appium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException

class phoneBase:
    def __init__(self, host, port, platform, version, deviceName, noReset, unicodeK, resetK, \
        appP_bdId, appA_udid, appPath, xloginID, xpwID, xloginBtn):
        self.pwmode = 'lower'

        self.desired_caps = {}
        self.desired_caps['platformName'] = platform
        self.desired_caps['platformVersion'] = version
        self.desired_caps['noReset'] = noReset
        self.desired_caps['unicodeKeyboard'] = unicodeK
        self.desired_caps['resetKeyboard'] = resetK
        self.desired_caps['app'] = appPath
        self.desired_caps['deviceName'] = deviceName # Android - Senlendroid mode, iOS - iPhone name
        if platform == "Android":
            self.desired_caps['appPackage'] = appP_bdId
            self.desired_caps['appActivity'] = appA_udid
        if platform == "iOS":
            self.desired_caps['bundleId'] = appP_bdId
            self.desired_caps['udid'] = appA_udid

        self.xpath_login_id = xloginID
        self.xpath_pw_id = xpwID
        self.xpath_login_btn = xloginBtn

        url = "http://" + host + ":" + str(port) + "/wd/hub"
        self.driver = webdriver.Remote(url, self.desired_caps)
        time.sleep(5)

    def login(self, account, pw):
        ele = self.driver.find_element_by_xpath(self.xpath_login_id)
        # iOS, U need switch to qwerty keyboard to input Letters
        if self.desired_caps['platformName'] == "iOS":
            ele.click()
            ele1 = self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[4]/UIAKeyboard[1]/UIAButton[4]")
            ele1.click()
        ele.send_keys(account)
        ele = self.driver.find_element_by_xpath(self.xpath_pw_id)
        ele.click()
        if self.desired_caps['platformName'] == "iOS":
            self.inputpw2(pw)
        else:
            self.inputpw(pw)
        # iOS mbank need not to press login again
        if self.desired_caps['platformName'] == "Android":
            ele = self.driver.find_element_by_xpath(self.xpath_login_btn)
            ele.click()
        time.sleep(5)

    def inputpw(self, pw):
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
        # input the OK button for end
        ele = self.driver.find_element_by_xpath("//Button[@id='digitkeypad_oknew']")
        ele.click()
        time.sleep(2)
    def inputpw2(self, pw):
        for letter in pw:
            print letter
            if letter >= 'a' and letter <= 'z':
                if self.pwmode != 'lower':
                    self.switchmode2('lower')
                ele = self.driver.find_element_by_name(letter)
                ele.click()
            elif letter >= 'A' and letter <= 'Z':
                if self.pwmode != 'upper':
                    self.switchmode2('upper')
                ele = self.driver.find_element_by_name(letter)
                ele.click()
            elif letter >= '0' and letter <= '9':
                if self.pwmode != 'digit':
                    self.switchmode2('digit')
                ele = self.driver.find_element_by_name(letter)
                ele.click()
            else:
                print "unsupport sign now!"
                return 0
        # input OK button for end
        ele = self.driver.find_element_by_name("确定")
        ele.click()
        time.sleep(2)
                
    def switchmode(self, mode):
        #mode: digit/upper/lower/sign
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
                # keypad_abc_ABC (letter mode) | keypad_num_new_abc (digit mode) | have bug !!
                #ele = self.driver.find_element_by_xpath("//Button[@id='keypad_num_new_abc']")
                print "could not found letter-mode switch key, error!"
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
    def switchmode2(self, mode):
        #mode: digit/lower/upper/sign
        ele = 'null'
        if mode == 'upper':
            try:#check if in lower mode
                ele = self.driver.find_element_by_name('q')
            except NoSuchElementException as e:
                print "phoneBase::switchmode2: not in mode \'lower\', ", e
            if ele != 'null': 
                print "debug:: found in lower mode"
                ele = self.driver.find_element_by_name("key upper iphone")
                ele.click()
                self.pwmode = 'upper'
                return 1

        elif mode == 'lower':
            try:#check if in upper mode
                ele = self.driver.find_element_by_name('Q')
            except NoSuchElementException as e:
                print "phoneBase::switchmode2: not in mode \'lower\', ", e
            if ele != 'null':
                print "debug:: found in upper mode"
                ele = self.driver.find_element_by_name("key upper iphone")
                ele.click()
                self.pwmode = 'upper'
                return 1

        elif mode == 'digit':
            try:#check if in upper mode
                ele = self.driver.find_element_by_name('Q')
            except NoSuchElementException as e:
                print "phoneBase::switchmode2: not in mode \'upper\', ", e
            if ele != 'null':
                ele = self.driver.find_element_by_name('123')
                ele.click()
                self.pwmode = 'digit'
                return 1

            try:#check if in lower mode
                ele = self.driver.find_element_by_name('q')
            except NoSuchElementException as e:
                print "phoneBase::switchmode2: not in mode \'lower\', ", e
            if ele != 'null':
                ele = self.driver.find_element_by_name('123')
                ele.click()
                self.pwmode = 'digit'
                return 1
        elif mode == 'sign':
            print "on building..."
            return 1
        else:
            print "unsupport mode!"
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
    #mbank = mobileBank('localhost', 4723, "Android", "4.4.2", "Selendroid", True, True, True, \
    #    "com.yitong.fjnx.mbank.android", ".Splash", "/Volumes/Mobile/Mobile Test/FJNX_MBANK.apk", \
    #    "//LinearLayout[@id='ll_account']", "//LinearLayout[@id='ll_pwd']", "//Button[@id='login_btn_login']")
    mbank = mobileBank('localhost', 4723, "iOS", "9.2.1", "Dream(9.2.1)", True, True, True, \
        "com.chaonin.mbank", "f5951894f37eac2e91898a8a2f8cf1e6e059b9cc", "/Volumes/Mobile/Mobile Test/FJNXBankForIphone.app", \
        "//UIAApplication[1]/UIAWindow[1]/UIATextField[1]", "//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[1]", "//UIAApplication[1]/UIAWindow[1]/UIAButton[5]")
    mbank.login("test","test")
    #mbank.addInnerAcct("test","622")
    print "done"
    mbank.quit()
