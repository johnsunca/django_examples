from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("index", views.index, name='index'),
    path("create", views.create, name='create'),
    path("read", views.read, name='read'),
    path("update", views.update, name='update'),
    path("delete", views.delete, name='delete'),
    path("create_relations", views.create_relations, name='create_relations'),
    path("read_relations", views.read_relations, name='read_relations'),
    path("update_relations", views.update_relations, name='update_relations'),
    path("exercises", views.exercises, name='exercises'),
]