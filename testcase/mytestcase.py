# -*- coding:utf-8 -*-
"""
@project = xpappautotest
@file = mytestcase
@author = zhaoai
@create_time = 2019-1-16 11:51
"""
import unittest
from config.config import ANDROID5
zhihu = {
	'app_package': 'com.zhihu.android',
	'app': 'd:/zhihu.apk',
	'app_activity': 'com.zhihu.android.app.ui.activity.LauncherActivity'
}

baidu = {
	'app_package': 'com.baidu.searchbox',
	'app': 'd:/baidu.apk',
	'app_activity': 'com.baidu.searchbox.SplashActivity'
}

yxk = {
	'app_package': 'com.jieyue.xbxx',
	'app': 'd:/NMKP_default_channel_STG_v1.2.5_20181225101806_0.apk',
	'app_activity': 'com.jieyue.xbxx.MainActivity'
}

device = ANDROID5
app = yxk

class MyTestCase(unittest.TestCase):
	def test_something(self):
		self.assertEqual(True, False)


if __name__ == '__main__':
	unittest.main()
