from django import forms
from archive.models import Category
from datetime import datetime

import logging

logger = logging.getLogger('django')

class PersonForm(forms.Form):
   name = forms.CharField(max_length = 16)
   code = forms.CharField(max_length = 16)
   unit = forms.CharField(max_length = 128)
   serial = forms.CharField(max_length = 16, required=False)
   id_number = forms.CharField(max_length = 18, min_length = 18, required=False)
   

   #def clean_name(self):
   #   name = self.cleaned_data['name']
   #   num_words = len(name.split())
   #   if num_words < 4:
   #      raise forms.ValidationError("Not enough words!")
   #   return name

class RegisterForm(forms.Form):
   key_word = forms.CharField(max_length=32, required = False)
   #category = forms.ModelChoiceField(queryset=Category.objects.all())
   archive_name = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'style': 'width: 55em; '}), required = True)
   category = forms.ModelChoiceField(queryset=Category.objects.all())
   quantity = forms.IntegerField()
   document_date = forms.DateField(widget=forms.DateInput(format = '%Y%m%d'), 
                                 input_formats=('%Y%m%d',)) #widget=forms.widgets.SelectDateWidget(years=range(datetime.now().year, datetime.now().year-100, -1))
   RELATIONSHIP_OPTION = (('1', '本人'),('2', '夫妻'),('3', '父母'))
   relationship = forms.ChoiceField(choices=RELATIONSHIP_OPTION, initial='1', widget=forms.RadioSelect())
   sequence = forms.IntegerField(required=False)
   comment = forms.CharField(max_length=256, widget=forms.Textarea(attrs={'rows':3, 'cols':50}), required = False)

