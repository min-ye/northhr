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
from archive.models import Person, Register, Log, Heading, Category, Archive, PersonLog
from archive.forms import PersonForm, RegisterForm
import re

logger = logging.getLogger('django')

def layout(request):
   if request.method == 'POST':
      form = PersonForm(request.POST)

   else:
      form = PersonForm()
   return render_to_response('layout.html', { 'form': form })

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
            archive_name = register.archive_name
            document_date = register.document_date
            register.delete()
            log = Log(user = request.user, person = register.person, archive_name = register.archive_name, category = register.category, quantity = register.quantity, document_date = register.document_date, sequence = register.sequence, create_date = register.create_date, relationship = register.relationship, comment = register.comment, operation = 'delete')
            log.save()
            date = document_date.strftime("%Y-%m-%d")
            message = "%s %s 删除成功." % (archive_name, date)
            messages.append(message)
         except:
            messages.append("删除失败.")
         
      register_list = Register.objects.filter(person__id = id).order_by("document_date", "sequence")
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
            try:
               sequence = int(data['sequence'])
            except:
               sequence = 0

            logger.info(sequence)
            register = Register(user = request.user, 
               person = person, 
               archive_name = data['archive_name'],
               category = data['category'],
               quantity = data['quantity'], 
               document_date = data['document_date'], 
               create_date = datetime.datetime.now(), 
               sequence = sequence,
               relationship = data['relationship'],
               comment = data['comment'])
            register.save()
            try:
               logger.info(data['category'].id)
               logger.info(data['relationship'])
               
               messages.append('记录保存成功')
               log = Log(
                  user = request.user, 
                  person = register.person,
                  archive_name = register.archive_name,
                  category = register.category, 
                  quantity = register.quantity, 
                  document_date = data['document_date'], 
                  sequence = sequence,
                  create_date = datetime.datetime.now(), 
                  relationship = register.relationship,
                  comment = data['comment'], 
                  operation = 'create')
               log.save()
               form = RegisterForm(initial={'document_date': datetime.datetime.now() })
            except:
               messages.append("Log保存失败")
         else:
            messages.append('请检查输入数据')
         
         key_word = request.GET.get('key_word', '')
         
         category_list = Category.objects.all().order_by("sequence")
         archive_list = Archive.objects.filter(name__contains = key_word).order_by("sequence")

         form = RegisterForm(initial={'document_date': datetime.datetime.now() })
         form.fields['category'].queryset = category_list
         return render_to_response('register.html', { 'user': request.user, 'key_word': key_word, 'person': person, 'archive_list': archive_list, 'form': form, 'messages': messages })
      else:
         key_word = request.GET.get('key_word', '')
         if (key_word == ''):
            messages.append("请输入关键字查找材料名称")
         else:
            messages.append("查找 %s " % key_word)
         category_list = Category.objects.all().order_by("sequence")
         archive_list = Archive.objects.filter(name__contains = key_word).order_by("sequence")

         form = RegisterForm(initial={'document_date': datetime.datetime.now() })
         form.fields['category'].queryset = category_list
         return render_to_response('register.html', { 'user': request.user, 'key_word': key_word, 'person': person, 'archive_list': archive_list, 'form': form, 'messages': messages })
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

      register_list = Register.objects.filter(person__id = person_id).order_by("document_date", "category__code", "sequence")
      if register_list:
         ws = xlwt.Workbook(encoding='utf-8')
         w = ws.add_sheet(person.name)

         write_sheet(w, register_list)

         sheet_list = []
         #for code in Category.objects.values('code').order_by('code').distinct():
         #   code_list = code.split('-')
         #   code1 = code_list[0]
         #   if not code1 in sheet_list:
         #      sheet_list.append(code1)

         for register in register_list:
            code = register.category.code
            code_list = code.split('-')
            code1 = code_list[0]
            if not code1 in sheet_list:
               sheet_list.append(code1)

         sheet_list.sort(key = lambda x:x.zfill(5))

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
      category = register.archive_name
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
