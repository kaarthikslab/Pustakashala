from django.db import models
from django.db.models import Sum, F

class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, blank=True, null=True)
    is_out_of_stock = models.BooleanField(default=False)

    def total_purchased(self):
        return self.batches.aggregate(total=Sum('quantity'))['total'] or 0

    def total_distributed(self):
        return sum(batch.distributions.aggregate(total=Sum('quantity'))['total'] or 0 for batch in self.batches.all())

    def current_stock(self):
        return self.total_purchased() - self.total_distributed()

    def total_cost_distributed(self):
        return sum(
            dist.quantity * dist.batch.unit_cost
            for batch in self.batches.all()
            for dist in batch.distributions.all()
        )

    def __str__(self):
        return self.title

class Batch(models.Model):
    book = models.ForeignKey(Book, related_name='batches', on_delete=models.CASCADE)
    purchase_date = models.DateField()
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_value(self):
        return self.quantity * self.unit_cost

    def __str__(self):
        return f"{self.book.title} - {self.purchase_date}"

class Distribution(models.Model):
    batch = models.ForeignKey(Batch, related_name='distributions', on_delete=models.CASCADE)
    distribution_date = models.DateField()
    quantity = models.IntegerField()
    recipient_category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.batch.book.title} - {self.distribution_date}"
