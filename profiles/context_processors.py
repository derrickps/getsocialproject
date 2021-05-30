from .models import Profile, Relationship

#--------------------------FOR USER PROFILE PIC ON NAVBAR AVATAR------------------------
def profile_pic(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        pic = profile_obj.avatar
        return {'picture':pic}
    return {}

#--------------------------------INVITATION RECIEVED COUNT IN NAVBAR------------------
def invatations_received_no(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        qs_count = Relationship.objects.invatations_received(profile_obj).count()
        return {'invites_num':qs_count}
    return {}


# SIMPLE INTERFACE THAT TAKES ARHUMENTS AS HTTP REQUEST OBJECT AND RETURN DICTIONARY THAT CAN BE ADDED TO OUR TEMPLATE CONTEXT