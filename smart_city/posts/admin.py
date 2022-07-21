from django.contrib import admin
from .models import News,Article,Question,Type_Question,Theme,Review,ImageQuestion

admin.site.register(News)
admin.site.register(Article)
admin.site.register(Question)
admin.site.register(Type_Question)
admin.site.register(ImageQuestion)
admin.site.register(Theme)
admin.site.register(Review)
