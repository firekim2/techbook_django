from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm, EditionForm, VersionForm, NoticeForm
from .client import make_article
from .utility import request_parse, load_json
from .models import base_url
from django.core.files.storage import FileSystemStorage
from PIL import Image
import io
import time


def article_new(Articles, request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            edition = str(form.cleaned_data['edition'])
            category = str(form.cleaned_data['category'])
            try:
                get_object_or_404(Articles, edition=edition, category=category)
            except:
                form.save()
            result = redirect('admin_edition_modify', address=edition + '_' + category)
    else:
        form = ArticleForm()
        result = render(request, 'admin/admin_article.html', {'form' : form})
    return result


def article_modify(Articles, article, request):
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
    else:
        form = ArticleForm(instance=article)
    return {'form' : form}


def edition_modify(Editions, edition, request):
    if request.method == "POST":
        form = EditionForm(request.POST, request.FILES, instance=edition)
        if form.is_valid():
            form.save(commit=True)
    form = EditionForm(instance=edition)
    return render(request, 'admin/admin_edition.html', {'form' : form, 'url' : edition.img.url})


def edition_new(Editions, request):
    if request.method == "POST":
        form = EditionForm(request.POST, request.FILES)
        if form.is_valid():
            edition_number = str(form.cleaned_data['edition'])
            try:
                get_object_or_404(Editions, edition=edition_number)
            except:
                form.save()
            result = redirect('admin_edition_modify', edition_number = edition_number)
    else:
        form = EditionForm()
        result = render(request, 'admin/admin_edition.html', {'form' : form})
    return result


def version_modify(Versions, request):
    if request.method == "POST":
        form = VersionForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        recent_version = Versions.objects.latest('published_date')
        form = VersionForm(instance=recent_version)
    return {'form' : form}


def notice_modify(Notices, request):
    recent_notice = Notices.objects.latest('publish_date')
    if request.method == "POST":
        form = NoticeForm(request.POST, instance=recent_notice)
        if form.is_valid():
            form.save()
    else:
        if recent_notice.is_valid():
            form = NoticeForm(instance=recent_notice)
        else:
            form = NoticeForm()
    return {'form' : form}


def image_uploader(request):
    if request.method == 'GET':
        return render(request, 'admin/image_upload.html')
    elif request.method == 'POST':
        image = request.FILES['image']
        post_info = request.POST
        name = image.name
        location = "/src/media/techbook/" + post_info['edition'] + "/"\
                    + post_info['category'] + "/" + post_info['label']
        fs = FileSystemStorage(location=location)
        if post_info['label'] == "image":
            im = Image.open(image)
            new_width = 960
            new_height = int(new_width * im.size[1] / im.size[0])
            im = im.resize((new_width, new_height), Image.ANTIALIAS)
            img_temp_byte = io.BytesIO()
            im.save(img_temp_byte, format='PNG', quality=100)
            image = img_temp_byte
        filename = fs.save(name, image)
        uploaded_file_url = fs.path(filename).replace('src/','')
        if request.is_ajax():
            return JsonResponse({'url' : base_url + uploaded_file_url})
    elif request.is_ajax():
        return JsonResponse({'url' : 'fail!! 관리자에게 문의하셈!!'})
    return render(request, 'admin/image_upload.html')
