from django import forms
from archive.models import Category
from datetime import datetime

import logging

logger = logging.getLogger('django')

class PersonForm(forms.Form):
   name = forms.CharField(max_length = 16)
   code = forms.CharField(max_length = 16)
   unit = forms.CharField(max_length = 128)
   id_number = forms.CharField(max_length = 18, min_length = 18, required=False)
   

   #def clean_name(self):
   #   name = self.cleaned_data['name']
   #   num_words = len(name.split())
   #   if num_words < 4:
   #      raise forms.ValidationError("Not enough words!")
   #   return name

class RegisterForm(forms.Form):
   key_word = forms.CharField(max_length = 32, required = False)
   category = forms.ModelChoiceField(queryset=Category.objects.all())
   quantity = forms.IntegerField()
   document_date = forms.DateField() #widget=forms.widgets.SelectDateWidget(years=range(datetime.now().year, datetime.now().year-100, -1))
   comment = forms.CharField(max_length=256, widget=forms.Textarea(attrs={'rows':3, 'cols':50}), required = False)

