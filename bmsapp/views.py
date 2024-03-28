from sqlite3 import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth.models import User
from .models import Country, Author, Book, Publisher, FavoriteBook
from .forms import AuthorForm, AuthorModelForm, BookModelForm


from django.contrib.auth.decorators import (
    user_passes_test,
    permission_required,
    login_required,
)

# Create your views here.

def home(request):
    favoritebooks = FavoriteBook.objects.filter(user=request.user).count() \
        if request.user.is_authenticated else 0
    users_all = User.objects.all()  \
        if request.user.is_superuser else None
    count = {'users': User.objects.count(),
             'users_all': users_all,
             'authors': Author.objects.count(),
             'books': Book.objects.count(),
             'publishers': Publisher.objects.count(),
             'countries': Country.objects.count(), 
             'favoritebooks': favoritebooks,
             'favoritebooks_all': FavoriteBook.objects.count(),}
    return render(request, 'bmsapp/home.html', {'count': count})

# ===========================================================================

def country_list(request):
    countries = Country.objects.all().order_by('abbreviation')
    return render(request, 'bmsapp/country_list.html', {'country_list': countries})

def country_detail(request, country_id):
    country = get_object_or_404(Country, pk=country_id)
    return render(request, 'bmsapp/country_detail.html', {'country': country})

@permission_required('bmsapp.delete_country')
def country_delete(request, country_id):
    country = get_object_or_404(Country, pk=country_id)
    if request.method == 'POST':
        country.delete()
        return redirect('country_list')
    
    return render(request, 'bmsapp/country_delete.html', {'country': country})

# Way1: using raw form in template and view

@permission_required('bmsapp.add_country')
@permission_required('bmsapp.change_country')
def country_update(request, country_id=None):
    country = None
    if country_id:
        country = get_object_or_404(Country, pk=country_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        abbreviation = request.POST.get('abbreviation')
        if country:
            country.name = name
            country.abbreviation = abbreviation
            country.save()
        else:
            Country.objects.create(name=name, abbreviation=abbreviation)
        return redirect('country_list')
    
    return render(request, 'bmsapp/country_form.html', {'country': country})

# ===========================================================================

def author_list(request):
    authors = Author.objects.all().order_by('birth_date')
    return render(request, 'bmsapp/author_list.html', {'author_list': authors})

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'bmsapp/author_detail.html', {'author': author})

@permission_required('bmsapp.delete_author')
def author_delete(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    if request.method == 'POST':        
        author.delete()
        return redirect('author_list')
    else:
        return render(request, 'bmsapp/author_delete.html', {'author': author})

# ===========================================================================
# Way2: Ver1: use Form not ModelForm, separate create and update (urls.py need to change)    

@permission_required('bmsapp.add_author')    
def author_create(request):
    author = None
    error_message = None

    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():            
            author = Author(
                title=form.cleaned_data['title'],
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                birth_date=form.cleaned_data['birth_date'],
                country=form.cleaned_data['country'],
                status=form.cleaned_data['status'],
                is_active = form.cleaned_data['is_active']
            )
            try:
                author.save()
                return redirect('author_list')
            except Exception as e:
                error_message = 'Error: ' + str(e)
                form.add_error('email', 'This email address is already in use.')
    else:
        form = AuthorForm()
    return render(request, 'bmsapp/author_form.html', 
                  {'form': form, 'error_message': error_message})

@permission_required('bmsapp.change_author')
def author_update(request, author_id):
    error_message = None
    author = get_object_or_404(Author, pk=author_id)

    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():            
            author.title = form.cleaned_data['title']
            author.name = form.cleaned_data['name']
            author.email = form.cleaned_data['email']
            author.birth_date = form.cleaned_data['birth_date']
            author.country = form.cleaned_data['country'] 
            author.status = form.cleaned_data['status']
            author.is_active = form.cleaned_data['is_active']
            try:
                author.save()
                return redirect('author_list')
            except Exception as e:
                error_message = 'Error: ' + str(e)
                form.add_error('email', 'This email address is already in use.')
    else:
        form = AuthorForm(initial={
            'title': author.title,
            'name': author.name,
            'email': author.email,
            'birth_date': author.birth_date,
            'country': author.country,
            'status': author.status,
            'is_active': author.is_active,
        })           
    return render(request, 'bmsapp/author_form.html', 
                  {'form': form, 'author': author, 'error_message': error_message})


# ===========================================================================

# Way3: Ver2: use ModelForm, combine create and update (urls.py need to change)

@permission_required('bmsapp.add_author')
@permission_required('bmsapp.change_author')
def author_edit_modelform(request, author_id=None):
    # If pk is provided, it's an update operation, otherwise it's a create operation
    # If GET method, it's for an empty form for create or initial form for update
    # If POST method, it can be for creating a new author or updating an existing author
    author = get_object_or_404(Author, pk=author_id) if author_id else None

    if request.method == 'POST':
        form = AuthorModelForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author_list')  
    else:
        form = AuthorModelForm(instance=author)

    context = {'form': form, 'author': author}
    return render(request, 'bmsapp/author_form.html', context)
    

# ===========================================================================

def book_list(request):
    books = Book.objects.all().order_by('published_year')
    return render(request, 'bmsapp/book_list.html', {'book_list': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'bmsapp/book_detail.html', {'book': book})

@permission_required('bmsapp.add_book')
@permission_required('bmsapp.change_book')
def book_edit(request, book_id=None):
    book = get_object_or_404(Book, pk=book_id) if book_id else None
    
    if request.method == 'POST':
        form = BookModelForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookModelForm(instance=book)

    return render(request, 'bmsapp/book_form.html', {'form': form, 'book': book})

@permission_required('bmsapp.delete_book')
def book_delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bmsapp/book_delete.html', {'book': book})

# ===========================================================================
# Way4: use class-based generic views

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.urls import reverse_lazy

class PublisherListView(generic.ListView):
    model = Publisher

from django.conf import settings
# class PublisherDetailView(LoginRequiredMixin, generic.DetailView):
class PublisherDetailView(generic.DetailView):
    model = Publisher
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MEDIA_URL"] = settings.MEDIA_URL
        return context

class PublisherCreate(PermissionRequiredMixin, CreateView):
# class PublisherCreate(CreateView):
    model = Publisher
    fields = "__all__"
    success_url = '/bmsapp/publishers' # reverse_lazy('publishers') # specify the url directly
    permission_required = 'bmsapp.add_publisher'

class PublisherUpdate(PermissionRequiredMixin, UpdateView):
# class PublisherUpdate(UpdateView):
    model = Publisher
    fields = "__all__"
    success_url = reverse_lazy('publisher_list')
    permission_required = 'bmsapp.change_publisher'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MEDIA_URL"] = settings.MEDIA_URL
        return context

class PublisherDelete(PermissionRequiredMixin, DeleteView):
# class PublisherDelete(DeleteView):
    model = Publisher
    template_name = 'bmsapp/publisher_delete.html'
    success_url = reverse_lazy('publisher_list')
    permission_required = 'bmsapp.delete_publisher'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MEDIA_URL"] = settings.MEDIA_URL
        return context

# ===========================================================================

@login_required
def search(request):
    key = request.GET.get('key', '')
    type = request.GET.get('type', 'author')
    if len(key) < 3 or type not in ['author', 'book', 'publisher']: 
        return redirect('home')
    
    result_set = None
    if type == 'author': 
        result_set = Author.objects.filter(name__icontains=key) 
    elif type == 'book':
        result_set = Book.objects.filter(title__icontains=key) 
    elif type == 'publisher':
        result_set = Publisher.objects.filter(name__icontains=key)
    else: 
        return redirect('home')
    
    return render(request, f'bmsapp/{type}_list.html', 
                  {f'{type}_list': result_set, 'search_key': key})


# ===========================================================================

# not needed since login redirect set in settings
# def profile(request):
#     return redirect('home')


from .forms import CreateUserForm

def signup(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    return render(request, 'signup.html', {'form':form})


# ===========================================================================

class FavoriteBookListView(LoginRequiredMixin, generic.ListView):
    model = FavoriteBook
    fields = '__all__'
    
    def get_queryset(self): 
        user = self.request.user
        if user.is_superuser:
            return FavoriteBook.objects.all()
        return FavoriteBook.objects.filter(user=user)

@login_required    
def favoritebook_create(request, book_id):
    user = request.user
    book = get_object_or_404(Book, pk=book_id)
    try:
        favoritebook = FavoriteBook.objects.get(user=user, book=book)
        favoritebook.save()
    except:
        FavoriteBook.objects.create(user=user, book=book)
    return redirect('favoritebook_list')
        
@login_required
def favoritebook_delete(request, favoritebook_id):
    favoritebook = get_object_or_404(FavoriteBook, pk=favoritebook_id)
    if favoritebook and (favoritebook.user == request.user or request.user.is_superuser):
        favoritebook.delete()
    return redirect('favoritebook_list')

# ===========================================================================


from django.utils import timezone
from faker import Faker # pip install Faker
import random

@user_passes_test(lambda u: u.is_superuser)
def generate_fake_data_view(request):
    print('Populates the database with hardcoded data')

    # Clear existing data
    User.objects.filter(is_superuser=False).delete()
    Country.objects.all().delete()
    Author.objects.all().delete()
    Book.objects.all().delete()
    Publisher.objects.all().delete()
    FavoriteBook.objects.all().delete()

    fake = Faker()

    # Add countries
    countries = ['USA', 'UK', 'Canada', 'Australia', 'Germany', 'France']
    country_code = ['US', 'UK', 'CA', 'AU', 'DE', 'FR']
    for i in range(len(countries)):
        Country.objects.create(name=countries[i], abbreviation=country_code[i])

    # Add authors
    for _ in range(20):
        country = random.choice(Country.objects.all())
        Author.objects.create(
            title=random.choice(['MR', 'MRS', 'MS', 'DR', 'PF']),
            name=fake.name(),
            email=fake.email(),
            birth_date=fake.date_of_birth(),
            country=country,
            status=random.choice(['emerging', 'experienced', 'retired']),
            is_active=random.choice([True, False])
        )

    # Add publishers
    for _ in range(10):
        country = random.choice(Country.objects.all())
        Publisher.objects.create(
            name=fake.company(),
            address=fake.street_address(),
            city=fake.city(),
            state_province=fake.state(),
            country=country,
            website=fake.url()
        )

    # Add books
    for _ in range(50):
        publisher = random.choice(Publisher.objects.all())
        book = Book.objects.create(
            title=fake.text(max_nb_chars=50),
            published_year=random.randint(2000, timezone.now().year),
            rating=random.randint(0, 100) / 10,
            publisher=publisher
        )
        authors = random.sample(list(Author.objects.all()), random.randint(1, 3))
        book.authors.add(*authors)

    # Add users
    for _ in range(5):
        username = fake.user_name()
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email)

    # Add favorite books for users
    users = User.objects.all()
    for user in users:
        favorite_books = random.sample(list(Book.objects.all()), random.randint(10, 20))
        for book in favorite_books:
            FavoriteBook.objects.create(user=user, book=book, added_at=fake.date_time())

    print('Data population completed successfully.')

    return redirect('home')