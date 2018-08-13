from django import forms

from .models import Articles, Editions, Guests, Notices, Versions

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ('guest', 'edition', 'category', 'title', 'content', 'tag')


class EditionForm(forms.ModelForm):
    class Meta:
        model = Editions
        fields = ('publish', 'year', 'month', 'edition', 'img', 'calender')


class GuestForm(forms.ModelForm):
    class Meta:
        model = Guests
        fields = ('client', 'id', 'pw', 'view_count')


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notices
        fields = ('content', 'publish_date', 'expire_date')


class VersionForm(forms.ModelForm):
    class Meta:
        model = Versions
        fields = ('version_a', 'version_i')
