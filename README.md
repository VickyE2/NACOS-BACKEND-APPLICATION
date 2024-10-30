<h1 style="text-align: center;"><b>NACOS BACKEND TASK</b></h1>

<p style="color: #999999; text-align: center;"><b>So this is my backend task. My name is Popoola Victor. To integrate my backend to a front end you'll have to use the django web-frame...</b></p>

```html
<form method="post">
                    {% csrf_token %}
                    <p>
                        {{ form.email.label_tag }}
                        {{ form.email }}
                    </p>
                    <p>
                        {{ form.password.label_tag }}
                        {{ form.password }}
                    </p>
                    {% if form.errors %}
                        <div class="some_error_class">
                            {% for field, errors in form.errors.items %}
                            <!-- Run a loop for errors in the form -->
                                {% for error in errors %}
                            <!-- put a paragraph of the error -->
                                    <p>{{ error }}</p>
                                {% endfor %} <!-- ends a condition :) -->
                            {% endfor %}
                        </div>
                    {% endif %}

                    <div class="a-class">
                        <label id="some_label_to_hold_a_remember_me">
                            {{ form.remember_me }} {{ form.rememberme.label }}
                        </label>
                        <a id="some_link_id" href="re_register.html">Forgotten Password?</a>
                    </div>

                    <button type="submit" id="button_id">Log in</button>
                </form>
```

so now to start the `{% csrf_token %}` is used to initialise the form. 
`{{ form.email.label_tag }}` is the id of the form element. in this case the label of the element username as seen here:
```python
email = forms.CharField(
    label="Email",
    required=True,
    widget=forms.TextInput(attrs={'placeholder': 'mynameisemail@gmail.com', 'id': 'email'})
    # That is email is used when styling. when styling the css the id should
    # be (#)email same for the remaining fields
)
```
`{% if form.errors %}` is a condition that if the form has errors.

For the css the id of the element is found the code. From the above example, the id of `email` is `email` :| 
so in the css to style the element we'd use:
```css
    #email {
        border: 2px solid rgb(218, 218, 218);
        position: relative;
        border-radius: 8px;
        font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-size: 15px;
        width: 350px;
        height: 40px;
        text-align: left;
        padding-left: 14px;
    }
```

so this would style the form element. (the element is dependent of form position jsut like how you'd put an email field in an email div you put this in its required position :] )

To link a css naturally you'd do this:
```html
<link rel="stylesheet" href="css/somerandomcss.css">
``` 
but due to the work of static files you'd do this instead:
```html 
<link rel="stylesheet" href="{% static 'css/login_css.css' %}">
```
where you place the css file in the `static/css` folder but for that to be functional, at the begining of the html file you should do this:
```html
{% load static %}
<!DOCTYPE html>
<html>
    ...
</html>
```

and also place the html file in the `Login/templates` folder saving it as `login.html`
Since it isn't really ideal to have a login without a way to signup just add a html to that same folder with name `sign_up.html`

SO js for refrence sake this is a demo:
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Login</title>
        <link rel="stylesheet" href="{% static 'css/login_css.css' %}">
    </head> 
    <body class="main2">
        <div class="main">
            <div class="login-box">
                <div class="current">
                    <h3 id="title">Login</h3>
                </div>
                <form method="post">
                    {% csrf_token %}
                    <p>
                        {{ form.username.label_tag }}
                        {{ form.username }}
                    </p>
                    <p>
                        {{ form.password.label_tag }}
                        {{ form.password }}
                    </p>
                    {% if form.errors %}
                        <div class="error">
                            {% for field, errors in form.errors.items %}
                                {% for error in errors %}
                                    <p>{{ error }}</p>
                                {% endfor %}
                            {% endfor %}
                        </div>
                    {% endif %}

                    <div class="line-container">
                        <label id="checkbox">
                            {{ form.remember_me }} {{ form.rememberme.label }}
                        </label>
                        <a id="fpwd2" href="re_register.html">Forgotten Password?</a>
                    </div>

                    <button type="submit" id="button-1">Log in</button>
                </form>
                <p id="siw">Or continue with</p>
                <div class="button-container-1">
                    <button type="button" id="button-3" onclick="openSameWindowWebpage('twitter_login.html')"><img src="{% static 'images/logos/twitter_logo.png' %}" alt="Twitter logo"></button>
                    <button type="button" id="button-4"><img src="{% static 'images/logos/google_logo.png' %}" alt="Google logo"></button>
                </div>
                <p><a id="fpwd" href="{% url 'sign_up' %}">Dont have an account?</a></p>
            </div>
        </div>
        <script src="{% static 'js/global_scripts.js' %}"></script>
    </body>
</html>
```

From here my css is found ind the `static/css` folder of this project with name `login_css.css` and the javascript found in `static/js` folder with name `global_scripts.js`.

the reason the form has these names is because of how i made the form in the django framework:
```python
class LoginForm(AuthenticationForm):
    email = forms.CharField(
        label="Email",
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'mynameisemail@gmail.com', 'id': 'email'})
        # That is email is used when styling. when styling the css the id should
        # be (#)email same for the remaining fields
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'id': 'password'})

    )
    remember_me = forms.BooleanField(
        label="Remember me",
        required=False,
        widget=forms.CheckboxInput(attrs={'placeholder': 'Remember me', 'id': 'remember_me'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            self.add_error('email', "Username can't be empty.")
        if not BaseUser.objects.filter(email=email).exists():
            self.add_error('email', "Username does not exist")
            self.add_error('email', "Email already exists")
        return email

    def clean_password(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if BaseUser.email:
            self.add_error('password', "Username does not exist")
        if len(password) < 8:
            self.add_error('password', "Password must be at least 8 characters long.")
        if not re.search(r"\d", password):
            self.add_error('password', "Password must contain at least one number.")
        if not re.search(r"[!@#$%^&*()_+={}\[\]:;\"'<>?,./]", password):
            self.add_error('password', "Password must contain at least one special character.")

        return password
```

If you noticed the id of the email element in the LoginForm is `email` so in the css it would be #email...as mentioned earlier,
the label of it is where the `{{ form.username.label_tag }}` comes in so to style it, it would be:
```css
#email {
    ...email_styling...
}

label[for="email"] {
    ...email_label_styling...
}
```

if you want to add the remember me checkbox:
```html
<label id="checkbox">
    {{ form.remember_me }} {{ form.rememberme.label }}
</label>
```
p.s : the label with id: "checkbox" is just to style where the remember_me is...not specifically needed...

where the `form.remember_me` is the element `remember_me = forms.BooleanField(...` the label being `form.rememberme.label`

I think that covers everything about how to use it with the front end....

to visit the website, you'll run this command in the python shell: `python manage.py runserver` and visit the gemerated ip adress (usually ``http://127.0.0.1:8000/)

[It's Optional]
So for a sign up screen you'll need these elements:

- First name and last name fields
- A Username field
- An Email field
- Two password fields (password and confirm_password)

You should still use the `{{ form.email }}`...etc to place it the name for password is `{{ password1 }}` and for the confirm `{{ password2 }}`
for first name `{{ first_name }}` and last name `{{ last_name }}`

to visit it you'd go to the generated ip and `/signup/` for the userlist that was included you'd use `/users/`
