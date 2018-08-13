from django.contrib import admin
from .models import Versions, Editions, Articles, Messages, Guests, Notices
# Register your models here.

admin.site.register(Versions)
admin.site.register(Notices)
admin.site.register(Editions)
admin.site.register(Articles)
admin.site.register(Messages)
admin.site.register(Guests)
