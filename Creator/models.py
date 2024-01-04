from django.db import models
from AdminApp.models import*

# Create your models here.
class Creators(models.Model):
    FullName = models.CharField(max_length=50)
    UsrName = models.CharField(max_length=50)
    MusicRole = models.CharField(max_length=10)
    Country = models.CharField(max_length=10)
    Email = models.EmailField(max_length=50, unique=True)
    Password = models.CharField(max_length=100)
    Profile_Picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    Profile_Banner = models.ImageField(upload_to='profile_banners/', blank=True, null=True)
    doj=models.DateTimeField(auto_now_add=True,null=True)


class Albums(models.Model):
    Album_Name = models.CharField(max_length=50)
    CrId = models.ForeignKey(Creators, on_delete=models.CASCADE)
    Album_Cover = models.ImageField(upload_to='Creator/Album_Covers', blank=True, null=True)
    

class Follow(models.Model):
    follower = models.ForeignKey(Creators, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(Creators, on_delete=models.CASCADE, related_name='followers')
    date_followed = models.DateTimeField(auto_now_add=True)

class Music(models.Model):
    Title = models.CharField(max_length = 100)
    CrId = models.ForeignKey(Creators, on_delete=models.CASCADE)
    Crrole = models.CharField(max_length = 50, null=True)
    audio_file = models.FileField(upload_to="music/")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    Language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    release_date = models.DateField()
    Album = models.ForeignKey(Albums, on_delete=models.SET_NULL, null=True)
    cover_art = models.ImageField(upload_to="music_covers/")
    collaborator_1 = models.ForeignKey(Creators, on_delete=models.SET_NULL, null=True, related_name='collaborator_1')
    c1role = models.CharField(max_length = 50, null=True,blank=True)
    collaborator_2 = models.ForeignKey(Creators, on_delete=models.SET_NULL, null=True, related_name='collaborator_2')
    c2role = models.CharField(max_length = 50, null=True,blank=True)
    collaborator_3 = models.ForeignKey(Creators, on_delete=models.SET_NULL, null=True, related_name='collaborator_3')
    c3role = models.CharField(max_length = 50, null=True,blank=True)
    Mood = models.ForeignKey(MusicMood, on_delete=models.CASCADE, null=True)

class CrPlaylist(models.Model):
    PlaylistName = models.CharField(max_length=50)
    Playlist_Cover = models.ImageField(upload_to="Creator/CrPlaylist",null=True, blank=True)
    CrId = models.ForeignKey(Creators, on_delete=models.CASCADE)
    PlStatus = models.IntegerField(default=0)

class CrPlaylistItem(models.Model):
    CrPlid = models.ForeignKey(CrPlaylist, on_delete=models.CASCADE)
    MusicId = models.ForeignKey(Music, on_delete=models.CASCADE)

class Notifications(models.Model):
    Crid = models.ForeignKey(Creators, on_delete=models.CASCADE, related_name='notification_receiver')
    FlwCrid = models.ForeignKey(Creators, on_delete=models.CASCADE, related_name='notification_generator')
    Msg = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

class CollabNotifications(models.Model):
    Crid = models.ForeignKey(Creators, on_delete=models.CASCADE, related_name='Collab_notification_receiver')
    FlwCrid = models.ForeignKey(Creators, on_delete=models.CASCADE, related_name='Collab_notification_generator')
    Msg = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
