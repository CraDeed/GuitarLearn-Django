from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .models import YoutubeTutorial, PlayList
from craw import youtube_craw


video_list = None

# class VideoListView(View):
#     def post(self, request):
#         SearchList.objects.all().delete()       # 기존 SearchList 데이터 삭제

def index(request):
    video_list = YoutubeTutorial.objects.all()

    return render(request, 'video/index.html', {'video_list': video_list})

def video_detail(request, key):
    
    video_lists = YoutubeTutorial.objects.all()
    referer = request.META.get('HTTP_REFERER', '')

    # playlists = PlayList.objects.filter(author=request.user)

    if PlayList.objects.filter(author=request.user).filter(key=key):
        playlist = get_object_or_404(PlayList.objects.filter(key=key))
    else:
        playlist = None

    if  video_lists.filter(key=key):
        video = get_object_or_404(YoutubeTutorial, key=key)
        
        return render(request, 'video/video_detail.html', {'video': video, 'playlist':playlist})

    elif referer == f'http://localhost:8000/guitarlearn/playlist/{request.user}':
        video = get_object_or_404(PlayList.objects.filter(author=request.user).filter(key=key))
        return render(request, 'video/video_detail.html', {'video': video, 'playlist':playlist})

    else:
        global video_list
        for i in range(len(video_list)):
            if key == video_list[i]['key']:
                video = video_list[i]

                return render(request, 'video/video_detail.html', {'video': video, 'playlist':playlist})
        
@login_required
def playlist(request,username):
    # playlist = get_object_or_404(PlayList, author=author)

    try:
        user = get_object_or_404(
            get_user_model(), username=username, is_active=True)
        playlist = PlayList.objects.filter(author=user)
    except PlayList.DoesNotExist: # if not, send DoesNotExist
        return render(request, 'video/playlist.html')
    return render(request, 'video/playlist.html', {'playlist': playlist})

@login_required
def user_page(request, username):
    page_user = get_object_or_404(
        get_user_model(), username=username, is_active=True)

    return render(request, "video/user_page.html", {
        'page_user': page_user,
    })

def search_list(request):
    if request.method == "GET":
        singer = request.GET.get('singer')
        songtitle = request.GET.get('songtitle')

        global video_list
        video_list = youtube_craw(singer,songtitle)

        return render(request, "video/search_list.html", {
            'video_list': video_list,
            'singer': singer,
            'songtitle': songtitle,
        })


@login_required
def video_like(request, key):
    video_lists = YoutubeTutorial.objects.all()
    playlist = PlayList.objects.filter(author=request.user).filter(key=key)
    
    if playlist in video_lists:
        redirect_url = request.META.get('HTTP_REFERER', '/')
        return redirect(redirect_url)
    else:
        if video_lists.filter(key=key):
            # item = video_lists.filter(key=key)#.values()
            title = video_lists.filter(key=key).values_list('title', flat=True)
            youtuber = video_lists.filter(key=key).values_list('youtuber', flat=True)
            thumbnail = video_lists.filter(key=key).values_list('thumbnail', flat=True)
            key = video_lists.filter(key=key).values_list('key', flat=True)
            PlayList(author=request.user, title=title, youtuber=youtuber,thumbnail=thumbnail,key=key).save()
            messages.success(request, '포스팅을 저장했습니다.')

            redirect_url = request.META.get('HTTP_REFERER', '/')
            return redirect(redirect_url)

        else:
            global video_list
            for i in range(len(video_list)):
                if key == video_list[i]['key']:
                    item = video_list[i]
                    PlayList(author=request.user ,title = item['title'], youtuber = item['youtuber'],thumbnail = item['thumbnail'], key = item['key']).save()
                    messages.success(request, '포스팅을 저장했습니다.')
                    redirect_url = request.META.get('HTTP_REFERER', '/')
                    return redirect(redirect_url)


@login_required
def video_unlike(request, key):

    playlists = PlayList.objects.filter(author=request.user).filter(key=key)
    
    video_lists = YoutubeTutorial.objects.all()

    playlist = get_object_or_404(playlists)
    playlist.delete()
    messages.success(request, f"포스팅 좋아요를 취소합니다.")
    redirect_url = request.META.get('HTTP_REFERER', 'root')
    return redirect(redirect_url)


def video_search(request):
    
    referer = request.META.get('HTTP_REFERER', '')
    q = request.POST.get('q', "")

    if referer == 'http://localhost:8000/guitarlearn/':
        video = YoutubeTutorial.objects.all().order_by('id')
    
        if q:
            videos = video.filter(
                Q(title__icontains=q) |
                Q(youtuber__icontains=q)
        )
            return render(request, 'video/search.html', {'videos' : videos, 'q' : q})
        
        else:
            return render(request, 'video/search.html')

    else:
        videos = []
        global video_list
        if q:
            for i in range(len(video_list)):
                if q in video_list[i]['title'] or q in video_list[i]['youtuber']:
                    videos.append(video_list[i])
                    print(videos)
        
            return render(request, 'video/search.html', {'videos' : videos, 'q' : q})
        else:
            return render(request, 'video/search.html')
