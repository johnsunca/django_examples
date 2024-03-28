from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("countries", views.country_list, name='country_list'),
    path("country/<int:country_id>", views.country_detail, name='country_detail'),
    path("country/create/", views.country_update, name='country_create'),
    path("country/<int:country_id>/update/", views.country_update, name='country_update'),
    path("country/<int:country_id>/delete/", views.country_delete, name='country_delete'),

    path("authors", views.author_list, name='author_list'),
    path("author/<int:author_id>", views.author_detail, name='author_detail'),
    # path("author/create/", views.author_create, name='author_create'),
    # path("author/<int:author_id>/update/", views.author_update, name='author_update'),
    path("author/create/", views.author_edit_modelform, name='author_create'),
    path("author/<int:author_id>/update/", views.author_edit_modelform, name='author_update'),
    path("author/<int:author_id>/delete/", views.author_delete, name='author_delete'),

    path("books", views.book_list, name='book_list'),
    path("book/<int:book_id>", views.book_detail, name='book_detail'),
    path("book/create/", views.book_edit, name='book_create'),
    path("book/<int:book_id>/update/", views.book_edit, name='book_update'),
    path("book/<int:book_id>/delete/", views.book_delete, name='book_delete'),
    
    path("favoritebooks/", views.FavoriteBookListView.as_view(), name='favoritebook_list'),
    path("favoritebook/<int:book_id>/create/", views.favoritebook_create, name='favoritebook_create'),
    path("favoritebook/<int:favoritebook_id>/delete/", views.favoritebook_delete, name='favoritebook_delete'),

    path("publishers", views.PublisherListView.as_view(), name='publisher_list'),
    path("publisher/<int:pk>", views.PublisherDetailView.as_view(), name='publisher_detail'),
    path("publisher/create/", views.PublisherCreate.as_view(), name='publisher_create'),
    path("publisher/<int:pk>/update/", views.PublisherUpdate.as_view(), name='publisher_update'),
    path("publisher/<int:pk>/delete/", views.PublisherDelete.as_view(), name='publisher_delete'),   

    path("search/", views.search, name='search'),    

    path('generate-fake-data/', views.generate_fake_data_view, name='generate_fake_data'),
]

