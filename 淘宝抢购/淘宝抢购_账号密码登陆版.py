# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
淘宝秒杀脚本，账号密码登录版

实现原理：
1. 提示：请输入抢购时间，格式如(2018-09-06 11:20:00.000000)。（输入完数字需要摁回车键）
2. 自动打开淘宝网站
3. 自动找到"亲，请登录"按钮，并点击（点击后会跳到登录页）
4. 自动找到账号和密码输入框，并填充账号密码
5. 自动找到"登录"按钮并点击，如果登录成功则自动打开购物车页面（此处会自动登录失败，因为有拖动滑块验证，需要用户手动操作）
6. 提示：到时间自动勾选购物车请输入“1”，否则输入“2”。（输入完数字需要摁回车键）
7. 如果用户输入1，则会自动全选购物车；输入2，则需要用户手动勾选
8. 轮询判断当前时间是否大于第一步输入的抢购时间，是的话则自动找到"结 算"按钮并点击（点完会跳到提交订单页面）
9. 自动找到"提交订单"按钮并点击
10. 结束
"""
import getpass

from selenium import webdriver
import datetime
import time


def input_account(username, password):
    time.sleep(3)
    # 选择密码登录
    # if browser.find_element_by_id("J_Quick2Static"):
    #     browser.find_element_by_id("J_Quick2Static").click()
    # time.sleep(3)

    # 用户名输入
    # if browser.find_element_by_name("fm-login-id"):
    #     for i in username:
    #         browser.find_element_by_name("fm-login-id").send_keys(i)
    #         time.sleep(0.5)
    if browser.find_element_by_id("fm-login-id"):
        for i in username:
            browser.find_element_by_id("fm-login-id").send_keys(i)
            # time.sleep(0.5)
    time.sleep(3)

    # 密码输入
    # if browser.find_element_by_name("fm-login-password"):
    #     for j in password:
    #         browser.find_element_by_name("fm-login-password").send_keys(j)
    if browser.find_element_by_id("fm-login-password"):
        for j in password:
            browser.find_element_by_id("fm-login-password").send_keys(j)
            # time.sleep(0.5)
    time.sleep(3)

    # 点击登录按钮(由于需要人工拖动滑块验证，所以实际上不会自动登录成功）
    if browser.find_element_by_css_selector(".fm-button.fm-submit.password-login"):
        browser.find_element_by_css_selector(".fm-button.fm-submit.password-login").click()


def login(username, password):
    # 打开淘宝登录页，并进行扫码登录
    browser.get("https://www.taobao.com")
    time.sleep(3)
    if browser.find_element_by_link_text("亲，请登录"):
        browser.find_element_by_link_text("亲，请登录").click()
    input_account(username, password)
    browser.get("https://cart.taobao.com/cart.htm")
    time.sleep(3)

    now = datetime.datetime.now()
    print('login success:', now.strftime('%Y-%m-%d %H:%M:%S'))


def buy(times, choose):
    # 点击购物车里全选按钮
    if choose == 1:
        try:
            if browser.find_element_by_id("J_SelectAll2"):
                browser.find_element_by_id("J_SelectAll2").click()
        except:
            try:
                if browser.find_element_by_id("J_SelectAll1"):
                    browser.find_element_by_id("J_SelectAll1").click()
            except:
                print("购物车竟然是空的！！！")
                return
    elif choose == 2:
        print("请手动勾选需要购买的商品")

    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        # 对比时间，时间到的话就点击结算
        if now > times:
            # if choose == 1:
            #     while True:
            #         try:
            #             if browser.find_element_by_id("J_SelectAll2"):
            #                 browser.find_element_by_id("J_SelectAll2").click()
            #                 break
            #         except:
            #             print("找不到购买按钮")
            # 点击结算按钮
            while True:
                try:
                    if browser.find_element_by_link_text("结 算"):
                        browser.find_element_by_link_text("结 算").click()
                        print("结算成功")
                        break
                except:
                    try:
                        if browser.find_element_by_id("J_Go"):
                            browser.find_element_by_id("J_Go").click()
                            print("结算成功")
                            break
                    except:
                        pass
            while True:
                try:
                    if browser.find_element_by_link_text('提交订单'):
                        browser.find_element_by_link_text('提交订单').click()
                        now1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                        print("抢购成功时间：%s" % now1)
                        return
                except:
                    print("再次尝试提交订单")
        time.sleep(0.01)


if __name__ == "__main__":
    times = input("请输入抢购时间，格式如(2018-09-06 11:20:00.000000):")
    # 时间格式："2018-09-06 11:20:00.000000"

    # 先下载chromedriver（https://chromedriver.storage.googleapis.com/index.html?path=2.44/），然后指定其所在路径
    browser = webdriver.Chrome('/Users/shewenbiao/Downloads/ChromeDriver/2.44/chromedriver')

    # 使用chromedriver 2.33版本，调用browser.maximize_window()会报以下错误
    # selenium.common.exceptions.WebDriverException: Message: unknown error:
    # failed to change window state to maximized, current state is normal
    # browser.maximize_window()
    username = input("请输入用户名：")
    password = getpass.getpass("请输入密码：")  # 输入密码不可见
    login(username, password)
    choose = int(input("到时间自动勾选购物车请输入“1”，否则输入“2”："))
    buy(times, choose)
