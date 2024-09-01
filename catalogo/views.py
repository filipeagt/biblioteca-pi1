from django.db.models.query import QuerySet
from django.shortcuts import render

# Create your views here.
from django.db.models import Q # Para barra de pesquisa

from .models import Book, Autor, BookInstance, Gênero, Language

def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available copies of books
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()
    num_autors = Autor.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_autors': num_autors,
                 'num_visits': num_visits},
    )

from django.views import generic



class BookListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Book
    paginate_by = 10

    def get_queryset(self): #Para barra de pesquisa
        pesquisa = self.request.GET.get('pesquisa')
        if pesquisa == None:
            pesquisa = ''
        lista_objetos = Book.objects.filter(
            Q(título__icontains=pesquisa) #| Q(autor__icontains=pesquisa) | Q(gênero__icontains=pesquisa)
        )
        return lista_objetos

class BookDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Book

class AutorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Autor
    paginate_by = 10

class AutorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Autor


class GêneroDetailView(generic.DetailView):
    """Generic class-based detail view for a gênero."""
    model = Gênero

class GêneroListView(generic.ListView):
    """Generic class-based list view for a list of gêneros."""
    model = Gênero
    paginate_by = 10

class LanguageDetailView(generic.DetailView):
    """Generic class-based detail view for a gênero."""
    model = Language

class LanguageListView(generic.ListView):
    """Generic class-based list view for a list of gêneros."""
    model = Language
    paginate_by = 10

class BookInstanceListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = BookInstance
    paginate_by = 10

class BookInstanceDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = BookInstance

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalogo/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )

# Added as part of challenge!
from django.contrib.auth.mixins import PermissionRequiredMixin


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'catalogo.can_mark_returned'
    template_name = 'catalogo/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required, permission_required
from catalogo.forms import RenewBookForm


@login_required
@permission_required('catalogo.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalogo/book_renew_librarian.html', context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Autor


class AutorCreate(PermissionRequiredMixin, CreateView):
    model = Autor
    fields = ['nome', 'sobrenome']
    #initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalogo.add_autor'

class AutorUpdate(PermissionRequiredMixin, UpdateView):
    model = Autor
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    permission_required = 'catalogo.change_autor'

class AutorDelete(PermissionRequiredMixin, DeleteView):
    model = Autor
    success_url = reverse_lazy('autores')
    permission_required = 'catalogo.delete_autor'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("autor-delete", kwargs={"pk": self.object.pk})
            )

# Classes created for the forms challenge


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    #fields = ['title', 'author', 'summary', 'isbn', 'gênero', 'language']
    fields = ['título', 'autor', 'resumo', 'gênero', 'idade', 'capa']
    permission_required = 'catalogo.add_book'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    #fields = ['title', 'author', 'summary', 'isbn', 'gênero', 'language']
    fields = ['título', 'autor', 'resumo', 'gênero', 'idade', 'capa']
    permission_required = 'catalogo.change_book'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalogo.delete_book'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("book-delete", kwargs={"pk": self.object.pk})
            )


class GêneroCreate(PermissionRequiredMixin, CreateView):
    model = Gênero
    fields = ['name', ]
    permission_required = 'catalogo.add_gênero'


class GêneroUpdate(PermissionRequiredMixin, UpdateView):
    model = Gênero
    fields = ['name', ]
    permission_required = 'catalogo.change_gênero'


class GêneroDelete(PermissionRequiredMixin, DeleteView):
    model = Gênero
    success_url = reverse_lazy('gêneros')
    permission_required = 'catalogo.delete_gênero'


class LanguageCreate(PermissionRequiredMixin, CreateView):
    model = Language
    fields = ['name', ]
    permission_required = 'catalogo.add_language'


class LanguageUpdate(PermissionRequiredMixin, UpdateView):
    model = Language
    fields = ['name', ]
    permission_required = 'catalogo.change_language'


class LanguageDelete(PermissionRequiredMixin, DeleteView):
    model = Language
    success_url = reverse_lazy('languages')
    permission_required = 'catalogo.delete_language'


class BookInstanceCreate(PermissionRequiredMixin, CreateView):
    model = BookInstance
    fields = ['book', 'due_back', 'borrower', 'status']
    permission_required = 'catalogo.add_bookinstance'


class BookInstanceUpdate(PermissionRequiredMixin, UpdateView):
    model = BookInstance
    # fields = "__all__"
    fields = ['due_back', 'borrower', 'status']
    permission_required = 'catalogo.change_bookinstance'


class BookInstanceDelete(PermissionRequiredMixin, DeleteView):
    model = BookInstance
    success_url = reverse_lazy('bookinstances')
    permission_required = 'catalogo.delete_bookinstance'
