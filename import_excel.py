import os, sys, sqlite3, string
from xlrd import open_workbook

cx = sqlite3.connect("db.sqlite3")
cu = cx.cursor()

book = open_workbook('category.xlsx', encoding_override="utf-8")
for s in book.sheets():
   print("sheet:", s.name)

try:
   sheet = book.sheet_by_name('Sheet2')
except:
   print("no sheet in %s index = 1" % excel_name)

row_count = sheet.nrows
column_count = sheet.ncols

row_list =[]
print("开始导入------------------->>>>>>>")
for i in range(1, row_count):
   title = sheet.cell(i, 0).value
   name = sheet.cell(i, 1).value
   code = sheet.cell(i, 2).value

   print("%s, %s, %s" % (title, name, code))

   cx.execute("insert into archive_category(title, name, code) values ('%s', '%s', '%s')" % (title, name, code))
   cx.commit()
cu.close()
print("导入完成------------------->>>>>>>")
