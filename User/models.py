from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.models import SocialAccount
from Creator.models import*

# Create your models here.

class CustomUser(AbstractUser):
    said = models.ForeignKey(SocialAccount, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=255,null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, blank=True)
    picture = models.ImageField(upload_to="UserPictures/Profile", blank=True, null=True)
    bannerimage = models.ImageField(upload_to="UserPictures/Banner", blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def save_social_account_data(self, social_account):
        if social_account.provider == 'google':
            extra_data = social_account.extra_data
            self.name = extra_data.get('name', '')
            self.email = extra_data.get('email', '')
            self.picture = extra_data.get('picture', '')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        permissions = [
            ("view_social_account_data", "Can view social account data in CustomUser"),
        ]



class FormUser(models.Model):
    name = models.CharField(max_length=50)
    usr_name = models.CharField(max_length=50,null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    picture = models.ImageField(upload_to="UserPictures/Profile",null=True, blank=True)
    bannerimage = models.ImageField(upload_to="UserPictures/Banner",null=True,blank=True)
    date_joined = models.DateTimeField(auto_now_add=True,null=True)

class Playlist(models.Model):
    PlaylistName = models.CharField(max_length=50)
    Playlist_Cover = models.ImageField(upload_to="User/Playlist", null=True, blank=True)
    UsrId = models.ForeignKey(FormUser, on_delete=models.CASCADE)

class PlaylistItem(models.Model):
    Plid = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    MusicId = models.ForeignKey(Music, on_delete=models.CASCADE)

class FollowCr(models.Model):
    follower = models.ForeignKey(FormUser, on_delete=models.CASCADE, related_name='following_User')
    following = models.ForeignKey(Creators, on_delete=models.CASCADE, related_name='followed_Creator')
    date_followed = models.DateTimeField(auto_now_add=True)