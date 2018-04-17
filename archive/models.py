from django.conf import settings
from django.db import models
import datetime

class Person(models.Model):
   name = models.CharField(max_length = 16, verbose_name='姓名')
   code = models.CharField(max_length = 16, verbose_name='编号')
   unit = models.CharField(max_length = 128, verbose_name='工作单位')
   serial = models.CharField(max_length = 16, null=True, blank=True, default='', verbose_name='序号')
   id_number = models.CharField(max_length = 18, null=True, blank=True, default='', verbose_name='身份证号') #unique=True)

   def __str__(self):
      return '%s,%s' % (self.name, self.code)

   class Meta:
      verbose_name = '人员管理'
      verbose_name_plural = '人员管理'
      ordering = ["unit", "name"]


class Category(models.Model):
   name = models.CharField(max_length = 256, verbose_name='材料名称')
   title = models.CharField(max_length = 256, verbose_name='十大类')
   code = models.CharField(max_length = 16, verbose_name='类别号')
   comment = models.CharField(max_length = 512, null=True, blank=True, verbose_name='备注')
   description = models.CharField(max_length = 512, null=True, blank=True, verbose_name='说明')
   sequence = models.IntegerField(default=0, verbose_name='序号')

   def __str__(self):
      return '%s,%s(%s)' % (self.name, self.title, self.code)

   class Meta:
      verbose_name = '材料名称'
      verbose_name_plural = '材料名称'
      ordering = ["sequence"]


class Register(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
   person = models.ForeignKey(Person, on_delete=models.PROTECT)
   category = models.ForeignKey(Category, on_delete=models.PROTECT)
   category_code = models.CharField(max_length = 5, null=True, blank=True)
   quantity = models.IntegerField()
   document_date= models.DateField()
   create_date = models.DateTimeField()
   sequence = models.IntegerField(default=0)
   comment = models.CharField(max_length = 256, null=True, blank=True)

   def __str__(self):
      return '%s,%s,%s,%s,%s,%s' % (self.user.id, self.person, self.category, self.quantity, self.document_date, self.create_date)

   class Meta:
      ordering = ["person", "document_date", "category_code", "sequence"]

class PersonLog(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
   person = models.ForeignKey(Person, on_delete=models.PROTECT)
   name = models.CharField(max_length=16)
   code = models.CharField(max_length=16)
   unit = models.CharField(max_length=128)
   serial = models.CharField(max_length = 16, null=True, blank=True, default='')
   id_number = models.CharField(max_length = 18, null=True, blank=True, default='')
   operation_date = models.DateField('', auto_now = True)
   operation_time = models.TimeField('', auto_now = True)
   operation = models.CharField(max_length = 16)

   def __str__(self):
      return '%s, %s, %s, %s, %s' % (self.name, self.code, self.unit, self.serial, self.id_number, self.operation)

   class Meta:
      ordering = ["name", "operation_date", "operation_time"]


class Log(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,)
   person = models.ForeignKey(Person, on_delete=models.PROTECT,)
   category = models.ForeignKey(Category, on_delete=models.PROTECT,)
   quantity = models.IntegerField()
   document_date= models.DateField()
   sequence = models.IntegerField()
   create_date = models.DateTimeField()
   comment = models.CharField(max_length = 256, null=True, blank=True)
   operation_date = models.DateField('', auto_now = True)
   operation_time = models.TimeField('', auto_now = True)
   operation = models.CharField(max_length = 16)

   def __str__(self):
      return '%s,%s, %s, %s, %s, %s, %s' % (self.user.id, self.person.id, self.category.id, self.quantity, self.operation_date, self.operation_time, self.operation)

   class Meta:
      ordering = ["person", "operation_date", "operation_time"]
