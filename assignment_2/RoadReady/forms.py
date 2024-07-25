from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import *
from django.db import transaction
from django.utils import timezone
from .models import Feedback

    
class Signupform(UserCreationForm):
    # This form is used for user signup. It extends Django's built-in UserCreationForm.
    # It includes fields for email, username, and password.
    email = forms.EmailField(max_length=200, required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput( attrs={'class':'form-control', 'type':'password' }))
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput( attrs={'class':'form-control', 'type':'password' }))
    class Meta:
        model = User  # The model to be used with this form is User.
        fields = ['email','username', 'password1', 'password2']  # The fields to be included in this form.
        
    @transaction.atomic
    def save(self):
        # This method is used to save the form data to the database.
        user = super().save(commit=True)  # Save the form data to the user object but don't save it to the database yet.
        user.is_student = True  # Set the is_student field to True.
        print(user)
        user.save()  # Save the user object to the database.
        return user  # Return the user object.
        
    
class UserLoginForm(AuthenticationForm):
    # This form is used for user login. It extends Django's built-in AuthenticationForm.
    # It includes fields for username and password.
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password' ,'placeholder':'Your password'}))
    
class BookingForm(forms.ModelForm):
    # This form is used for booking. It extends Django's built-in ModelForm.
    # It includes fields for date, start time, end time, lessons, and instructor.
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
    class Meta:
        model = Booking  # The model to be used with this form is Booking.
        fields = ['date', 'start_time', 'end_time','lessons', 'instructor']  # The fields to be included in this form.

    def clean(self):
        # This method is used to validate the form data.
        # It checks if the date is in the past and if the booking conflicts with existing bookings.
        end_time = self.cleaned_data['end_time']
        date = self.cleaned_data['date']
        Lessons = self.cleaned_data['lessons']
        Instructor = self.cleaned_data['instructor']
        start_time = self.cleaned_data['start_time']

        if date < timezone.now().date():
            raise forms.ValidationError(message='Date cannot be in the past')

        bookings = Booking.objects.filter(date=date, lessons=Lessons, instructor = Instructor)
        for booking in bookings:
            if start_time >= end_time:
                raise forms.ValidationError(message='Error! Start Time is greater than the End Time')
            elif start_time == booking.start_time and end_time == booking.end_time:
                raise forms.ValidationError(message='Invalid, already booked')
            elif start_time > booking.start_time and start_time < booking.end_time:
                raise forms.ValidationError(message='Invalid, already booked')
            elif start_time < booking.start_time and end_time > booking.start_time:
                raise forms.ValidationError(message='Invalid, already booked')
            elif Lessons == booking.lessons:
                raise forms.ValidationError(message='Lesson, already booked')
                
        return self.cleaned_data  # Return the cleaned data.
    
class UpdateUserForm(forms.ModelForm):
    # This form is used for updating user profile. It extends Django's built-in ModelForm.
    # It includes fields for username, email, and profile image.
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = User  # The model to be used with this form is User.
        fields = ['username', 'email', 'profile_image']  # The fields to be included in this form.        

class FeedbackForm(forms.ModelForm):
    # This form is used for feedback. It extends Django's built-in ModelForm.
    # It includes all fields from the Feedback model.
    class Meta:
        model = Feedback  # The model to be used with this form is Feedback.
        exclude = []  # No fields are excluded from this form.
        widgets = {
            # The 'customer_name', 'email', and 'details' fields use TextInput and Textarea widgets with the 'form-control' CSS class.
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CheckoutForm(forms.Form):
    # This form is used for checkout. It extends Django's built-in Form.
    # It includes fields for first name, last name, username, email, address, credit card name, credit card number, credit card expiration date, and credit card CVV.
    firstName = forms.CharField(min_length=2, max_length=30, required=True)
    lastName = forms.CharField(min_length=2, max_length=30, required=True)
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=False)
    address = forms.CharField(min_length=5, max_length=100, required=True)
    address2 = forms.CharField(min_length=5, max_length=100, required=False)
    #paymentMethod = forms.CharField(max_length=30, required=True)
    cc_name = forms.CharField(max_length=30, required=True)
    cc_number = forms.CharField(max_length=16, required=True)
    cc_expiration = forms.DateField(required=True)
    cc_cvv = forms.CharField(max_length=3, required=True)



