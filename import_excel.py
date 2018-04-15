import os, sys, sqlite3, string
from xlrd import open_workbook

cx = sqlite3.connect("db.sqlite3")
cu = cx.cursor()

book = open_workbook('category.xlsx', encoding_override="utf-8")
for s in book.sheets():
   print("sheet:", s.name)

try:
   sheet = book.sheet_by_name('Sheet1')
except:
   print("no sheet in %s index = 1" % excel_name)

row_count = sheet.nrows
column_count = sheet.ncols

row_list =[]
print("开始导入------------------->>>>>>>")
previous_code = ""
code1 = 1
code2 = 1
code3 = 1
cx.execute("delete from archive_category")
cx.commit()
for i in range(1, row_count):
   title = sheet.cell(i, 0).value
   name = sheet.cell(i, 1).value
   comment = sheet.cell(i, 2).value
   description = sheet.cell(i, 3).value
   code = sheet.cell(i, 5).value
   if (len(name) > 0):
      if not (isinstance(code, str)):
         code = str(int(code))
      print ("%s, %s, %s, %s, %s" % (title, name, comment, description, code))

      if ('-' in code):
         code_list = code.split('-')
         code1 = int(code_list[0])
         code2 = int(code_list[1])
      else:
         code1 = int(code)
         code2 = 0

      if (previous_code == code):
         code3 = code3 + 1
      else:
         code3 = 1

      sequence = code1 *1000000 + code2 * 10000 + code3 * 10

      print("%s, %s, %s, %d" % (title, name, code, sequence))

      script = "insert into archive_category(title, name, code, comment, description, sequence) values ('%s', '%s', '%s', '%s', '%s', %s)" % (title, name, code, comment, description, sequence)

      cx.execute(script)
      cx.commit()
      previous_code = code

cu.close()
print("导入完成------------------->>>>>>>")
