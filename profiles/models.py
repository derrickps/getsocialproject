from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save # for signal
from profiles.utils import get_random_code  # for slug
from django.template.defaultfilters import slugify  # for slug
from django.db.models import Q

# Create your models here.

#--------------------------------------------USER PROFILE MODEL MANAGER-------------------
class ProfileManager(models.Manager):

    def get_all_profiles_to_invite(self, sender):  # all the profile that are available us to invite
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile)) #filtering if we are the sender or receiver
        print(qs)
        print("#########")

        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        print(accepted)
        print("#########")

        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        print("#########")
        return available


    def get_all_profiles(self, me):  # all the profile in the system excluding our own
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

    def get_friendsAPI(self):
        friendlist = Profile.objects.all().values('friends',)
        return friendlist

#------------------------------------------------- USER PROFILE MODEL---------------------------------------
class Profile(models.Model):   # Profile model
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    mobile = models.CharField(max_length=10, unique=True)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)


    objects = ProfileManager()   # calling profile model manager

    def __str__(self):
        return f"{self.user.username}"

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})

    def get_friends(self):  # get complete info of friends
        return self.friends.all()

    def get_friends_no(self): # get total no. of friends
        return self.friends.all().count()

    def get_posts_no(self):  # get total no. of posts
        return self.posts.all().count()

    def get_all_authors_posts(self): # get all posts
        return self.posts.all()

    # def get_likes_given_no(self): # get total no. of likes given
    #     likes = self.like_set.all()
    #     total_liked = 0
    #     for item in likes:
    #         if item.value=='Like':
    #             total_liked += 1
    #     return total_liked
    #
    # def get_likes_recieved_no(self):  # get total no. of like recieved
    #     posts = self.posts.all()
    #     total_liked = 0
    #     for item in posts:
    #         total_liked += item.liked.all().count()
    #     return total_liked




    __initial_first_name = None  # code to set slug permanently
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name  


    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug=="":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs) #upto here



STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)

#-------------------------------------------RELATIONSHIP MODEL MANAGER----------------------
class RelationshipManager(models.Manager):    # Invitation Received model manager
    def invatations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs


#---------------------------------------------RELATIONSHIP MODEL----------------------
class Relationship(models.Model): 
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"





