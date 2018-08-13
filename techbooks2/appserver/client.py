

def make_version(Version, os):
    version_info = Version.objects.order_by('published_date').last()
    if os is 'android':
        version_json = version_info.json_version_a()
    else:
        version_json = version_info.json_version_i()
    return version_json


def make_notice(Notices):
    notice = Notices.objects.latest('publish_date')
    if not notice.is_valid():
        return {'result_msg' : 'N'}
    else:
        return notice.notice_json()


def make_edition(Editions, Articles, role):
    editions = Editions.objects
    if role != 'admin':
        editions = editions.filter(publish=True)
    editions = editions.order_by('-edition')
    edition_info = []
    for i in range(editions.count()):
        editions_dict = editions[i].json_edition()
        articles = Articles.objects.filter(edition=editions_dict['edition_number'])
        articles = articles.order_by('category')
        if role == 'guest':
            articles = articles.filter(guest=True)
        article_info = []
        for j in range(articles.count()):
            article_info.append(articles[j].json_list())
        editions_dict['article_info'] = article_info
        edition_info.append(editions_dict)
    return {'edition_info': edition_info}


def make_article(Articles, edition, category):
    article = Articles.objects.get(edition=edition, category=category)
    article.update_view_count()
    return article.json_content()


def make_calender(Editions):
    calenders = Editions.objects.all().exclude(calender__exact='').order_by('-edition')
    calender_info = []
    for calender in calenders:
        calender_info.append(calender.json_calender())
    return {'calender_info': calender_info}


def save_message(Messages, name, message):
    try:
        _message = Messages(name = name, message = message)
        _message.save()
    except Exception:
        return '{"result_msg" : "N"}'
    return '{"result_msg" : "Y"}'
