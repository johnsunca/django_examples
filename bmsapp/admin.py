from django.contrib import admin

# Register your models here.

from .models import Country, Author, Book, Publisher, FavoriteBook

# simple customization
admin.site.site_title = 'Site Admin'
admin.site.site_header = 'Site Admin'
admin.site.index_title = 'App Index'

# customize admin forms: 
# - fields/fieldsets, date_hierarchy
class AuthorAdmin(admin.ModelAdmin):
    # fields = ['title', 'name', 'status', 'is_active', 'email', 'country', 'birth_date']
    fieldsets = (('Major Info', {'fields': ('title', 'name', 'status', 'is_active')}), 
                  ('Other Info', {'fields': ('email', 'country', 'birth_date')}))
    date_hierarchy = 'birth_date'

# - inlines
class BookInline(admin.TabularInline):
    model = Book 
class PublisherAdmin(admin.ModelAdmin):    
    inlines = [BookInline, ]

# - list_display, list_filter, search_fields
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_year', 'rating']
    list_filter = ['publisher', 'authors']
    search_fields = ['publisher__name', 'authors__name', 'title']

# register models and model admins
admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register([Country, FavoriteBook])
