from django.forms import ModelForm
from mainapp.models import Data

from django import forms


class DataForm(ModelForm):
    class Meta:
        model = Data
        fields = ['category', 'quantity']
       