from tkinter.constants import BASELINE

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from Login.forms import LoginForm, RegistrationForm
from Login.models import BaseUser


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')

            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)

                # a simple code to add a token to make the user signed in cuz of remember me
                if remember_me:
                    request.session.set_expiry(1209600) # this is for... 2 weeks... 1209600 seconds
                else:
                    request.session.set_expiry(0)

                return redirect('profile')  # Redirect to a profile page maybe?
            else:
                # Handle invalid login attempt
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()

    # the login.html is the html file :)
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)  # Bind the POST data to the form
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            # This else part ensures that if the form is not valid, it will be passed to the template
            empty_fields = []
            for field in form.fields:
                value = request.POST.get(field)
                if not value:  # If the field is empty
                    empty_fields.append(field)
            print(f"failed to add user: {request.POST['username']}, empty_fields: {'{ ' + ' }, { '.join(empty_fields) + ' }'}, reason: {form.errors}")
    else:
        form = RegistrationForm()  # Create an empty form for GET requests

    return render(request, 'sign_up.html', {'form': form})  # Pass the form back to the template

def user_list(request):
    # Query all users
    users = BaseUser.objects.all()  # Retrieves all entries in BasicUser table
    return render(request, 'user_list.html', {'users': users})