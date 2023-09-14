from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from .models import Book
from mainapp.models import COST_DETAIL
# from .models import COST_DETAILS
class BookFilterForm(BSModalForm):
    type = forms.ChoiceField(choices=Book.BOOK_TYPES)

    class Meta:
        fields = ['type']


class BookModelForm(BSModalModelForm):
    # publication_date = forms.DateField(
    #     error_messages={'invalid': 'Enter a valid date in YYYY-MM-DD format.'}
    # )
    EFFDT = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),
            error_messages={'invalid': 'Enter a valid date in YYYY-MM-DD format.'}
        )
    class Meta:
        #model = Book
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
