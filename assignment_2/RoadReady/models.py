from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime



class User(AbstractUser):
    # This model extends Django's built-in AbstractUser model.
    # It adds a boolean field 'is_student' to indicate if the user is a student.
    # It also adds a 'profile_image' field to store the user's profile image.
    is_student = models.BooleanField(default=False)
    profile_image = models.FileField(default="Profile.png")

class Instructor(models.Model):
    # It includes fields for the instructor's first name, last name, bio, and profile image.
    id = models.AutoField(primary_key=True)
    first_name = models.TextField(max_length=15)
    last_name = models.TextField(max_length=15)
    bio = models.TextField(max_length=200, default="I am a driving instructor")
    profile_image = models.FileField(default="Profile.png")

    def __str__(self):
        # This method returns a string representation of an instructor.
        return self.first_name + " " + self.last_name

class Lesson(models.Model):
    # It includes fields for the lesson type and duration.
    id = models.AutoField(primary_key=True)
    lesson_type = models.CharField(max_length=10, default=True)
    duration = models.IntegerField()

    def __str__(self):
        # This method returns a string representation of a lesson.
        return self.lesson_type
    
class Booking(models.Model):
    # It includes fields for the booking date, start time, end time, user, lesson, and instructor.
    id = models.AutoField(primary_key=True)
    date = models.DateField(null=True, blank=False)
    start_time = models.TimeField(null=True, blank=False)
    end_time = models.TimeField(null=True, blank=False)
    # ForeignKey creates a many-to-one relationship. Many bookings can be made by one user.
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,default=True)
    # ForeignKey creates a many-to-one relationship. Many bookings can be for one lesson.
    lessons = models.ForeignKey(Lesson, on_delete=models.CASCADE,default=True)
    # ForeignKey creates a many-to-one relationship. Many bookings can be with one instructor.
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE,default=True)
    
class Feedback(models.Model):
    # This model represents feedback from a customer.
    # It includes fields for the customer's name, email, and feedback details.
    customer_name = models.CharField(max_length=120)
    email = models.EmailField()
    details = models.TextField()

    def __str__(self):
        # This method returns a string representation of feedback.
        return self.customer_name

class Product(models.Model):
    # This model represents a courses from the pricing page
    # It includes fields for the product's title, price, description, and associated instructors.
    title = models.CharField(max_length=120)
    price = models.IntegerField()
    description = models.TextField(max_length=120)
    # ManyToManyField creates a many-to-many relationship. Many products can be taught by many instructors.
    instructors = models.ManyToManyField(Instructor)
    
    def __str__(self):
        # This method returns a string representation of a product.
        return self.title

class Transaction(models.Model):
    # It includes fields for the payment method, card name, card number, card expiry date, and card CVV.
    PAYMENT_METHODS = [
        ('credit', 'Credit Card'),
        ('debit', 'Debit Card'),
        ('paypal', 'PayPal'),
    ]
    id = models.AutoField(primary_key=True)
    # ForeignKey creates a many-to-one relationship. Many transactions can be for one product.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=6, choices=PAYMENT_METHODS, default='credit')
    card_name = models.CharField(max_length=200)
    card_number = models.CharField(max_length=16)
    card_expiry = models.DateField(null=True, blank=False)
    card_cvv = models.CharField(max_length=3)

    def __str__(self):
        # This method returns a string representation of a transaction.
        return f'Transaction for {self.product.title}'

class Basket(models.Model):
    # This model represents a user's basket.
    # It includes a foreign key field for the associated user.
    # ForeignKey creates a many-to-one relationship. Many baskets can be owned by one user.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class BasketItem(models.Model):
    # It includes fields for the associated product, basket, and quantity.
    # ForeignKey creates a many-to-one relationship. Many basket items can be for one product.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # ForeignKey creates a many-to-one relationship. Many basket items can be in one basket.
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class BillingAddress(models.Model):
    # It includes fields for the associated user, first name, last name, username, email, and address.
    # OneToOneField creates a one-to-one relationship. One user can have one billing address.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True)

class Order(models.Model):
    # It includes fields for the associated user, transactions, and date.
    # ForeignKey creates a many-to-one relationship. Many orders can be made by one user.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # ManyToManyField creates a many-to-many relationship. Many orders can have many transactions.
    transactions = models.ManyToManyField(Transaction)
    date = models.DateTimeField(auto_now_add=True)
