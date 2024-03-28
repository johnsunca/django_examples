from django.db import models

# Create your models here.

class Country(models.Model):
    abbreviation = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.abbreviation} - {self.name}"


TITLE_CHOICES = (
    ('', 'No title'),
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
    ('DR', 'Dr.'),
    ('PF', 'Prof.')
)

STATUS_CHOICES = (
    ('emerging', 'Emerging'),
    ('experienced', 'Experienced'),
    ('retired', 'Retired')
)

class Author(models.Model):
    title = models.CharField(max_length=5, choices=TITLE_CHOICES, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True, unique=True)
    birth_date = models.DateField(blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='experienced')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} {self.name}'

    
class Book(models.Model):
    title = models.CharField(max_length=100, unique=True)
    authors = models.ManyToManyField(Author, blank=True)
    publisher = models.ForeignKey("Publisher", blank=True, null=True, on_delete=models.CASCADE)
    published_year = models.IntegerField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title

class Publisher(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True, null=True)
    state_province = models.CharField(max_length=50, blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.SET_NULL)
    website = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name
    

from django.contrib.auth.models import User

class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'book')  # Ensure a user cannot have the same book as a favorite multiple times

    def __str__(self):
        return f'{self.user}: {self.book} ({self.added_at})'