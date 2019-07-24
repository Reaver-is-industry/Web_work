# -*- coding:utf-8 -*-

from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Путь')
