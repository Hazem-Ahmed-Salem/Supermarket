from django.db import models


class Product(models.Model):
    Category_choices = [
    ('FR', 'Fruits'),
    ('VG', 'Vegetables'),
    ('DR', 'Dairy'),
    ('MT', 'Meat'),
    ('BK', 'Bakery'),
    ('OT', 'Other'),
    ]
    Shelf_life_choices = [
    ('p', 'Perishable'),
    ('n', 'Non-Perishable'),
    ]
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255,choices=Category_choices)
    weight = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    volume = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    shelf_life = models.CharField(max_length=255,choices=Shelf_life_choices)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_category_choices(cls):
        return [choice for choice in cls.Category_choices]
    @classmethod
    def get_shelf_life_choices(cls):
        return [choice for choice in cls.Shelf_life_choices]

    def get_stock_quantity(self):
        return Stock.objects.filter(product=self.id).aggregate(models.Sum('quantity'))['quantity__sum'] or 0

    def __str__(self):
        return self.name


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    supplier = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.product}:{self.quantity} Units".title()

