# 5/4
from django.db import models
from django.contrib.auth.models import User

class MainMenu(models.Model):
    item = models.CharField(max_length=100)
    link = models.CharField(max_length=100)

    def __str__(self):
        return self.item

# Book model
class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    picture = models.ImageField(upload_to='book_images/', null=True, blank=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Comment model (for book comments)
class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.book.name}"

# Favorite model (for favoriting books)
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} favorites {self.book.name}"

# CartItem model (for shopping cart)
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'book')

    def total_price(self):
        return self.book.price * self.quantity

    def __str__(self):
        return f"{self.user.username} cart item {self.book.name} x {self.quantity}"
