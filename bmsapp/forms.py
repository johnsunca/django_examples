
from django import forms

from bmsapp.models import STATUS_CHOICES, TITLE_CHOICES, Country, Author, Book

# Way 1: Raw Form for Country

# Way 2: Form for Author

class AuthorForm(forms.Form):    
    title = forms.ChoiceField(required=False, choices=TITLE_CHOICES)
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    country = forms.ModelChoiceField(required=False, queryset=Country.objects.all())
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.RadioSelect, initial='experienced')
    is_active = forms.BooleanField(required=False)

# Way 3: ModelForm for Author (and Book?)
        
class AuthorModelForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        labels = {'name': 'Author Name', } # Customize label for 'name' field
        widgets = {'status': forms.Select, # Customize widget for 'status' field
                   'birth_date': forms.DateInput(attrs={"type": "date"})}  
        
class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "authors", "publisher", "published_year", "rating"]  # Adjusted field name from "name" to "title"
        help_texts = {'rating': "Enter your rating for this book"}  # Customize help text for 'rating' field
        widgets = {'rating': forms.NumberInput(attrs={'step': '0.1'})}  
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all(), required=False)

# ===========================================================================
    
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 
                  'username', 'email', 'password1', 'password2']
