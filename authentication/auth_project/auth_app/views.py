from django.http import HttpResponse
from django.shortcuts import redirect
from django.middleware.csrf import get_token

def generate_html(content):
    """Dynamically generates an HTML response."""
    return f"""
    <html>
    <head><title>Auth System</title></head>
    <body>
        {content}
    </body>
    </html>
    """

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return HttpResponse(generate_html("<p style='color:red;'>Username & password required</p>" + register_form(request)))

        request.session["username"] = username
        request.session["password"] = password
        return redirect("login")

    return HttpResponse(generate_html(register_form(request)))

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        stored_username = request.session.get("username")
        stored_password = request.session.get("password")

        if username == stored_username and password == stored_password:
            request.session["logged_in"] = True
            return redirect("dashboard")

        return HttpResponse(generate_html("<p style='color:red;'>Invalid credentials</p>" + login_form(request)))

    return HttpResponse(generate_html(login_form(request)))

def dashboard_view(request):
    if not request.session.get("logged_in"):
        return redirect("login")

    csrf_token = get_token(request)
    content = f"""
    <h2>Welcome, {request.session.get('username')}</h2>
    <p>You are logged in.</p>
    <form action='/auth/logout/' method='post'>
        <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
        <button type='submit'>Logout</button>
    </form>
    """
    return HttpResponse(generate_html(content))

def logout_view(request):
    request.session.flush()
    return redirect("login")

def register_form(request):
    csrf_token = get_token(request)
    return f"""
    <h2>Register</h2>
    <form method="post">
        <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
        <label>Username:</label><input type="text" name="username" required><br><br>
        <label>Password:</label><input type="password" name="password" required><br><br>
        <button type="submit">Register</button>
    </form>
    <p>Already have an account? <a href='/auth/login/'>Login</a></p>
    """

def login_form(request):
    csrf_token = get_token(request)
    return f"""
    <h2>Login</h2>
    <form method="post">
        <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
        <label>Username:</label><input type="text" name="username" required><br><br>
        <label>Password:</label><input type="password" name="password" required><br><br>
        <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <a href='/auth/register/'>Register</a></p>
    """
