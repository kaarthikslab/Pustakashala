from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Book, Batch, Distribution
from .forms import BookForm, BatchForm, DistributionForm
import plotly.express as px
from django.db.models import Sum

@login_required
def dashboard(request):
    books = Book.objects.all()
    total_purchased = sum(book.total_purchased() for book in books)
    total_distributed = sum(book.total_distributed() for book in books)
    total_stock = sum(book.current_stock() for book in books)
    total_cost = sum(book.total_cost_distributed() for book in books)

    distributions = Distribution.objects.all().values('distribution_date').annotate(total=Sum('quantity')).order_by('distribution_date')
    fig = px.line(distributions, x='distribution_date', y='total', title='Monthly Distribution Trends')
    chart = fig.to_html(full_html=False)

    return render(request, 'books/dashboard.html', {
        'total_purchased': total_purchased,
        'total_distributed': total_distributed,
        'total_stock': total_stock,
        'total_cost': total_cost,
        'chart': chart,
    })

@login_required
def books_list(request):
    book_id = request.GET.get('book')
    if book_id:
        books = Book.objects.filter(id=book_id)
    else:
        books = Book.objects.all()
    all_books = Book.objects.all()
    return render(request, 'books/books_list.html', {'books': books, 'all_books': all_books})

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books_list')
    else:
        form = BookForm()
    return render(request, 'books/modal_form.html', {'form': form, 'title': 'Add Book'})

@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/modal_form.html', {'form': form, 'title': 'Edit Book'})

@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('books_list')

@login_required
def mark_out_of_stock(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.current_stock() == 0:
        book.is_out_of_stock = True
        book.save()
    return redirect('books_list')

# Add similar views for batches/distributions if needed
