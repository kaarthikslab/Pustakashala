from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('books/', views.books_list, name='books_list'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    path('books/<int:pk>/out-of-stock/', views.mark_out_of_stock, name='mark_out_of_stock'),
    # Add paths for batches/distributions
]
