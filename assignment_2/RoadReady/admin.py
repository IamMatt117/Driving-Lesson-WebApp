from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User) # Register the User model with the admin site.
admin.site.register(Booking) # Register the Booking model with the admin site.
admin.site.register(Lesson)
admin.site.register(Instructor)
admin.site.register(Feedback)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Transaction)