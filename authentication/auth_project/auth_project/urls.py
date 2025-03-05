from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Default redirect function
def home_redirect(request):
    return redirect("login")  # Redirect to the login page

urlpatterns = [
    path("", home_redirect),  # Redirect the root URL to login
    path("admin/", admin.site.urls),
    path("auth/", include("auth_app.urls")),
]
