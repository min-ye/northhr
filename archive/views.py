from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.contrib import auth
from django.http    import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
import xlwt 
import logging
import datetime
import time
import os
import io
from io import StringIO
from archive.models import Person, Register, Log, Category, PersonLog
from archive.forms import PersonForm, RegisterForm

logger = logging.getLogger('django')

def layout(request):
   if request.method == 'POST':
      form = PersonForm(request.POST)

   else:
      form = PersonForm()
   return render_to_response('layout.html', { 'form': form })

#def index(request):
#   if request.user.is_authenticated:
#      return render_to_response('index.html', { 'user': request.user })
#   else:
#      return HttpResponseRedirect('/login')  

def login(request):
   username = request.POST.get('inputUserID', '')
   password = request.POST.get('inputPassword', '')
   if (username != '' and password != ''):
      user = auth.authenticate(username = username, password = password)  
      if user is not None:  
         auth.login(request, user)  
         return HttpResponseRedirect('/person/search/')  
      else:
         return render_to_response('login.html', { 'message': '用户名或密码不正确' })
   else:
      return render_to_response('login.html', { 'message': '请输入用户名和密码' })

def change_password(request):
   if request.method == 'POST':
      form = PasswordChangeForm(request.user, request.POST)
      if form.is_valid():
         user = form.save()
         update_session_auth_hash(request, user)  # Important!
         messages.success(request, 'Your password was successfully updated!')
         return redirect('change_password')
      else:
         messages.error(request, 'Please correct the error below.')
   else:
      form = PasswordChangeForm(request.user)
   return render(request, 'change_password.html', {
      'form': form
   })

def logout(request):
    auth.logout(request)  
    return render_to_response('login.html', { 'message': '退出登录成功' })

'''
def register(request, person_id):
   if request.user.is_authenticated:
      step = request.POST.get('step', '')

      if (step == ''):
         return render_to_response('register.html', { 'user': request.user, 'step': 1 })
      else:
         if (step == '1'):
            person_id_number = request.POST.get('person_id_number', '')
            if (person_id_number == ''):
               message = "请输入身份证号."
               return render_to_response('register.html', { 'user': request.user, 'step': 1, 'message': message })
            elif (len(person_id_number) != 18):
               message = "请输入18位身份证号."
               return render_to_response('register.html', { 'user': request.user, 'step': 1, 'message': message })
            else:
               try:
                  person = Person.objects.get(id_number = person_id_number)
                  message = "身份证号已存在."
                  return render_to_response('register.html', { 'user': request.user, 'step': 3, 'person': person, 'message': message })
               except Person.DoesNotExist:
                  message = "身份证号不存在.请输入姓名."
                  person = Person(id_number = person_id_number, name = '')
                  return render_to_response('register.html', { 'user': request.user, 'step': 2, 'person': person, 'message': message })

         elif (step == '2'):
            person_id_number = request.POST.get('person_id_number', '')
            person_name = request.POST.get('person_name', '')
            logger.info(person_id_number)
            logger.info(person_name)
            if (person_id_number == ''):
               message = "信息丢失, 请重新输入身份证号."
               return render_to_response('register.html', { 'user': request.user, 'step': 1, 'message': message })
            elif (person_name == ''):
               message = "姓名不能为空."
               person = Person(id_number = person_id_number, name = '')
               return render_to_response('register.html', { 'user': request.user, 'step': 2, 'person': person, 'message': message })
            else:
               message = '新记录已保存. 请输入材料关键字.'
               person = Person(id_number = person_id_number, name = person_name)
               person.save()
               return render_to_response('register.html', { 'user': request.user, 'step': 3, 'person': person, 'message': message })

         elif (step == '3'):
            person_id_number = request.POST.get('person_id_number', '')
            person_name = request.POST.get('person_name', '')
            person_id = request.POST.get('person_id', '')
            category_name = request.POST.get('category_name', '')
            try:
               person_id = int(person_id)
               person = Person(id = person_id, name = person_name, id_number = person_id_number)
            except:
               message = "信息丢失, 请重新输入身份证号."
               return render_to_response('register.html', { 'user': request.user, 'step': 1, 'message': message })
            else:
               if (category_name == ''):
                  message = "请输入材料关键字."
                  return render_to_response('register.html', { 'user': request.user, 'step': 3, 'person': person, 'message': message })
               else:
                  category_list = Category.objects.filter(name__contains = category_name)
                  if ( len(category_list) == 0 ):
                     message = "未找到相关记录."
                     return render_to_response('register.html', { 'user': request.user, 'step': 3, 'person': person, 'message': message })
                  else:
                     message = "请选择材料并输入页数."
                     return render_to_response('register.html', { 'user': request.user, 'step': 4, 'person': person, 'category_list': category_list, 'message': message })

         elif (step == '4' or step == '5'):
            person_id_number = request.POST.get('person_id_number', '')
            person_name = request.POST.get('person_name', '')
            person_id = request.POST.get('person_id', '')
            category_id = request.POST.get('category_id', '')
            quantity = request.POST.get('quantity', '')
            try:
               person_id = int(person_id)
               person = Person(id = person_id, name = person_name, id_number = person_id_number)
            except:
               message = "信息丢失, 保存失败, 请重新输入身份证号."
               return render_to_response('register.html', { 'user': request.user, 'step': 1, 'message': message })
            else:
               try:
                  category_id = int(category_id)
               except:
                  message = "信息丢失, 保存失败, 请重新输入材料关键字."
                  return render_to_response('register.html', { 'user': request.user, 'step': 3, 'person': person, 'message': message })

               try:
                  category = Category.objects.get(id = category_id)
               except Category.DoesNotExist:
                  message = "未找到相关记录, 保存失败, 请重新输入材料关键字."
                  return render_to_response('register.html', { 'user': request.user, 'step': 3, 'person': person, 'message': message })

               try:
                  quantity = int(quantity)
               except:
                  message = "在页数字段请输入数字."
                  return render_to_response('register.html', { 'user': request.user, 'step': 5, 'person': person, 'category': category, 'message': message })

               try:
                  register = Register(user = request.user, person = person, category = category, quantity = quantity)
                  register.save()
                  log = Log(user = request.user, person = person, category = category, quantity = quantity, operation = 'create')
                  log.save()
                  message = "保存成功."
                  return render_to_response('register.html', { 'user': request.user, 'step': 6, 'person': person, 'category': category, 'register': register, 'message': message })
               except:
                  message = "保存失败."
                  return render_to_response('register.html', { 'user': request.user, 'step': 1, 'message': message })

   else:
      return render_to_response('login.html', { })
'''

'''
def category(request):
   if request.user.is_authenticated:
      if request.method == 'POST':
         register_id = request.POST.get('register_id', '')
         try:
            register_id = int(register_id)
            register = Register.objects.get(id = register_id)
            register.delete()
            log = Log(user = request.user, person = register.person, category = register.category, quantity = register.quantity, operation = 'delete')
            log.save()
            message = "删除成功."
         except:
            message = "删除失败."
         person_information = request.GET.get('person_information', '')
         if (person_information != ''):
            if (hasNumber(person_information)):
               register_list = Register.objects.filter(person__id_number__contains = person_information)
            else:
               register_list = Register.objects.filter(person__name__contains = person_information)
            return render_to_response('category.html', { 'user': request.user, 'information': person_information, 'register_list': register_list, 'message': message} )
         else:
            return render_to_response('category.html', { 'user': request.user, 'message': message} )
      else:
         person_information = request.GET.get('person_information', '')
         if (person_information != ''):
            if (hasNumber(person_information)):
               register_list = Register.objects.filter(person__id_number__contains = person_information)
               message = "查找身份证 '%s'" % (person_information)
            else:
               register_list = Register.objects.filter(person__name__contains = person_information)
               message = "查找姓名 '%s'" % (person_information)
            return render_to_response('category.html', { 'user': request.user, 'information': person_information, 'register_list': register_list, 'message': message} )
         else:
            message = "请输入姓名查找相关的记录"
            return render_to_response('category.html', { 'user': request.user, 'message': message })
   else:
      return render_to_response('login.html', { })
'''

def log(request, person_id):
   if request.user.is_authenticated and request.user.is_staff:
      messages = []
      try:
         person = Person.objects.get(id = person_id)
      except Person.DoesNotExist:
         url = "/person/unknown/"
         return HttpResponseRedirect(url)
      log_list = Log.objects.filter(person__id__contains = person_id).order_by("operation_date", "operation_time")
         
      return render_to_response('log.html', { 'user': request.user, 'person': person, 'log_list': log_list, 'messages': messages} )
   else:
      url = "/login/"
      return HttpResponseRedirect(url)

def personlog(request, person_id):
   if request.user.is_authenticated and request.user.is_staff:
      messages = []
      try:
         person = Person.objects.get(id = person_id)
      except Person.DoesNotExist:
         url = "/person/unknown/"
         return HttpResponseRedirect(url)
      log_list = PersonLog.objects.filter(person__id__contains = person_id).order_by("operation_date", "operation_time")
         
      return render_to_response('personlog.html', { 'user': request.user, 'person': person, 'log_list': log_list, 'messages': messages} )
   else:
      url = "/login/"
      return HttpResponseRedirect(url)

#def form_template_1(request):
#   return render_to_response('form_template_1.html', { })

def person_detail(request, id):
   if request.user.is_authenticated:
      messages = []
      try:
         person = Person.objects.get(id = id)
      except Person.DoesNotExist:
         url = "/person/unknown/"
         return HttpResponseRedirect(url)

      if request.method == 'POST':
         register_id = request.POST.get('register_id', '')
         try:
            register_id = int(register_id)
            register = Register.objects.get(id = register_id)
            category_name = register.category.name
            document_date = register.document_date
            register.delete()
            log = Log(user = request.user, person = register.person, category = register.category, quantity = register.quantity, document_date = register.document_date, create_date = register.create_date, comment = register.comment, operation = 'delete')
            log.save()
            date = document_date.strftime("%Y-%m-%d")
            message = "%s %s 删除成功." % (category_name, date)
            messages.append(message)
         except:
            messages.append("删除失败.")
         
      register_list = Register.objects.filter(person__id = id).order_by("document_date", "category__sequence")
      return render_to_response('person_detail.html', { 'user': request.user, 'person': person, 'registers': register_list, 'messages': messages })
   else:
      url = "/login/"
      return HttpResponseRedirect(url)

def person_unknown(request):
   return render_to_response('person_unknown.html', { 'user': request.user })

def person_edit(request, id):
   if request.user.is_authenticated:
      messages = []
      try:
         person = Person.objects.get(id = id)
      except Person.DoesNotExist:
         url = "/person/unknown/"
         return HttpResponseRedirect(url)
      if request.method == 'POST':
         form = PersonForm(request.POST)
         if form.is_valid():
            data = form.cleaned_data
            try:
               person = Person(id = id, name = data['name'], code = data['code'], unit = data['unit'], serial = data['serial'], id_number = data['id_number'])
               person.save()
               personLog = PersonLog(user = request.user, 
                  person = person,
                  name = person.name, 
                  code = person.code, 
                  unit = person.unit, 
                  serial = person.serial,
                  id_number = person.id_number,
                  operation = 'update')
               personLog.save()
               messages.append('保存成功')
               url = "/person/detail/%s" % (id)
               return HttpResponseRedirect(url)
            except:
               messages.append('保存失败')
         else:
            messages.append('保存失败，请检查输入数据')
         return render_to_response('person_edit.html', { 'user': request.user, 'form': form, 'messages': messages })
      else:
         messages.append('找到记录')
         form = PersonForm(initial={'name': person.name, 'code': person.code, 'unit': person.unit, 'serial': person.serial, 'id_number': person.id_number })
         return render_to_response('person_edit.html', { 'user': request.user, 'form': form, 'messages': messages })
   else:
      url = "/login/"
      return HttpResponseRedirect(url)

def person_new(request):
   if request.user.is_authenticated:
      messages = []
      if request.method == 'POST':
         form = PersonForm(request.POST)
         if form.is_valid():
            data = form.cleaned_data
            try:
               person = Person(name = data['name'], code = data['code'], unit = data['unit'], serial = data['serial'], id_number = data['id_number'])
               person.save()
               personLog = PersonLog(user = request.user, 
                  person = person,
                  name = person.name, 
                  code = person.code, 
                  unit = person.unit, 
                  serial = person.serial,
                  id_number = person.id_number,
                  operation = 'create')
               personLog.save()
               messages.append("保存成功")
               return render_to_response('person_edit.html', { 'user': request.user, 'person': person, 'messages': messages })
            except:
               messages.append("保存失败")
               return render_to_response('person_edit.html', { 'user': request.user, 'form': form, 'messages': messages })
         else:
            messages.append("数据不正确")
            return render_to_response('person_edit.html', { 'user': request.user, 'form': form, 'messages': messages })
      else:
         name = request.GET.get('name', '')
         code = request.GET.get('code', '')
         unit = request.GET.get('unit', '')
         serial = request.GET.get('serial', '')
         id_number = request.GET.get('id_number', '')
         form = PersonForm(initial={'name': name, 'code': code, 'unit': unit, 'serial': serial, 'id_number': id_number })
         messages.append('新增人员')
         return render_to_response('person_edit.html', { 'user': request.user, 'form': form, 'messages': messages })
   else:
      url = "/login/"
      return HttpResponseRedirect(url)

def person_search(request):
   if request.user.is_authenticated:
      messages = []
      person_name = request.GET.get('name', '')
      person_code = request.GET.get('code', '')
      person_unit = request.GET.get('unit', '')
      person_serial = request.GET.get('serial', '')
      person_id_number = request.GET.get('id_number', '')

      if 'create' in request.GET:
         url = "/person/new?name=%s&code=%s&unit=%s&serial=%s&id_number=%s" % (person_name, person_code, person_unit, person_serial, person_id_number)
         return HttpResponseRedirect(url)
      else:
         person_list = []

         if (person_name == ''):
            messages.append("请输入姓名.")
            return render_to_response('person_search.html', { 'user': request.user, 'name': person_name, 'code': person_code, 'unit': person_unit, 'serial': person_serial, 'id_number': person_id_number, 'messages': messages })
         else:
            person_list = Person.objects.filter(name__contains = person_name)

         if (person_code != ''):
            person_list = person_list.filter(code__contains = person_code)

         if (person_unit != ''):
            person_list = person_list.filter(unit__contains = person_unit)

         if (person_serial != ''):
            person_list = person_list.filter(serial__contains = person_serial)

         if (person_id_number != ''):
            person_list = person_list.filter(id_number__contains = person_id_number)

         messages.append("找到%s条记录." % person_list.count())
         return render_to_response('person_search.html', { 'user': request.user, 'name': person_name, 'code': person_code, 'unit': person_unit, 'serial': person_serial, 'id_number': person_id_number, 'person_list': person_list, 'messages': messages })
         

   else:
      url = "/login/"
      return HttpResponseRedirect(url)

def register(request, person_id):
   if request.user.is_authenticated:
      messages = []
      try:
         person = Person.objects.get(id = person_id)
      except Person.DoesNotExist:
         url = "/person/unknown/"
         return HttpResponseRedirect(url)

      if request.method == 'POST':
         form = RegisterForm(request.POST)

         if form.is_valid():
            data = form.cleaned_data
            #category_list = Category.objects.filter(name__contains = data.field['key_word'])
            #form.fields['category'].queryset = category_list
            try:
               register = Register(user = request.user, 
                  person = person, 
                  category = data['category'], 
                  quantity = data['quantity'], 
                  document_date = data['document_date'], 
                  create_date = datetime.datetime.now(), 
                  comment = data['comment'])
               register.save()
               messages.append('保存成功')
               log = Log(
                  user = request.user, 
                  person = register.person, 
                  category = register.category, 
                  quantity = register.quantity, 
                  document_date = data['document_date'], 
                  create_date = datetime.datetime.now(), 
                  comment = data['comment'], 
                  operation = 'create')
               log.save()
               form = RegisterForm(initial={'document_date': datetime.datetime.now() })
            except:
               messages.append("保存失败")
         else:
            messages.append('请检查输入数据')
         return render_to_response('register.html', { 'user': request.user, 'person': person, 'form': form, 'messages': messages })
      else:
         key_word = request.GET.get('key_word', '')
         if (key_word == ''):
            messages.append("请输入关键字查找材料名称")
         else:
            messages.append("查找 %s " % key_word)
         category_list = Category.objects.filter(name__contains = key_word).order_by("sequence")
         form = RegisterForm(initial={'document_date': datetime.datetime.now() })
         form.fields['category'].queryset = category_list
         return render_to_response('register.html', { 'user': request.user, 'key_word': key_word, 'person': person, 'form': form, 'messages': messages })

   else:
      url = "/login/"
      return HttpResponseRedirect(url)

def excel(request, person_id):
   if request.user.is_authenticated:
      messages = []
      try:
         person = Person.objects.get(id = person_id)
      except Person.DoesNotExist:
         url = "/person/unknown/"
         return HttpResponseRedirect(url)

      register_list = Register.objects.filter(person__id = person_id).order_by("document_date", "category__sequence")
      if register_list:
         ws = xlwt.Workbook(encoding='utf-8')
         w = ws.add_sheet(person.name)

         write_sheet(w, register_list)

         sheet_list = []
         for register in register_list:
            code = register.category.code
            code_list = code.split('-')
            code1 = code_list[0]
            if not code1 in sheet_list:
               sheet_list.append(code1)

         sheet_list.sort()

         for sheet in sheet_list:
            register_sheet = []
            for register in register_list:
               code = register.category.code
               code_list = code.split('-')
               code1 = code_list[0]

               if (code1 == sheet):
                  register_sheet.append(register)

            w = ws.add_sheet(sheet)
            write_sheet(w, register_sheet)


         now = int(time.time())
         file_name = "%s-%s.xls" % (now, person_id)
         logger.info(file_name)
         exist_file = os.path.exists(file_name)
         if exist_file:
            os.remove(file_name)
         ws.save(file_name)
         sio = io.BytesIO()
         ws.save(sio)
         sio.seek(0)
         response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
         response['Content-Disposition'] = 'attachment; filename=%s' % file_name
         response.write(sio.getvalue())  
         return response

   else:
      url = "/login/"
      return HttpResponseRedirect(url)
    
def write_sheet(sheet, register_list):
   alignment = xlwt.Alignment()
   alignment.horz = xlwt.Alignment.HORZ_CENTER
   alignment.vert = xlwt.Alignment.VERT_CENTER
   style = xlwt.XFStyle()
   style.alignment = alignment

   borders = xlwt.Borders()
   borders.left = xlwt.Borders.THIN
   borders.right = xlwt.Borders.THIN
   borders.top = xlwt.Borders.THIN
   borders.bottom = xlwt.Borders.THIN
   borders.left_colour = 0x40
   borders.right_colour = 0x40
   borders.top_colour = 0x40
   borders.bottom_colour = 0x40
   style.borders = borders

   row = 0
   row += 1
   sheet.write_merge(0, 1, 0, 0, u"类号", style)
   sheet.write_merge(0, 1, 1, 1, u"材料名称", style)
   sheet.write_merge(0, 0, 2, 4, u"材料形成时间", style)
   sheet.write_merge(0, 1, 5, 5, u"页数", style)
   sheet.write_merge(0, 1, 6, 6, u"备注", style)

   sheet.write(1, 2, u"年", style)
   sheet.write(1, 3, u"月", style)
   sheet.write(1, 4, u"日", style)
   row += 1
   for register in register_list:
      code = register.category.code
      category = register.category.name
      year = register.document_date.year
      month = register.document_date.month
      day = register.document_date.day
      quantity = register.quantity
      comment = register.comment
      sheet.write(row, 0, code, style)
      sheet.write(row, 1, category, style)
      sheet.write(row, 2, year, style)
      sheet.write(row, 3, month, style)
      sheet.write(row, 4, day, style)
      sheet.write(row, 5, quantity, style)
      sheet.write(row, 6, comment, style)
      row += 1

   sheet.col(0).width = 2500
   sheet.col(1).width = 9000
   sheet.col(2).width = 1250
   sheet.col(3).width = 1250
   sheet.col(4).width = 1250
   sheet.col(5).width = 2500
   sheet.col(6).width = 5000

   sheet.row(row).height = 600


def hasNumber(inputString):
   return any(char.isdigit() for char in inputString)
