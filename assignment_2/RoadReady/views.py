from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import * 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.urls import reverse
from datetime import datetime
from django.views.decorators.http import require_POST
import re
from django.core.exceptions import ValidationError

def index(request):
    # Fetch all Instructor objects from the database. This is equivalent to SELECT * FROM Instructor in SQL.
    instructor = Instructor.objects.all()  
    # Render the index page. The second argument is a context dictionary that maps variable names, 
    # which will be available in the template, to their Python objects.
    return render(request, 'index.html',  {'instructor' : instructor})
    
class SignupView(CreateView):
    # This is a class-based view for user signup. It uses Django's built-in CreateView which is a view 
    # for creating a new object, with a response rendered by a template.

    # User model will be used to create a new instance of the model (a new user).
    model = User
    # Signupform is the name of the form class to be used for user data validation.
    form_class = Signupform
    # The HTML template to be used in this view is 'register.html'.
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        # This method is used to get context data which is then available in the template.
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = form.save()  # Save the user form data to the database.
        login(self.request, user)  # Log the user in.
        return redirect('/')  # Redirect to the homepage.
    
class UserLoginView(LoginView):
    # This is a class-based view for user login. It uses Django's built-in LoginView.
    template_name='login.html'  # The HTML template to be used in this view is 'login.html'.

def logout_user(request):
    # This function logs out the user.
    logout(request)  # Remove the authenticated user's ID from the request and flush their session data.
    return redirect("/")  # Redirect to the homepage.

@login_required
def booking(request):
    # This function handles the booking form. The @login_required decorator means the user must be authenticated to access this view.
    user = request.user  # Get the current logged in user.
    if request.method == 'POST':
        # If the form has been submitted,
        form = BookingForm(request.POST)  # Populate the form with the submitted data.
        if form.is_valid():
            # If the form data is valid,
            booking = form.save(commit=False)  # Save the form data to the booking object but don't save it to the database yet.
            booking.user_id = user  # Set the user_id to the current user.
            booking.save()  # Save the booking object to the database.
            return redirect('timetable')  # Redirect to the timetable page.
        else:
            # If the form data is not valid, render the form again with error messages.
            return render(request, 'booking.html', {'form': form})
    else:
        # If the form has not been submitted yet, display the form.
        form = BookingForm()
        return render(request, 'booking.html', {'form': form})

def pricing(request):
    # Fetch all Product objects from the database.
    products = Product.objects.all()
    # Render the pricing page with the product data.
    return render(request, 'pricing.html', {'products': products})

@login_required
def checkout(request):
    # Render the checkout page.
    return render(request, 'checkout.html')
    
@login_required
def profile(request):
    # This function handles the profile update form.
    if request.method == 'POST':
        # If the form has been submitted,
        form = UpdateUserForm(request.POST, instance=request.user)  # Populate the form with the submitted data.
        if form.is_valid():
            # If the form data is valid,
            form.save()  # Save the form data to the database.
            messages.success(request, 'Your profile is updated successfully')  # Display a success message.
            return redirect(to='/')  # Redirect to the homepage.
    else:
        # If the form has not been submitted yet, display the form.
        form = UpdateUserForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

@login_required
def profile_view(request):
    # This function renders the profile view page.
    user = request.user  # Get the current logged in user.
    return render(request, 'profile_view.html')
    
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    # This is a class-based view for changing password. It uses Django's built-in PasswordChangeView.
    template_name = 'change_password.html'  # The HTML template to be used in this view is 'change_password.html'.
    success_message = "Successfully Changed Your Password"  # The success message to be displayed when the password is changed successfully.
    success_url = reverse_lazy('index')  # The URL to redirect to when the password is changed successfully.
    
def feedback_form(request):
    # This function handles the feedback form.
    if request.method == 'POST':
        # If the form has been submitted,
        form = FeedbackForm(request.POST)  # Populate the form with the submitted data.
        if form.is_valid():
            # If the form data is valid,
            form.save()  # Save the form data to the database.
            return redirect("/")  # Redirect to the homepage.
    else:
        # If the form has not been submitted yet, display the form.
        form = FeedbackForm()
    return render(request, 'feedback_form.html', {'form': form})

@login_required
def timetable(request):
    # This function renders the timetable page.
    user = request.user  # Get the current logged in user.
    booking = Booking.objects.filter(user_id=user).order_by('date')  # Get all bookings of the current user ordered by date.
    return render(request, 'booked.html', {'booking':booking})

def product_list(request):
    # Fetch all Product objects from the database.
    products = Product.objects.all()
    # Render the product list page with the product data.
    return render(request, 'pricing.html', {'products': products})

@login_required
def add_to_basket(request, prodid):
    # This function adds a product to the user's basket.
    product = get_object_or_404(Product, id=prodid)  # Get the product with the given id.
    basket, created = Basket.objects.get_or_create(user=request.user)  # Get or create a basket for the current user.
    basket_item, created = BasketItem.objects.get_or_create(product=product, basket=basket)  # Get or create a basket item for the product.
    return redirect(reverse('checkout'))  # Redirect to the checkout page.

from datetime import datetime

def checkout(request):
    # Get the basket for the current user or return a 404 error if not found.
    basket = get_object_or_404(Basket, user=request.user)
    # Calculate the total price of all items in the basket.
    total = sum(item.product.price for item in basket.basketitem_set.all())
    if request.method == 'POST':
        # If the request method is POST, process the checkout.
        order = Order(user=request.user)  # Create a new order for the current user.
        order.save()  # Save the order to the database.
        # Get or create a billing address for the current user.
        address, created = BillingAddress.objects.get_or_create(user=request.user)
        # Update the billing address with the data from the POST request.
        address.first_name = request.POST['firstName']
        address.last_name = request.POST['lastName']
        address.username = request.POST['username']
        address.email = request.POST['email']
        address.address = request.POST['address']
        address.address2 = request.POST['address2']
        address.save()  # Save the updated billing address to the database.
        for item in basket.basketitem_set.all():
            # For each item in the basket, create a new transaction.
            transaction = Transaction(product=item.product)
            # Update the transaction with the data from the POST request.
            transaction.payment_method = request.POST['paymentMethod']
            transaction.card_name = request.POST['cc-name']
            transaction.card_number = request.POST['cc-number']
            card_expiry_str = request.POST['cc-expiration']
            try:
                # Try to parse the card expiry date from the POST request.
                card_expiry = datetime.strptime(card_expiry_str, '%Y-%m-%d').date()
                transaction.card_expiry = card_expiry
            except ValueError:
                # If the date format is invalid, ignore it.
                pass
            transaction.card_cvv = request.POST['cc-cvv']
            transaction.save()  # Save the transaction to the database.
            order.transactions.add(transaction)  # Add the transaction to the order.
        basket.basketitem_set.all().delete()  # Clear the basket.
        # Redirect to the order complete page with the order ID.
        return redirect('order_complete', order_id=order.id)
    else:  # GET request
        # If the request method is GET, display the checkout page.
        # Get or create a billing address for the current user.
        address, created = BillingAddress.objects.get_or_create(user=request.user)
        # Render the checkout page with the basket, address, and total.
        return render(request, 'checkout.html', {'basket': basket, 'address': address, 'total': total})

def order_complete(request, order_id):
    # Get the order with the given ID or return a 404 error if not found.
    order = get_object_or_404(Order, id=order_id)
    # Get all transactions for the order.
    transactions = order.transactions.all()
    # Render the order complete page with the order and transactions.
    return render(request, 'order_complete.html', {'order': order, 'transactions': transactions})

@require_POST
def remove_from_basket(request, item_id):
    # Get the basket item with the given ID and user or return a 404 error if not found.
    item = get_object_or_404(BasketItem, id=item_id, basket__user=request.user)
    item.delete()  # Delete the basket item from the database.
    return redirect('checkout')  # Redirect to the checkout page.

@login_required
def order_history(request):
    # This function renders the order history page.
    user = request.user  # Get the current logged in user.
    orders = Order.objects.filter(user=user)  # Get all orders for the current user.
    # Render the order history page with the orders.
    return render(request, 'order_history.html', {'orders': orders})
