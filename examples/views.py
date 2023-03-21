from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic

from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)

from .forms import (
    BookModelForm,
    CustomUserCreationForm,
    CustomAuthenticationForm,
    BookFilterForm
)
from .models import Book
from mainapp.models import COST_DETAIL


class BooksIndex(generic.ListView):
    model = COST_DETAIL
    #model = Book
    context_object_name = 'books'
    template_name = 'cost_detail.html'
    # dispatch is called when the class instance loads
    def dispatch(self, request, *args, **kwargs):
        self.YYYYMM = kwargs.get('YYYYMM','2023-03')

    # other code

    # needed to have an HttpResponse
        return super(BooksIndex, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # qs = super().get_queryset()

        user = self.request.user
        return COST_DETAIL.objects.filter(USERNAME=user,YYYYMM=self.YYYYMM)
        #return COST_DETAIL.objects.filter(USERNAME=user)
        # if 'type' in self.request.GET:
        #     qs = qs.filter(book_type=int(self.request.GET['type']))
        # return qs
    def get_context_data(self, **kwargs):
        context = super(BooksIndex, self).get_context_data(**kwargs)
        context['username'] = self.request.user
        context['YYYYMM'] = self.YYYYMM
        return context

class BookFilterView(BSModalFormView):
    template_name = 'examples/filter_book.html'
    form_class = BookFilterForm

    def form_valid(self, form):
        self.filter = '?type=' + form.cleaned_data['type']
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('booksindex') + self.filter

   
class BookCreateView(BSModalCreateView):
    template_name = 'examples/create_book.html'
    form_class = BookModelForm
    success_message = 'Success: Cost was added.'

    def dispatch(self, request, *args, **kwargs):
        self.YYYYMM = kwargs.get('YYYYMM','2023-03')

    # other code

    # needed to have an HttpResponse
        return super(BookCreateView, self).dispatch(request, *args, **kwargs)


    def get_success_url(self):
        return  reverse_lazy('booksindex', kwargs={'YYYYMM': self.YYYYMM})

   


class BookUpdateView(BSModalUpdateView):
    model = COST_DETAIL
    template_name = 'examples/update_book.html'
    form_class = BookModelForm
    success_message = 'Success: Cost was updated.'
    # success_url = reverse_lazy('booksindex')
    def dispatch(self, request, *args, **kwargs):
        self.YYYYMM = kwargs.get('YYYYMM','2023-03')

    # other code

    # needed to have an HttpResponse
        return super(BookUpdateView, self).dispatch(request, *args, **kwargs)
    def get_success_url(self):
        return  reverse_lazy('booksindex', kwargs={'YYYYMM': self.YYYYMM})

class BookReadView(BSModalReadView):
    model = Book
    template_name = 'examples/read_book.html'


class BookDeleteView(BSModalDeleteView):
    model = COST_DETAIL
    template_name = 'examples/delete_book.html'
    success_message = 'Success: Cost was deleted.'
    # success_url = reverse_lazy('booksindex')
    def dispatch(self, request, *args, **kwargs):
        self.YYYYMM = kwargs.get('YYYYMM','2023-06')
        
    # other code

    # needed to have an HttpResponse
        return super(BookDeleteView, self).dispatch(request, *args, **kwargs)
    def get_success_url(self):
        return  reverse_lazy('booksindex', kwargs={'YYYYMM': self.YYYYMM})


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'examples/signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('booksindex')


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'examples/login.html'
    success_message = 'Success: You were successfully logged in.'
    success_url = reverse_lazy('booksindex')


def books(request,YYYYMM):

    data = dict()
    username = request.user.username
    
    if request.method == 'GET':
        #books = COST_DETAIL.objects.all()
       
        #books = COST_DETAIL.objects.filter(USERNAME=username,YYYYMM=YYYYMM)
        books = COST_DETAIL.objects.filter(USERNAME=username,YYYYMM=YYYYMM)
        #books = Book.objects.all()
        data['table'] = render_to_string(
            '_books_table.html',
            {'books': books},
            request=request
        )
        return JsonResponse(data)
