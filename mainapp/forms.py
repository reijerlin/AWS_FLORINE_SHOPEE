from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from .models import COST_DETAIL


# class BookFilterForm(BSModalForm):
#     type = forms.ChoiceField(choices=COST_DETAIL.COST_TYPES)

#     class Meta:
#         fields = ['type']




class BookModelForm(BSModalModelForm):
  
        
    EFFDT = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),
        error_messages={'invalid': 'Enter a valid date in YYYY-MM-DD format.'}
    )
   
    # USERNAME= forms.CharField(max_length=50,
    #                        widget= forms.TextInput
    #                        (attrs={'placeholder':}))
    
    class Meta:
        model = COST_DETAIL
        exclude = ['timestamp']


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
