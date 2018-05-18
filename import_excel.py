# coding=utf-8
import os, sys, sqlite3, string
from xlrd import open_workbook

def create_heading(name, chinese_code, code, sequence):
   script = "insert into archive_heading(name, chinese_code, code, sequence) values ('%s', '%s', '%s', %s)" % (name, chinese_code, code, sequence)
   cx.execute(script)

def create_category(header_id, name, code, sequence):
   script = "insert into archive_category(heading_id, name, code, sequence) values (%s, '%s', '%s', %s)" % (header_id, name, code, sequence)
   cx.execute(script)

def create_archive(category_id, name, comment, description, sequence):
   script = "insert into archive_archive(category_id, name, comment, description, sequence) values (%s, '%s', '%s', '%s', %s)" % (category_id, name, comment, description, sequence)
   cx.execute(script)

book = open_workbook('Document/category.xlsx', encoding_override="utf-8")
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

with sqlite3.connect("db.sqlite3") as cx:
   cu = cx.cursor()

   cx.execute("delete from archive_heading")
   cx.execute("delete from archive_category")
   cx.execute("delete from archive_archive")

   cx.commit()

   create_heading('履历材料', '一', '1', 1)
   create_heading('自传材料', '二', '2', 2)
   create_heading('鉴定、考察、考核材料', '三', '3', 3)
   create_heading('学历和评聘专业技术职务材料', '四', '4', 4)
   create_heading('政治历史审查材料', '五', '5', 5)
   create_heading('参加党、团及民主党派材料', '六', '6', 6)
   create_heading('奖励材料', '七', '7', 7)
   create_heading('处分材料', '八', '8', 8)
   create_heading('录用任免工资待遇退休材料', '九', '9', 9)
   create_heading('其他参考材料', '十', '10', 10)
   create_heading('承办材料', '十一', '11', 11)
   create_heading('影印参考材料', '十二', '12', 12)
   create_heading('参考材料', '十三', '13', 13)

   cx.commit()

   heading_dictionary = dict()
   cu.execute("select id, code from archive_heading")
   rows = cu.fetchall()
   for row in rows:
      heading_code = row[1]
      heading_id = row[0]
      heading_dictionary[heading_code] = heading_id

   heading_id = heading_dictionary['1']
   create_category(heading_dictionary['1'], '第一类履历类', '1', 101)
   create_category(heading_dictionary['2'], '第二类自传类', '2', 201)
   create_category(heading_dictionary['3'], '第三类鉴定类', '3', 301)
   create_category(heading_dictionary['4'], '第四类专业类4-1学历材料', '4-1', 401)
   create_category(heading_dictionary['4'], '第四类专业类4-2专业技术材料', '4-2', 402)
   create_category(heading_dictionary['4'], '第四类专业类4-3科研成果', '4-3', 403)
   create_category(heading_dictionary['4'], '第四类专业类4-4培训材料', '4-4', 404)
   create_category(heading_dictionary['5'], '第五类政历类', '5', 501)
   create_category(heading_dictionary['6'], '第六类党团类', '6', 601)
   create_category(heading_dictionary['7'], '第七类奖励类', '7', 701)
   create_category(heading_dictionary['8'], '第八类处分类', '8', 801)
   create_category(heading_dictionary['9'], '第九类任免类9-1工资', '9-1', 901)
   create_category(heading_dictionary['9'], '第九类任免类9-2任免', '9-2', 902)
   create_category(heading_dictionary['9'], '第九类任免类9-3出国', '9-3', 903)
   create_category(heading_dictionary['9'], '第九类任免类9-4其他', '9-4', 904)
   create_category(heading_dictionary['10'], '第十类其他', '10', 1001)
   create_category(heading_dictionary['11'], '第十一类承办材料', '11', 1101)
   create_category(heading_dictionary['12'], '第十二类参考材料（影印）', '12', 1201)
   create_category(heading_dictionary['13'], '第十三类参考材料（入党材料）', '13', 1301)

   cx.commit()

   category_dictionary = dict()
   cu.execute("select id, code from archive_category")
   rows = cu.fetchall()
   for row in rows:
      category_code = row[1]
      category_id = row[0]
      category_dictionary[category_code] = category_id

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
            code2 = 1

         if (previous_code == code):
            code3 = code3 + 1
         else:
            code3 = 1

         sequence = code1 *1000000 + code2 * 10000 + code3 * 10
         category_id = category_dictionary[code]
         print("%s, %s, %s, %d" % (title, name, code, sequence))
         create_archive(category_id, name, comment, description, sequence)
         previous_code = code

   cx.commit()
   cu.close()

print("导入完成------------------->>>>>>>")


