from django.contrib import admin

from news_portal import models


admin.site.register(models.Author)
admin.site.register(models.Post)
admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.PostCategory)
