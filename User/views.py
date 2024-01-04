from django.shortcuts import render,redirect
from Creator.models import Creators
from User.models import *
from Creator.models import *
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from fuzzywuzzy import fuzz
from django.shortcuts import get_object_or_404
import random 
from random import randint
from django.http import JsonResponse
from datetime import date
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import os


# Create your views here.


def Index(request):
    pldata = playlist_data(request)
    messages_to_display = messages.get_messages(request)
    return render(request,"UserTemp/User_Index.html",{'pldata':pldata,'messages_to_display':messages_to_display})

def playlist_data(request):
    user_id = request.session.get('Usrid')
    if user_id:
        user = FormUser.objects.get(id=user_id)
        if user:
            playlist_data = Playlist.objects.filter(UsrId=user)
            return list(playlist_data)
        
def generate_random_color(last_color=None):
    color_palette = [ "#008600","#374ca9","#c9b8ab", "#ff7300", "#ff0059", "#a600ff","#b2702d", "#00ac7e","#dfab01","#7300ff"]
    available_colors = [color for color in color_palette if color != last_color]
    random_color = available_colors[randint(0, len(available_colors) - 1)]
    return random_color

def Home(request):
    if 'Usrid' in request.session:
        pldata = playlist_data(request)
        user_id = request.session['Usrid']
        langdata = Language.objects.all().order_by('?')[:6]
        gdata = Genre.objects.all().order_by('?')[:6]
        albums_data = Albums.objects.all().order_by('?')[:6]
        following_creators = Creators.objects.filter(followed_Creator__follower_id=user_id)
        if following_creators.exists():
            music_data = Music.objects.filter(Q(CrId__in=following_creators) | Q(collaborator_1__in=following_creators) | Q(collaborator_2__in=following_creators) | Q(collaborator_3__in=following_creators)).order_by('?')[:6]
        else:
            music_data = Music.objects.all().order_by('?')[:6]
        current_date = date.today()
        latest_releases = Music.objects.filter(release_date__lt=current_date).order_by('-release_date')[:6]
        last_color = None
        color_list = []
        for item in langdata:
            color = generate_random_color(last_color)
            color_list.append(color)
            last_color = color
        messages_to_display = messages.get_messages(request)
        return render(request, "UserTemp/Homepage.html", {'pldata': pldata,
                                                        'Ldata': zip(langdata, color_list),
                                                        'Gdata':gdata,
                                                        'albums_data':albums_data,
                                                        'music_data':music_data,
                                                        'latest_releases':latest_releases,
                                                        'messages_to_display':messages_to_display,
                                                        })
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')


def SocialHome(request):
        pldata = playlist_data(request)
        # user_id = request.session['Usrid']
        langdata = Language.objects.all().order_by('?')[:6]
        gdata = Genre.objects.all().order_by('?')[:6]
        albums_data = Albums.objects.all().order_by('?')[:6]
        # following_creators = Creators.objects.filter(followed_Creator__follower_id=user_id)
        # if following_creators.exists():
        #     music_data = Music.objects.filter(Q(CrId__in=following_creators) | Q(collaborator_1__in=following_creators) | Q(collaborator_2__in=following_creators) | Q(collaborator_3__in=following_creators)).order_by('?')[:6]
        # else:
        #     music_data = Music.objects.all().order_by('?')[:6]
        current_date = date.today()
        latest_releases = Music.objects.filter(release_date__lt=current_date).order_by('-release_date')[:6]
        last_color = None
        color_list = []
        for item in langdata:
            color = generate_random_color(last_color)
            color_list.append(color)
            last_color = color
        messages_to_display = messages.get_messages(request)
        return render(request, "UserTemp/Homepage.html", {'pldata': pldata,
                                                        'Ldata': zip(langdata, color_list),
                                                        'Gdata':gdata,
                                                        'albums_data':albums_data,
                                                        # 'music_data':music_data,
                                                        'latest_releases':latest_releases,
                                                        'messages_to_display':messages_to_display,
                                                        })

def Login(request):
    if request.method == 'POST':
        Mail = request.POST.get('mail')
        Pass = request.POST.get('pass')
        Crlogin = Creators.objects.filter(Email=Mail,Password=Pass).count()
        Fm_User = FormUser.objects.filter(email=Mail,password=Pass).count()
        Tunely_Admin = Admindata.objects.filter(mail=Mail,Password=Pass).count()
        if Crlogin > 0:
            Cr = Creators.objects.get(Email=Mail,Password=Pass)
            request.session['Crid'] = Cr.id
            Crname = Cr.UsrName
            messages.success(request, 'Successfully Logged in as ' + Crname )
            return redirect("Creator:CrHome")
        elif Fm_User > 0:
            Usr = FormUser.objects.get(email=Mail,password=Pass)
            request.session['Usrid'] = Usr.id
            UsrName = Usr.name
            messages.success(request, 'Successfully Logged in as ' + UsrName )
            return redirect('User:Home')
        elif Tunely_Admin > 0:
            Admn = Admindata.objects.get(mail=Mail,Password=Pass)
            request.session['Admnid'] = Admn.id
            return redirect('TunelyAdmin:Index')
        else:
            error = "Invalid email or password !"
            return render(request,"UserTemp/Login.html",{'ERR':error})
    else:
        messages_to_display = messages.get_messages(request)
        return render(request,"UserTemp/Login.html", {'messages_to_display': messages_to_display})

def Usrlogout(request):
    if 'Usrid' in request.session:
        del request.session["Usrid"]
        messages.success(request, 'Logged Out, Successfully')
        return redirect("User:Login")
    else:
        return redirect('User:Login')
    
def SignUp(request):
    if request.method == "POST":
        name = request.POST.get('Name')
        email = request.POST.get('mail')
        password = request.POST.get('pass')
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'This Mail id is linked to an existing account. Please choose a different email or login to the existing account.')
            return redirect('User:SignUp')
        elif FormUser.objects.filter(email=email).exists():
            messages.warning(request, 'This Mail id is linked to an existing account. Please choose a different email or login to the existing account.')
            return redirect('User:SignUp')
        FormUser.objects.create(name=name, 
                                email=email, 
                                password=password)
        messages.success(request, 'Sign-Up successful, Please login to your account.')
        return redirect('User:Login')
    messages_to_display = messages.get_messages(request)
    return render(request, 'UserTemp/SignUp.html',{'messages_to_display':messages_to_display})

def UsrProfile(request):
    if 'Usrid' in request.session:
        usr = FormUser.objects.get(id=request.session['Usrid'])
        user = get_object_or_404(FormUser, id=usr.id)
        following_creators = FollowCr.objects.filter(follower=user)
        followed_creators_details = []
        for follow_relation in following_creators:
            followed_creator = follow_relation.following
            creator_details = {
                'id': followed_creator.id,
                'UsrName': followed_creator.UsrName,
                'Profile_Picture': followed_creator.Profile_Picture.url if followed_creator.Profile_Picture else None,
            }
            followed_creators_details.append(creator_details)
        pldata = playlist_data(request)
        return render(request, "UserTemp/UsrProfile.html",{'pldata':pldata,
                                                            'USR':usr,
                                                            'Following':followed_creators_details,
                                                            })
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def EditPage(request,usrid):
    if 'Usrid' in request.session:
        usr = FormUser.objects.get(id=usrid)
        pldata = playlist_data(request)
        return render(request, "UserTemp/Editprofile.html",{'pldata':pldata,'USR':usr})
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def UpdateProfile(request, usrid):
    if request.method == "POST":
        Unam = request.POST.get("usrname")
        name = request.POST.get("name")
        try:
            banner_img = request.FILES['banner-img']
            fs_banner = FileSystemStorage()
            banner_file = fs_banner.save(banner_img.name, banner_img)
        except MultiValueDictKeyError:
            banner_file = FormUser.objects.get(id=usrid).bannerimage
        try:
            profile_img = request.FILES['profile-img']
            fs_profile = FileSystemStorage()
            profile_file = fs_profile.save(profile_img.name, profile_img)
        except MultiValueDictKeyError:
            profile_file = FormUser.objects.get(id=usrid).picture
        FormUser.objects.filter(id=usrid).update(usr_name=Unam,
                                                name=name,
                                                bannerimage=banner_file,
                                                picture=profile_file
                                                )
        return redirect("User:UsrProfile")
   

def UsrChngPass(request):
    if 'Usrid' in request.session:
        if request.method == "POST":
            user=FormUser.objects.get(id=request.session['Usrid'])
            Cpass = request.POST.get('currpass')
            NPass = request.POST.get('newpass')
            origpass = user.password
            if Cpass != origpass:
                Error="  incorrect password"
                return render(request,"CreatorTemp/CrchngPass.html",{'ERR':Error})
            else:
                FormUser.objects.filter(id=request.session['Usrid']).update(password=NPass)
                del request.session["Usrid"]
                messages.success(request, 'Password changed successfully. Please login to your account.')
                return redirect("User:Login")
        return render(request, "UserTemp/ChangePass.html")
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')


def ViewAlbum(request, Aid):
    if 'Usrid' in request.session:
        album = get_object_or_404(Albums, id=Aid)
        creator = album.CrId
        Mdata = Music.objects.filter(Album=album)
        msg = messages.get_messages(request)
        pldata = playlist_data(request)
        return render(request, "UserTemp/ViewAlbum.html", {'pldata':pldata,'ALdata': album, 'CR': creator,'Mdata':Mdata, 'MSG': msg,'Aid':Aid})
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def ViewProfile(request, Cid):
    if 'Usrid' in request.session:
        session_usrid = request.session.get('Usrid')
        requested_creator = Creators.objects.get(id=Cid)
        music = Music.objects.filter(CrId=Cid)[:5]
        AlbumData = Albums.objects.filter(CrId=requested_creator)
        crplaylists = CrPlaylist.objects.filter(CrId=Cid, PlStatus=1)
        allmusic = Music.objects.filter(Q(CrId=Cid) | Q(collaborator_1=Cid) | Q(collaborator_2=Cid) | Q(collaborator_3=Cid))
        collabs = Music.objects.filter(Q(collaborator_1=Cid) | Q(collaborator_2=Cid) | Q(collaborator_3=Cid))
        is_following = FollowCr.objects.filter(follower=session_usrid, following=requested_creator).exists()
        follow_count = Follow.objects.filter(following=requested_creator).count()
        follow_cr_count = FollowCr.objects.filter(following=requested_creator).count()
        follower_count = follow_count + follow_cr_count
        pldata = playlist_data(request)
        messages_to_display = messages.get_messages(request)
        return render(request, "UserTemp/ProfileView.html", {'pldata':pldata,
                                                            'CR': requested_creator, 
                                                            'Mdata':music,
                                                            'ALdata': AlbumData,
                                                            'Allmusic':allmusic,
                                                            'collabs':collabs,
                                                            'follower_count':follower_count, 
                                                            'is_following': is_following,
                                                            'Playlist':crplaylists,
                                                            'messages_to_display':messages_to_display,
                                                            })
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')


def Followcr(request, Cid):
    if 'Usrid' in request.session:
        session_usrid = request.session.get('Usrid')
        cr =Creators.objects.get(id=Cid)
        follower = FormUser.objects.get(id=session_usrid)
        following = Creators.objects.get(id=Cid)
        FollowCr.objects.create(follower=follower, following=following)
        messages.success(request, 'Started Following '+cr.UsrName)
        return redirect('User:ViewProfile', Cid=Cid)
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')


def Unfollwcr(request, Cid):
    if 'Usrid' in request.session:
        session_usrid = request.session.get('Usrid')
        cr =Creators.objects.get(id=Cid)
        follower = get_object_or_404(FormUser, id=session_usrid)
        following = get_object_or_404(Creators, id=Cid)
        follow_entry = FollowCr.objects.filter(follower=follower, following=following).first()
        if follow_entry:
            follow_entry.delete()
        messages.success(request, 'Unfollowed ' +cr.UsrName)
        return redirect('User:ViewProfile', Cid=Cid)
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')


def search(request):
    query = request.GET.get('q', '')
    creators_results = Creators.objects.filter(UsrName__icontains=query).order_by('?')
    albums_results = Albums.objects.filter(Album_Name__icontains=query)
    music_results = Music.objects.filter(Title__icontains=query)

    creators_results = sorted(creators_results, key=lambda x: fuzz.partial_ratio(x.UsrName.replace(" ", ""), query.replace(" ", "")), reverse=True)
    albums_results = sorted(albums_results, key=lambda x: fuzz.partial_ratio(x.Album_Name.replace(" ", ""), query.replace(" ", "")), reverse=True)
    music_results = sorted(music_results, key=lambda x: fuzz.partial_ratio(x.Title.replace(" ", ""), query.replace(" ", "")), reverse=True)
    default_profile_image_url = '/static/CrAssets/img/profiledefault.jpg'
    creators_data = [
        {
            'id': creator.id, 
            'FullName': creator.FullName, 
            'UsrName': creator.UsrName,
            'profile':creator.Profile_Picture.url if creator.Profile_Picture and creator.Profile_Picture.url else default_profile_image_url,
        } for creator in creators_results
    ]
    albums_data = [
        {
            'id': album.id, 
            'Album_Name': album.Album_Name, 
            'Creator': album.CrId.UsrName,
            'album_img':album.Album_Cover.url,
        } for album in albums_results
    ]
    music_data = [
        {
            'id': music.id,
            'Title': music.Title,
            'Creator': music.CrId,
            'Collab1': music.collaborator_1 if music.collaborator_1 else None,
            'Collab2': music.collaborator_2 if music.collaborator_2 else None,
            'Collab3': music.collaborator_3 if music.collaborator_3 else None,
            'audio_file': music.audio_file.url,
            'music_cover': music.cover_art.url,
        } for music in music_results
    ]
    creators_and_albums = {}

    for creator in creators_data:
        creator_albums = Albums.objects.filter(CrId=creator['id']).order_by('?')[:5]
        shuffled_albums = list(creator_albums)
        random.shuffle(shuffled_albums)
        albums_for_creator = [{'id': album.id, 'Album_Name': album.Album_Name, 'Album_Image': album.Album_Cover.url} for album in shuffled_albums]
        creators_and_albums[creator['UsrName']] = albums_for_creator
    pldata = playlist_data(request)
    return render(request, 'UserTemp/search_results.html', {'creators_data': creators_data,
                                                                'albums_data': albums_data, 
                                                                'query': query, 
                                                                'creators_and_albums': creators_and_albums,
                                                                'music_data': music_data,
                                                                'pldata': pldata
                                                                })


def play_song(request):
    song_id = request.GET.get('song_id')
    default_profile_image_url = '/static/CrAssets/img/profiledefault.jpg'
    try:
        song = Music.objects.get(id=song_id)
        song_data = {
                "MusicId":song.id,
                "name": song.Title,
                "artist": song.CrId.UsrName,
                "img": song.cover_art.url,
                "audio": song.audio_file.url,
                "creatorid": song.CrId.id if song.CrId else None,
                "CrImg": song.CrId.Profile_Picture.url if song.CrId and song.CrId.Profile_Picture else default_profile_image_url,
                "Crrole": song.Crrole if song.Crrole else None,
                "alid":song.Album.id if song.Album else None,
                "alNm":song.Album.Album_Name if song.Album else None,
                "alCvr":song.Album.Album_Cover.url if song.Album else None,
                "rd": song.release_date if song.release_date else None,
                "lang": song.Language.Lang if song.Language else None,
                "genre":song.genre.Genre_Name if song.genre else None,
                "mood":song.Mood.Mood if song.Mood else None,
                "collab1id":song.collaborator_1.id if song.collaborator_1 else None,
                "collab1nm":song.collaborator_1.UsrName if song.collaborator_1 else None,
                "collab1img":song.collaborator_1.Profile_Picture.url if song.collaborator_1 and song.collaborator_1.Profile_Picture else default_profile_image_url,
                "collab1role":song.c1role if song.collaborator_1 else None,
                "collab2id":song.collaborator_2.id if song.collaborator_2 else None,
                "collab2nm":song.collaborator_2.UsrName if song.collaborator_2 else None,
                "collab2img":song.collaborator_2.Profile_Picture.url if song.collaborator_2 and song.collaborator_2.Profile_Picture  else default_profile_image_url,
                "collab2role":song.c2role if song.collaborator_2 else None,
                "collab3id":song.collaborator_3.id if song.collaborator_3 else None,
                "collab3nm":song.collaborator_3.UsrName if song.collaborator_3 else None,
                "collab3img":song.collaborator_3.Profile_Picture.url if song.collaborator_3 and song.collaborator_3.Profile_Picture  else default_profile_image_url,
                "collab3role":song.c3role if song.collaborator_3 else None,
            }
        return JsonResponse(song_data)   
    except Music.DoesNotExist:
        return JsonResponse({'error': 'Song not found'})
    
def play_album(request):
    album_id = request.GET.get('album_id')
    default_profile_image_url = '/static/CrAssets/img/profiledefault.jpg'

    try:
        album = Albums.objects.get(id=album_id)
        music_data = Music.objects.filter(Album=album)

        music_list = []

        for song in music_data:
            song_data = {
                "MusicId":song.id,
                "name": song.Title,
                "artist": song.CrId.UsrName,
                "img": song.cover_art.url,
                "audio": song.audio_file.url,
                "creatorid": song.CrId.id if song.CrId else None,
                "CrImg": song.CrId.Profile_Picture.url if song.CrId and song.CrId.Profile_Picture else default_profile_image_url,
                "Crrole": song.Crrole if song.Crrole else None,
                "alid":song.Album.id if song.Album else None,
                "alNm":song.Album.Album_Name if song.Album else None,
                "alCvr":song.Album.Album_Cover.url if song.Album else None,
                "rd": song.release_date if song.release_date else None,
                "lang": song.Language.Lang if song.Language else None,
                "genre":song.genre.Genre_Name if song.genre else None,
                "mood":song.Mood.Mood if song.Mood else None,
                "collab1id":song.collaborator_1.id if song.collaborator_1 else None,
                "collab1nm":song.collaborator_1.UsrName if song.collaborator_1 else None,
                "collab1img":song.collaborator_1.Profile_Picture.url if song.collaborator_1 and song.collaborator_1.Profile_Picture else default_profile_image_url,
                "collab1role":song.c1role if song.collaborator_1 else None,
                "collab2id":song.collaborator_2.id if song.collaborator_2 else None,
                "collab2nm":song.collaborator_2.UsrName if song.collaborator_2 else None,
                "collab2img":song.collaborator_2.Profile_Picture.url if song.collaborator_2 and song.collaborator_2.Profile_Picture  else default_profile_image_url,
                "collab2role":song.c2role if song.collaborator_2 else None,
                "collab3id":song.collaborator_3.id if song.collaborator_3 else None,
                "collab3nm":song.collaborator_3.UsrName if song.collaborator_3 else None,
                "collab3img":song.collaborator_3.Profile_Picture.url if song.collaborator_3 and song.collaborator_3.Profile_Picture  else default_profile_image_url,
                "collab3role":song.c3role if song.collaborator_3 else None,
            }
            music_list.append(song_data)

        response_data = {
            'music_data': music_list,
        }

        return JsonResponse(response_data)

    except Albums.DoesNotExist:
        return JsonResponse({'error': 'Album not found'})
    
def play_crplaylist(request):
    playlist_id = request.GET.get('playlist_id')
    default_profile_image_url = '/static/CrAssets/img/profiledefault.jpg'

    try:
        playlist = CrPlaylist.objects.get(id=playlist_id)
        playlist_items = CrPlaylistItem.objects.filter(CrPlid=playlist)
        music_data = Music.objects.filter(id__in=[item.MusicId.id for item in playlist_items])

        music_list = []

        for song in music_data:
            song_data = {
                "MusicId": song.id,
                "name": song.Title,
                "artist": song.CrId.UsrName,
                "img": song.cover_art.url,
                "audio": song.audio_file.url,
                "creatorid": song.CrId.id if song.CrId else None,
                "CrImg": song.CrId.Profile_Picture.url if song.CrId and song.CrId.Profile_Picture else default_profile_image_url,
                "Crrole": song.CrId.MusicRole if song.CrId.MusicRole else None,
                "alid": song.Album.id if song.Album else None,
                "alNm": song.Album.Album_Name if song.Album else None,
                "alCvr": song.Album.Album_Cover.url if song.Album else None,
                "rd": song.release_date,
                "lang": song.Language.Lang if song.Language else None,
                "genre": song.genre.Genre_Name if song.genre else None,
                "mood": song.Mood.Mood,
                "collab1id": song.collaborator_1.id if song.collaborator_1 else None,
                "collab1nm": song.collaborator_1.UsrName if song.collaborator_1 else None,
                "collab1img": song.collaborator_1.Profile_Picture.url if song.collaborator_1 and song.collaborator_1.Profile_Picture else default_profile_image_url,
                "collab1role": song.collaborator_1.MusicRole if song.collaborator_1 else None,
                "collab2id": song.collaborator_2.id if song.collaborator_2 else None,
                "collab2nm": song.collaborator_2.UsrName if song.collaborator_2 else None,
                "collab2img": song.collaborator_2.Profile_Picture.url if song.collaborator_2 and song.collaborator_2.Profile_Picture else default_profile_image_url,
                "collab2role": song.collaborator_2.MusicRole if song.collaborator_2 else None,
            }
            music_list.append(song_data)

        response_data = {
            'music_data': music_list,
        }

        return JsonResponse(response_data)

    except Playlist.DoesNotExist:
        return JsonResponse({'error': 'playlist not found or unauthorized'})
    except PlaylistItem.DoesNotExist:
        return JsonResponse({'error': 'playlistitem not found or unauthorized'})

def play_playlist(request):
    playlist_id = request.GET.get('playlist_id')
    user_id = request.session.get('Usrid')
    default_profile_image_url = '/static/CrAssets/img/profiledefault.jpg'

    try:
        playlist = Playlist.objects.get(id=playlist_id, UsrId=user_id)
        playlist_items = PlaylistItem.objects.filter(Plid=playlist)
        music_data = Music.objects.filter(id__in=[item.MusicId.id for item in playlist_items])
       

        music_list = []

        for song in music_data:
            song_data = {
                "MusicId": song.id,
                "name": song.Title,
                "artist": song.CrId.UsrName,
                "img": song.cover_art.url,
                "audio": song.audio_file.url,
                "creatorid": song.CrId.id if song.CrId else None,
                "CrImg": song.CrId.Profile_Picture.url if song.CrId and song.CrId.Profile_Picture else default_profile_image_url,
                "Crrole": song.CrId.MusicRole if song.CrId.MusicRole else None,
                "alid": song.Album.id if song.Album else None,
                "alNm": song.Album.Album_Name if song.Album else None,
                "alCvr": song.Album.Album_Cover.url if song.Album else None,
                "rd": song.release_date,
                "lang": song.Language.Lang if song.Language else None,
                "genre": song.genre.Genre_Name if song.genre else None,
                "mood": song.Mood.Mood,
                "collab1id": song.collaborator_1.id if song.collaborator_1 else None,
                "collab1nm": song.collaborator_1.UsrName if song.collaborator_1 else None,
                "collab1img": song.collaborator_1.Profile_Picture.url if song.collaborator_1 and song.collaborator_1.Profile_Picture else default_profile_image_url,
                "collab1role": song.collaborator_1.MusicRole if song.collaborator_1 else None,
                "collab2id": song.collaborator_2.id if song.collaborator_2 else None,
                "collab2nm": song.collaborator_2.UsrName if song.collaborator_2 else None,
                "collab2img": song.collaborator_2.Profile_Picture.url if song.collaborator_2 and song.collaborator_2.Profile_Picture else default_profile_image_url,
                "collab2role": song.collaborator_2.MusicRole if song.collaborator_2 else None,
            }
            music_list.append(song_data)

        response_data = {
            'music_data': music_list,
        }

        return JsonResponse(response_data)

    except Playlist.DoesNotExist:
        return JsonResponse({'error': 'playlist not found or unauthorized'})
    except PlaylistItem.DoesNotExist:
        return JsonResponse({'error': 'playlistitem not found or unauthorized'})



def CreatePlaylist(request):
    if 'Usrid' in request.session:
        if request.method == "POST":
            Pnam = request.POST.get("playlistname")
            Img = request.FILES.get('playlistcover', None)
            User=FormUser.objects.get(id=request.session['Usrid'])
            Playlist.objects.create(PlaylistName = Pnam,
                                    Playlist_Cover = Img,
                                    UsrId = User )
        messages.success(request, 'Playlist Successfully Created.')
        return redirect('User:AllPlaylist')
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def AllPlaylist(request):
    if 'Usrid' in request.session:
        User=FormUser.objects.get(id=request.session['Usrid'])
        data = Playlist.objects.filter(UsrId=User)
        messages_to_display = messages.get_messages(request)
        pldata = playlist_data(request)
        return render(request,'UserTemp/AllPlaylists.html',{'Playlist':data,
                                                            'pldata':pldata,
                                                            'messages_to_display':messages_to_display,
                                                            })
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def ViewPlaylist(request, Pid):
    if 'Usrid' in request.session:
        playlist = get_object_or_404(Playlist, id=Pid)
        User = playlist.UsrId
        playlist_items = PlaylistItem.objects.filter(Plid=playlist)
        songs = Music.objects.filter(id__in=[item.MusicId.id for item in playlist_items])
        messages_to_display = messages.get_messages(request)
        pldata = playlist_data(request)
        return render(request, "UserTemp/ViewPlaylist.html", {'PLdata': playlist,
                                                            'USR': User, 
                                                            'messages_to_display': messages_to_display,
                                                            'Mdata':songs,
                                                            'pldata':pldata,
                                                            })
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def UpdatePlaylist(request, Pid):
    if 'Usrid' in request.session:
        if request.method == "POST":
            Plnam = request.POST.get("playlistname")
            try:
                Cvr_img = request.FILES['playlistcover']
                fs_banner = FileSystemStorage()
                NewCvr_Img = fs_banner.save(Cvr_img.name, Cvr_img)
            except MultiValueDictKeyError:
                NewCvr_Img = Playlist.objects.get(id=Pid).Playlist_Cover if Playlist.objects.get(id=Pid).Playlist_Cover else None
            Playlist.objects.filter(id=Pid).update(
                                                    PlaylistName=Plnam,
                                                    Playlist_Cover=NewCvr_Img
                                                    )
        messages.success(request, 'Playlist Successfully Updated.')
        return redirect('User:ViewPlaylist',Pid)
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def AddtoPlaylist(request):
    if request.method == 'GET':
        playlist_id = request.GET.get('playlistId')
        music_id = request.GET.get('musicId')
        if 'Usrid' not in request.session:
            return JsonResponse({'status': 'error', 'message': 'User not in session'})
        user_id_from_session = request.session['Usrid']
        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Playlist not found'})
        if user_id_from_session == playlist.UsrId.id:
            music = get_object_or_404(Music, id=music_id)
            PlaylistItem.objects.create(Plid=playlist, MusicId=music)
            return JsonResponse({'status': 'success', 'message': 'Added to playlist successfully'})
        return JsonResponse({'status': 'error', 'message': 'User does not own the playlist'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def delete_from_usr_playlist(request, playlist_id, music_id):
    if 'Usrid' in request.session:
        playlist = get_object_or_404(Playlist, id=playlist_id)
        music = get_object_or_404(Music, id=music_id)
        playlist_item = get_object_or_404(PlaylistItem, Plid=playlist, MusicId=music)
        playlist_item.delete()
        messages.success(request, 'Item Sucessfully Removed From Playlist.')
        return redirect('User:ViewPlaylist',Pid=playlist.id)
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')


def AboutUs(request):
    pldata = playlist_data(request)
    messages_to_display = messages.get_messages(request)
    return render(request,'UserTemp/AboutUs.html',{'pldata':pldata,'messages_to_display':messages_to_display,})


def download_music(request):
    if 'Usrid' in request.session:
        song_id = request.GET.get('song_id')
        try:
            song = Music.objects.get(id=song_id)
            audio_file_path = os.path.join(settings.MEDIA_ROOT, song.audio_file.name)
            download_url = song.audio_file.url 

            return JsonResponse({'download_url': download_url})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Song not found'})
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')
    

def PlaylistView(request, Pid):
    if 'Usrid' in request.session:
        crplaylist = get_object_or_404(CrPlaylist, id=Pid)
        creator = crplaylist.CrId
        playlist_items = CrPlaylistItem.objects.filter(CrPlid=crplaylist)
        songs = Music.objects.filter(id__in=[item.MusicId.id for item in playlist_items])
        pldata = playlist_data(request)
        messages_to_display = messages.get_messages(request)
        return render(request, "UserTemp/ArtistPlaylist.html", {
                                                                'PLdata': crplaylist, 
                                                                'CR': creator, 
                                                                'messages_to_display': messages_to_display,
                                                                'Mdata': songs,
                                                                'pldata': pldata,
                                                                    })
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def songs_by_language(request, Lid):
    if 'Usrid' in request.session:
        language = Language.objects.get(pk=Lid)
        songs = Music.objects.filter(Language=language)
        context = {
            'language': language,
            'songs': songs,
        }
        return render(request, 'UserTemp/SongsbyLanguage.html', context)
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')

def songs_by_genre(request, Gid):
    if 'Usrid' in request.session:
        try:
            genre = Genre.objects.get(pk=Gid)
            songs = Music.objects.filter(genre=genre)
            context = {'genre': genre, 'songs': songs}
            return render(request, 'UserTemp/SongsbyGenre.html', context)
        except Genre.DoesNotExist:
            return render(request, 'UserTemp/Homepage.html', {'error_message': 'Genre not found'})
    else:
        messages.warning(request, 'Access Denied: Please log in to view this page.')
        return redirect('User:Login')
    