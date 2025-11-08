from django import forms
from .models import Book, Batch, Distribution

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'isbn']

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['purchase_date', 'quantity', 'unit_cost']

class DistributionForm(forms.ModelForm):
    class Meta:
        model = Distribution
        fields = ['distribution_date', 'quantity', 'recipient_category']
