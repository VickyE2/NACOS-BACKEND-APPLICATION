from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from Login.forms import LoginForm


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
