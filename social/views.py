from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from profiles.models import Profile

# Create your views here.

#----------------------------- FUNCTION FOR SEARCHING PROFILE
def searchuser(request):
    if request.method == "POST":
        searched = request.POST['q']
        #searchedprofile = Profile.objects.filter(slug__contains=searched)
        #searchedprofile = Profile.objects.filter(Q(slug__contains=searched) | Q(email__istartswith=searched) | Q(mobile__iexact=searched) | Q(user__istartswith=searched))
        searchedprofile = Profile.objects.filter(Q(first_name__contains=searched) | Q(email__istartswith=searched) | Q(mobile__iexact=searched))
        return render(request, 'main/search.html',{'searched':searched,'searchedprofile':searchedprofile})
    else:
        return render(request, 'main/search.html')
