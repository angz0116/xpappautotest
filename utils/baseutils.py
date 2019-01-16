# -*- coding:utf-8 -*-
"""
@project = xpappautotest
@file = baseutils
@author = zhaoai
@create_time = 2019-1-16 11:35
"""
import cx_Oracle
import glob
from openpyxl import load_workbook
import time

def get_func(f):
	def _wrapper(*argc, **kwargs):
		print("======================== running", f.__name__, "========================")
		f(*argc, **kwargs)
	return _wrapper

class baseDB(object):

	def __init__(self, dbconf, dbtype='oracle'):
		self.db = None
		self.cursor = None
		try:
			if 'oracle' == dbtype:
				self.db = cx_Oracle.connect(dbconf['username'] + '/' + dbconf['password'] + '@' + dbconf['host'] + ':' + str(dbconf['port']) + '/' + dbconf['dbname'])
				self.cursor = self.db.cursor()
		except Exception as err:
			print(err)
		finally:
			pass

	def execute(self, sql):
		sql = sql.strip().lower()
		while sql.endswith(';'):
			sql = sql[:-1]
		rs = None
		try:
			rs = self.cursor.execute(sql)
		except Exception as err:
			print(err)
		finally:
			pass
		res = None
		act = sql.split()[0]
		if ('select' == act):
			if rs is not None:
				res = rs.fetchall()
		elif ('insert' == act):
			self.cursor.commit()
		# todo: execute_many / execute
		return res

	def __del__(self):
		self.cursor.close()
		self.db.close()

	def download_file(fn_pattern, timeout=60):

		files = []
		i = 0
		while ((i < timeout) and ([] == files)):
			time.sleep(1)
			files = glob.glob(fn_pattern)
			i = i + 1
		files.sort()
		return files[-1]


	def comp_cells_xlsx(cells, xlsx_filename, tabname=None, head_row=0, key_col='A'):
		res = True

		wb = load_workbook(filename=xlsx_filename)
		sheet = wb.worksheets[0]
		if tabname is not None:
			sheet = wb[tabname]
		keys = None
		rows = []
		i = 1

		for row in sheet.rows:
			if(i < head_row):
				i = i + 1
			else:
				if (keys is None):
					keys = [v.value for v in row]
				else:
					rows.append([r.value for r in row])

		key = keys[ord(key_col)-ord('A')]
		xrows = {}
		for value in cells.values():
			tmp_v = {}
			for k in value:
				if (k != key):
					tmp_v[k] = value[k].text
			xrows[value[key].text] = tmp_v

		for row in rows:
			for i in range(len(keys)):
				orgname = row[ord(key_col) - ord('A')]
				xrow = xrows[orgname]
				if(keys[i] in xrow):
					res = res and (row[i] == xrow[keys[i]])
		return res

if ('__main__' == __name__):
	ora = baseDB('172.18.100.126', 1521, 'core0915', 'core0915', 'testdb')
	sql = 'select count(*) from t_c_at_repay_plan'
	res = ora.execute(sql)
	print(res)

