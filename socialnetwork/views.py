from django.http import HttpResponse
from django.shortcuts import render


# -------------------- HOME PAGE VIEW---------------
def home_view(request):
    user = request.user
    hello = "Hello"

    context = {
    'user': user,
    'hello': hello,
    }
    return render(request, 'main/home.html', context)
