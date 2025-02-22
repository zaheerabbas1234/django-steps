from django.shortcuts import render

# Sample Data
data = [
    {"id": 1, "name": "Alice", "age": 25},
    {"id": 2, "name": "Bob", "age": 30},
    {"id": 3, "name": "Charlie", "age": 22},
]

def home(request):
    return render(request, 'home.html', {'data': data})
