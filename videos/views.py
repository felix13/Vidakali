from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from videos.models import Video
from videos.forms import VideoForm

User = get_user_model()


@login_required
def home(request):
    videos = Video.objects.filter(parent=None).order_by('?')
    paginator = Paginator(videos, 6)
    page = request.GET.get('page')
    all_videos = paginator.get_page(page)
    return render(request, "videos/home.html", {'videos': all_videos})


@login_required
def add_video(request):
    data = {}
    form = VideoForm()
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.video_file = form.cleaned_data.get('video_file')
            video.post = form.cleaned_data.get('post')
            video.save()
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['video_form'] = render_to_string("videos/video_form.html", {'form': form}, request=request)  # noqa: E501

    data['video_form'] = render_to_string("videos/video_form.html", {'form': form}, request=request)  # noqa: E501
    return JsonResponse(data)


@login_required
def edit_video(request, id):
    data = {}
    video = get_object_or_404(Video, pk=id)
    form_instance = VideoForm(instance=video)
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['edited_video'] = render_to_string("videos/edit_video.html", {'form': form}, request=request)  # noqa: E501

    data['edit_video'] = render_to_string("videos/edit_video.html", {'form': form_instance}, request=request)  # noqa: E501
    return JsonResponse(data)


@login_required
def video(request, id):
    video = get_object_or_404(Video, id=id)
    side_videos = Video.objects.filter(parent=None).order_by('?').exclude(id=id)[:4]  # noqa: E501
    return render(request, 'videos/video.html', {'video': video, 'side_videos': side_videos})  # noqa: E501


@login_required
def comment(request):
    data = {}
    if request.method == 'POST':
        video_id = request.POST['video_id']
        video = Video.objects.get(pk=video_id)
        post = request.POST['post']
        post = post.strip()
        if len(post) > 0:
            user = request.user
            video.comment(user=user, post=post)
            data['partial_video_comments'] = render_to_string('videos/partial_video_comments.html', {'video': video}, request=request)  # noqa: E501
            data['comment_count'] = video.calculate_comments()
            return JsonResponse(data)
        else:
            return JsonResponse(data)


@login_required
def profile(request, username):
    page_user = get_object_or_404(User, username=username)
    all_videos = Video.objects.filter(parent=None).filter(user=page_user)
    return render(request, 'videos/profile.html', {'page_user': page_user, 'all_videos': all_videos})  # noqa: E501


@login_required
def remove(request):
    data = {}
    comment_id = request.POST.get('comment_id')
    comment = Video.objects.get(pk=comment_id)
    if comment.user == request.user:
        parent = comment.parent
        comment.delete()
        data['comment_count'] = parent.calculate_comments()

    data['partial_video_comments'] = render_to_string('videos/partial_video_comments.html', {'video': parent}, request=request)  # noqa: E501
    return JsonResponse(data)
