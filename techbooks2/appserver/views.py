from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .client import *
from .editor import *
from .login import login_server
from .utility import *
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login


def health_check(request):
    return HttpResponse("I'm GOOD")


def version(request):
    if request.method == 'POST':
        request_data = request_parse(request, quote=True)
        request_data = load_json(request_data)
        os = request_data.get('os')
        try:
            _version = make_version(Versions, os)
        except Exception:
            return HttpResponse('{"result" : "fail", "message" : "POST ERROR"}')
        _version = make_json(_version)
        return HttpResponse(_version, content_type='application/json; charset=utf-8')
    else:
        return HttpResponse('{"result" : "fail", "message" : "POST only"}')


def notice(request):
    _notice = make_notice(Notices)
    _notice = make_json(_notice)
    return HttpResponse(_notice, content_type='application/json; charset=utf-8')


def edition_info(request):
    if request.method == 'POST':
        request_data = request_parse(request, quote=True)
        request_data = load_json(request_data)
        role = request_data.get('role')
        try:
            _editions = make_edition(Editions, Articles, role)
        except Exception:
            return HttpResponse('{"result" : "fail", "message" : "POST ERROR"}')
        _editions = make_json(_editions)
        return HttpResponse(_editions, content_type='application/json; charset=utf-8')
    else:
        return HttpResponse('{"result" : "fail", "message" : "POST only"}')


def calender_info(request):
    try:
        _calender = make_calender(Editions)
        _calender = make_json(_calender)
    except Exception:
        return HttpResponse('{"result" : "fail", "message" : "PARSING ERROR"}')
    return HttpResponse(_calender, content_type='application/json; charset=utf-8')


def article(request):
    if request.method == 'POST':
        request_data = request_parse(request, quote=True)
        request_data = load_json(request_data)
        edition = int(request_data.get('address').split('_')[0])
        category = int(request_data.get('address').split('_')[-1])
        try:
            _article = make_article(Articles, edition, category)
        except Exception:
            return HttpResponse('{"result" : "fail", "message" : "POST ERROR"}')
        _article = make_json(_article)
        return HttpResponse(_article, content_type='application/json; charset=utf-8')
    else:
        return HttpResponse('{"result" : "fail", "message" : "POST only"}')


def app_login(request):
    if request.method == 'POST':
        request_data = request_parse(request, quote=True)
        request_data = load_json(request_data)
        id = request_data.get('id')
        pw = request_data.get('pw')
        return HttpResponse(login_server(Guests, id, pw), content_type='application/json; charset=utf-8')
    else:
        return HttpResponse('{"result" : "fail", "message" : "POST only"}')


def message(request):
    if request.method == 'POST':
        request_data = request_parse(request, quote=True)
        request_data = load_json(request_data)
        name = request_data.get('id')
        message = request_data.get('message')
        return HttpResponse(save_message(Messages, name, message), content_type='application/json; charset=utf-8')
    else:
        return HttpResponse('{"result" : "fail", "message" : "POST only"}')


def image_upload(request):
    return image_uploader(request)


def youtube(request, video_address):
    return render(request, 'youtube.html', {"video_address" : video_address})


def download_page(request):
    _version_a = make_version(Versions, "android").get("version")
    link_android = "" #removed for security reason.
    _version_i = make_version(Versions, "ios").get("version")
    link_ios = "" #removed for security reason.
    return render(request, 'download_page.html', {"link_ios" : link_ios, "link_android": link_android})

def admin_article_new(request):
    result = article_new(Articles, request)
    return result


def admin_article_modify(request, address):
    try:
        edition = int(address.split('_')[0])
        category = int(address.split('_')[-1])
        article = get_object_or_404(Articles, edition=edition, category=category)
        result = article_modify(Articles, article, request)
    except Exception:
        return redirect('admin_article_new')
    return render(request, 'admin/admin_article.html', result)


def admin_edition_new(request):
    result = edition_new(Editions, request)
    return result


def admin_edition_modify(request, edition_number):
    try:
        edition_number = int(edition_number)
        edition = get_object_or_404(Editions, edition=edition_number)
        result = edition_modify(Editions, edition, request)
    except Exception:
        return redirect('admin_edition_new')
    return result


def admin_version(request):
    try:
        result = version_modify(Versions, request)
    except Exception:
        print("Version pasrsing Error")
    return render(request, 'admin/admin_version.html', result)


def admin_message(request):
    try:
        unchecked_messages = Messages.objects.filter(check=False).order_by('-time')
        checked_messages = Messages.objects.filter(check=True).order_by('-time')
    except Exception:
        print("Message pasr asing Error")
    return render(request, 'admin/admin_message.html', {'unchecked' : unchecked_messages, 'checked' : checked_messages})


def admin_notice(request):
    result = notice_modify(Notices, request)
    return render(request, 'admin/admin_notice.html', result)


def admin_webviewer(request, edition_number):
    articles = Articles.objects.filter(edition=edition_number).order_by('category')
    articles_json = []
    for article in articles:
        articles_json.append(make_json(article.json_content()))
    return render(request, 'admin/admin_webviewer.html', {'articles' : articles_json})


def admin_main(request):
    role = "admin"
    _editions = make_edition(Editions, Articles, role)
    return render(request, 'admin/admin_main.html', {'editions' : _editions})


#@csrf_protect
#@never_cache ##Django doens't support https + csrf
def admin_login(request):
    epic_fail = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_main')
        else:
            epic_fail = True
    return render(request, 'admin/admin_login.html', {'epic_fail' : epic_fail})
