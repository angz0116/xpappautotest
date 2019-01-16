# -*- coding:utf-8 -*-
"""
@project = xpappautotest
@file = pageObject
@author = zhaoai
@create_time = 2019-1-16 11:46
"""
from appium import webdriver
from selenium.webdriver.common.by import By

import logging
import time
import unittest


class PageObject(unittest.TestCase):

	def setUp(self, device, app):
		super().setUp()
		self.options = {
			'platformName': device['platform'],
			'platformVersion': device['version'],
			'deviceName': device['conn'],
			'appPackage': app['app_package'],
			'app': app['app'],
			'appActivity': app['app_activity']
		}
		self.driver = webdriver.Remote('http://' + device['host'] + ':' + str(device['port']) + '/wd/hub', self.options)

	def tearDown(self):
		self.driver.remove_app(self.options['appPackage'])
		assert(not self.driver.is_app_installed(self.options['appPackage']))
		self.driver.quit()

	def find_element(self, by, value):
		res = None
		try:
			res = self.driver.find_element(by, value)
		except Exception as err:
			logging.warning(err)
		finally:
			pass
		return res

	def find_element_by_id(self, value):
		return self.find_element(By.ID, value)

	def find_element_by_xpath(self, value):
		return self.find_element(By.XPATH, value)

	def find_element_until(self, by, value, timeout=60):
		res = self.find_element(by, value)
		i = 0
		while (res is None) and (i < timeout):
			time.sleep(1)
			i = i + 1
			res = self.find_element(by, value)
		return res
	def find_element_by_xpath_until(self, value, timeout=60):
		return self.find_element_until(By.XPATH, value, timeout)

	def find_element_by_id_until(self, value, timeout=60):
		return self.find_element_until(By.ID, value, timeout)

	def swipe(self, dir='l2r', limit=0.1, pos=0.5, t=1000):
		screen_size = self.driver.get_window_size()
		width = screen_size['width']
		height = screen_size['height']
		dir = dir.lower()
		x0, y0, x1, y1 = 0, 0, 0, 0
		if ('l2r' == dir):
			x0, y0, x1, y1 = width * limit, height *pos, width*(1-limit), height *pos
		elif ('r2l' == dir):
			x0, y0, x1, y1 = width*(1-limit), height *pos, width*limit, height *pos
		elif ('t2b' == dir):
			x0, y0, x1, y1 = width*pos, height*limit, width *pos, height*(1-limit)
		elif('b2t' == dir):
			x0, y0, x1, y1 = width *pos, height* limit, width*pos, height *(1-limit)
		self.driver.swipe(x0, y0, x1, y1, t)

	def is_available(self, by, value, timeout=60):
		return self.find_element_until(by, value, timeout) is not None

	def is_available_by_id(self, value, timeout=60):
		return self.is_available(By.ID, value, timeout)

	def is_available_by_xpath(self, value, timeout=60):
		return self.is_available(By.XPATH, value, timeout)